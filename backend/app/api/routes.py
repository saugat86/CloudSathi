from datetime import date
import os
from typing import List

from botocore.exceptions import ClientError
from fastapi import APIRouter, HTTPException, Query

from app.api.models import CostResponse, ServiceCost

import boto3

aws_router = APIRouter()


def get_aws_client():
    try:
        return boto3.client(
            'ce',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize AWS client: {str(e)}"
        ) from e


@aws_router.get("/costs", response_model=CostResponse)
async def get_aws_costs(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)")
):
    if end_date < start_date:
        raise HTTPException(
            status_code=422,
            detail="end_date must be after start_date"
        )
    client = get_aws_client()
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.isoformat(),
                'End': end_date.isoformat()
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
        total_cost = 0.0
        costs_by_service: List[ServiceCost] = []
        currency = 'USD'  # Default to USD as CE API typically returns costs in USD
        for result in response.get('ResultsByTime', []):
            for group in result.get('Groups', []):
                amount = float(group['Metrics']['UnblendedCost']['Amount'])
                if amount > 0:  # Only include services with costs
                    service_name = group['Keys'][0]
                    total_cost += amount
                    currency = group['Metrics']['UnblendedCost']['Unit']
                    costs_by_service.append(
                        ServiceCost(
                            service_name=service_name,
                            amount=amount,
                            currency=currency
                        )
                    )
        return CostResponse(
            start_date=start_date,
            end_date=end_date,
            total_cost=total_cost,
            currency=currency,
            costs_by_service=costs_by_service,
            time_period_start=response['ResultsByTime'][0]['TimePeriod']['Start'],
            time_period_end=response['ResultsByTime'][-1]['TimePeriod']['End']
        )
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            raise HTTPException(
                status_code=403,
                detail="Access denied. Please check your AWS credentials."
            ) from e
        raise HTTPException(
            status_code=500,
            detail=f"AWS API error: {str(e)}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) from e
