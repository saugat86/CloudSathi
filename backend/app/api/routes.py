"""API routes for AWS cost management."""
from datetime import date
import os
import logging
from typing import List

from botocore.exceptions import ClientError, NoCredentialsError
from fastapi import APIRouter, HTTPException, Query

from app.api.models import CostResponse, ServiceCost

import boto3

aws_router = APIRouter()
logger = logging.getLogger(__name__)


@aws_router.get("/costs", response_model=CostResponse)
async def get_aws_costs(
    start_date: date = Query(..., description="Start date"),
    end_date: date = Query(..., description="End date"),
):
    """Retrieves AWS cost and usage data."""
    if end_date < start_date:
        raise HTTPException(
            status_code=422,
            detail="end_date must be after start_date"
        )
    
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION')

    if not all([aws_access_key_id, aws_secret_access_key, aws_region]):
        logger.error("AWS credentials or region not found")
        raise HTTPException(
            status_code=500,
            detail="AWS credentials or region not found. "
                   "Please set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION environment variables."
        )

    try:
        client = boto3.client(
            'ce',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )
    except NoCredentialsError as exc:
        logger.error("Invalid AWS credentials")
        raise HTTPException(
            status_code=500,
            detail="Invalid AWS credentials. Please check your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
        ) from exc
    except Exception as e:
        logger.error("Failed to initialize AWS client: %s", e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize AWS client: {e}"
        ) from e

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
        results = response.get('ResultsByTime', [])
        total_cost = 0.0
        daily_costs_by_service: List[ServiceCost] = []
        currency = 'USD'  # Default to USD as CE API typically returns costs in USD
        
        time_period_start = None
        time_period_end = None
        if results:
            time_period_start = results[0]['TimePeriod']['Start']
            time_period_end = results[-1]['TimePeriod']['End']

        for result in results:
            for group in result.get('Groups', []):
                amount = float(group['Metrics']['UnblendedCost']['Amount'])
                if amount > 0:  # Only include services with costs
                    service_name = group['Keys'][0]
                    total_cost += amount
                    currency = group['Metrics']['UnblendedCost']['Unit']
                    daily_costs_by_service.append(
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
            costs_by_service=daily_costs_by_service,
            time_period_start=time_period_start,
            time_period_end=time_period_end
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
            detail=f"AWS API error: {e}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {e}"
        ) from e
