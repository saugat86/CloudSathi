import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from botocore.exceptions import ClientError
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_aws_response():
    return {
        'ResultsByTime': [
            {
                'TimePeriod': {
                    'Start': '2025-06-01',
                    'End': '2025-06-02'
                },
                'Groups': [
                    {
                        'Keys': ['Amazon Elastic Compute Cloud - Compute'],
                        'Metrics': {
                            'UnblendedCost': {
                                'Amount': '10.0',
                                'Unit': 'USD'
                            }
                        }
                    }
                ]
            }
        ]
    }

@pytest.fixture(autouse=True)
def mock_aws_env_vars(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_REGION", "us-east-1")

def test_get_aws_costs_success(mock_aws_response):
    with patch('boto3.client') as mock_client:
        mock_ce = MagicMock()
        mock_ce.get_cost_and_usage.return_value = mock_aws_response
        mock_client.return_value = mock_ce

        response = client.get("/api/aws/costs", params={
            "start_date": "2025-06-01",
            "end_date": "2025-06-02"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["total_cost"] == 10.0
        assert len(data["costs_by_service"]) == 1
        assert data["currency"] == "USD"

def test_get_aws_costs_invalid_dates():
    response = client.get("/api/aws/costs", params={
        "start_date": "2025-06-02",
        "end_date": "2025-06-01"  # End date before start date
    })
    assert response.status_code == 422  # Validation error
    error = response.json()
    assert "detail" in error
    assert error["detail"] == "end_date must be after start_date"

def test_get_aws_costs_access_denied():
    with patch('boto3.client') as mock_client:
        mock_ce = MagicMock()
        mock_ce.get_cost_and_usage.side_effect = ClientError(
            error_response={
                "Error": {
                    "Code": "AccessDeniedException",
                    "Message": "Access Denied"
                }
            },
            operation_name="GetCostAndUsage"
        )
        mock_client.return_value = mock_ce

        response = client.get("/api/aws/costs", params={
            "start_date": "2025-06-01",
            "end_date": "2025-06-02"
        })

        assert response.status_code == 403
        assert "Access denied" in response.json()["detail"]
