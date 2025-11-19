from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
from app.services.athena_service import athena_service
from app.core.config import settings

router = APIRouter()

@router.get("/top-resources", response_model=List[Dict[str, Any]])
async def get_top_resources(limit: int = 10):
    """
    Get the top most expensive resources from AWS CUR.
    """
    query = f"""
        SELECT 
            line_item_resource_id,
            line_item_product_code,
            line_item_usage_type,
            SUM(line_item_unblended_cost) as total_cost,
            line_item_currency_code
        FROM "{settings.AWS_ATHENA_TABLE}"
        WHERE 
            line_item_line_item_type = 'Usage' 
            AND line_item_unblended_cost > 0
            AND date_parse(line_item_usage_start_date, '%Y-%m-%d %H:%i:%s') >= date_add('day', -30, current_date)
        GROUP BY 
            line_item_resource_id, 
            line_item_product_code, 
            line_item_usage_type,
            line_item_currency_code
        ORDER BY total_cost DESC
        LIMIT {limit}
    """
    
    try:
        execution_id = athena_service.execute_query(query)
        results = athena_service.get_query_results(execution_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/usage-by-operation", response_model=List[Dict[str, Any]])
async def get_usage_by_operation(limit: int = 10):
    """
    Get cost breakdown by operation (e.g., RunInstances, PutObject).
    """
    query = f"""
        SELECT 
            line_item_operation,
            line_item_product_code,
            SUM(line_item_unblended_cost) as total_cost
        FROM "{settings.AWS_ATHENA_TABLE}"
        WHERE 
            line_item_line_item_type = 'Usage'
            AND date_parse(line_item_usage_start_date, '%Y-%m-%d %H:%i:%s') >= date_add('day', -30, current_date)
        GROUP BY 
            line_item_operation,
            line_item_product_code
        ORDER BY total_cost DESC
        LIMIT {limit}
    """
    
    try:
        execution_id = athena_service.execute_query(query)
        results = athena_service.get_query_results(execution_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
