"""API routes for Azure cost management."""
import os
from typing import List
from datetime import date
from fastapi import APIRouter, HTTPException, Query
from azure.identity import ClientSecretCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement.models import QueryDefinition, GranularityType, QueryTimePeriod
from azure.core.exceptions import ClientAuthenticationError
from app.api.azure_models import AzureCostResponse, ResourceGroupCost

azure_router = APIRouter()


def get_azure_credentials():
    """Retrieves Azure credentials from environment variables."""
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    tenant_id = os.getenv('AZURE_TENANT_ID')
    client_id = os.getenv('AZURE_CLIENT_ID')
    client_secret = os.getenv('AZURE_CLIENT_SECRET')
    if not subscription_id:
        raise HTTPException(
            status_code=400,
            detail="AZURE_SUBSCRIPTION_ID is required"
        )
    if not all([tenant_id, client_id, client_secret]):
        raise HTTPException(
            status_code=400,
            detail="Azure credentials are not properly configured. "
                   "Missing one or more required credentials."
        )
    return subscription_id, tenant_id, client_id, client_secret


def get_azure_client():
    """Initializes and returns the Azure Cost Management client."""
    try:
        subscription_id, tenant_id, client_id, client_secret = get_azure_credentials()
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        return CostManagementClient(credential, subscription_id)
    except HTTPException as exc:
        raise exc
    except ClientAuthenticationError as exc:
        raise HTTPException(
            status_code=401,
            detail="Azure authentication failed. Please check your credentials."
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize Azure client: {exc}"
        ) from exc


@azure_router.get("/costs", response_model=AzureCostResponse)
async def get_azure_costs(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)")
):
    """Retrieves Azure cost and usage data."""
    if end_date < start_date:
        raise HTTPException(
            status_code=422,
            detail="end_date must be after start_date"
        )
    try:
        subscription_id, _, _, _ = get_azure_credentials()
        client = get_azure_client()
        scope = f"/subscriptions/{subscription_id}"
        query_definition = QueryDefinition(
            type="ActualCost",
            timeframe="Custom",
            time_period=QueryTimePeriod(
                from_property=start_date.isoformat(),
                to=end_date.isoformat()
            ),
            dataset={
                "granularity": GranularityType.DAILY,
                "aggregation": {
                    "totalCost": {
                        "name": "Cost",
                        "function": "Sum"
                    }
                },
                "grouping": [
                    {
                        "type": "Dimension",
                        "name": "ResourceGroupName"
                    }
                ]
            }
        )
        response = client.query.usage(scope=scope, parameters=query_definition)
        total_cost = 0.0
        costs_by_resource_group: List[ResourceGroupCost] = []
        currency = "USD"  # Default to USD
        if response.rows:
            for row in response.rows:
                amount = float(row[0])  # Cost value
                resource_group = row[1]  # ResourceGroupName
                if amount > 0:
                    total_cost += amount
                    costs_by_resource_group.append(
                        ResourceGroupCost(
                            resource_group=resource_group or "Unassigned",
                            amount=amount,
                            currency=currency
                        )
                    )
        return AzureCostResponse(
            start_date=start_date,
            end_date=end_date,
            total_cost=total_cost,
            currency=currency,
            costs_by_resource_group=costs_by_resource_group,
            time_period_start=start_date.isoformat(),
            time_period_end=end_date.isoformat()
        )
    except HTTPException as exc:
        raise exc
    except ClientAuthenticationError as exc:
        raise HTTPException(
            status_code=401,
            detail="Azure authentication failed. Please check your credentials."
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {exc}"
        ) from exc
