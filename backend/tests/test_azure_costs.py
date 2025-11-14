import pytest
from datetime import date
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from azure.core.exceptions import ClientAuthenticationError
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_azure_response():
    class MockResponse:
        @property
        def rows(self):
            return [
                [10.0, "resource-group-1", "USD"],
                [20.0, "resource-group-2", "USD"],
                [5.0, None, "USD"]  # Test unassigned resource group
            ]
    return MockResponse()

@pytest.fixture
def mock_env_vars():
    return {
        'AZURE_TENANT_ID': 'test-tenant',
        'AZURE_CLIENT_ID': 'test-client',
        'AZURE_CLIENT_SECRET': 'test-secret',
        'AZURE_SUBSCRIPTION_ID': 'test-subscription'
    }

def test_get_azure_costs_success(mock_azure_response, mock_env_vars):
    mock_mgmt_client = MagicMock()
    mock_mgmt_client.query.usage.return_value = mock_azure_response

    with patch('os.getenv', mock_env_vars.get), \
         patch('app.api.azure_routes.ClientSecretCredential') as mock_credential, \
         patch('app.api.azure_routes.CostManagementClient', return_value=mock_mgmt_client):

        response = client.get("/api/azure/costs", params={
            "start_date": "2025-06-01",
            "end_date": "2025-06-02"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["total_cost"] == 35.0  # Sum of all costs
        assert len(data["costs_by_resource_group"]) == 3
        assert data["currency"] == "USD"

        # Verify resource groups
        resource_groups = {cost["resource_group"] for cost in data["costs_by_resource_group"]}
        assert "resource-group-1" in resource_groups
        assert "resource-group-2" in resource_groups
        assert "Unassigned" in resource_groups

def test_get_azure_costs_invalid_dates():
    response = client.get("/api/azure/costs", params={
        "start_date": "2025-06-02",
        "end_date": "2025-06-01"  # End date before start date
    })
    assert response.status_code == 422  # Validation error
    error = response.json()
    assert "detail" in error
    assert "end_date must be after start_date" in error["detail"]

def test_get_azure_costs_authentication_error(mock_env_vars):
    with patch('os.getenv', mock_env_vars.get), \
         patch('app.api.azure_routes.ClientSecretCredential', side_effect=ClientAuthenticationError("Auth failed")):

        response = client.get("/api/azure/costs", params={
            "start_date": "2025-06-01",
            "end_date": "2025-06-02"
        })

        assert response.status_code == 401
        error = response.json()
        assert "detail" in error
        assert "Azure authentication failed" in error["detail"]


def test_get_azure_costs_missing_subscription():
    def mock_getenv(key, default=None):
        if key == 'AZURE_SUBSCRIPTION_ID':
            return None
        return {
            'AZURE_TENANT_ID': 'test-tenant',
            'AZURE_CLIENT_ID': 'test-client',
            'AZURE_CLIENT_SECRET': 'test-secret'
        }.get(key, default)
    
    with patch('os.getenv', mock_getenv):
        response = client.get("/api/azure/costs", params={
            "start_date": "2025-06-01",
            "end_date": "2025-06-02"
        })

        assert response.status_code == 400
        error = response.json()
        assert "detail" in error
        assert "AZURE_SUBSCRIPTION_ID is required" in error["detail"]
