import boto3
import time
import logging
from typing import List, Dict, Any, Optional
from botocore.exceptions import ClientError
from app.core.config import settings

logger = logging.getLogger(__name__)

class AthenaService:
    def __init__(self):
        self.database = settings.AWS_ATHENA_DATABASE
        self.table = settings.AWS_ATHENA_TABLE
        self.output_location = settings.AWS_ATHENA_OUTPUT_LOCATION
        self.region = settings.AWS_REGION
        
        # Initialize Athena client only if credentials are present
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            self.client = boto3.client(
                'athena',
                region_name=self.region,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
        else:
            self.client = None
            logger.warning("AWS credentials not found. AthenaService will run in mock mode.")

    def execute_query(self, query_string: str) -> str:
        """
        Submits a query to Athena and returns the execution ID.
        """
        if not self.client:
            return "mock-execution-id"

        try:
            response = self.client.start_query_execution(
                QueryString=query_string,
                QueryExecutionContext={'Database': self.database},
                ResultConfiguration={'OutputLocation': self.output_location}
            )
            return response['QueryExecutionId']
        except ClientError as e:
            logger.error(f"Athena query execution failed: {e}")
            raise

    def get_query_results(self, query_execution_id: str) -> List[Dict[str, Any]]:
        """
        Waits for the query to complete and returns the results.
        """
        if not self.client or query_execution_id == "mock-execution-id":
            return self._get_mock_results()

        try:
            # Wait for query to complete
            while True:
                response = self.client.get_query_execution(QueryExecutionId=query_execution_id)
                state = response['QueryExecution']['Status']['State']
                
                if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                    break
                time.sleep(1)  # Wait before polling again

            if state != 'SUCCEEDED':
                raise Exception(f"Query failed with status: {state}")

            # Fetch results
            results_paginator = self.client.get_paginator('get_query_results')
            results_iter = results_paginator.paginate(
                QueryExecutionId=query_execution_id,
                PaginationConfig={'PageSize': 1000}
            )

            results = []
            for results_page in results_iter:
                rows = results_page['ResultSet']['Rows']
                # Skip header row if it's the first page
                if len(results) == 0:
                    headers = [col['VarCharValue'] for col in rows[0]['Data']]
                    rows = rows[1:]
                
                for row in rows:
                    data = [col.get('VarCharValue', None) for col in row['Data']]
                    results.append(dict(zip(headers, data)))
            
            return results

        except ClientError as e:
            logger.error(f"Failed to get query results: {e}")
            raise

    def _get_mock_results(self) -> List[Dict[str, Any]]:
        """
        Returns mock CUR data for testing/demo purposes.
        """
        return [
            {
                "line_item_resource_id": "i-0123456789abcdef0",
                "line_item_product_code": "AmazonEC2",
                "line_item_usage_type": "RunInstances:SV006:t3.large",
                "line_item_unblended_cost": "145.20",
                "line_item_currency_code": "USD"
            },
            {
                "line_item_resource_id": "vol-0abcdef1234567890",
                "line_item_product_code": "AmazonEC2",
                "line_item_usage_type": "EBS:VolumeUsage.gp2",
                "line_item_unblended_cost": "45.50",
                "line_item_currency_code": "USD"
            },
            {
                "line_item_resource_id": "arn:aws:rds:us-east-1:123456789012:db:prod-db",
                "line_item_product_code": "AmazonRDS",
                "line_item_usage_type": "InstanceUsage:db.m5.large",
                "line_item_unblended_cost": "280.00",
                "line_item_currency_code": "USD"
            },
            {
                "line_item_resource_id": "arn:aws:s3:::my-production-bucket",
                "line_item_product_code": "AmazonS3",
                "line_item_usage_type": "TimedStorage-ByteHrs",
                "line_item_unblended_cost": "89.30",
                "line_item_currency_code": "USD"
            },
            {
                "line_item_resource_id": "arn:aws:lambda:us-east-1:123456789012:function:process-data",
                "line_item_product_code": "AWSLambda",
                "line_item_usage_type": "Lambda-GB-Second",
                "line_item_unblended_cost": "12.45",
                "line_item_currency_code": "USD"
            }
        ]

athena_service = AthenaService()
