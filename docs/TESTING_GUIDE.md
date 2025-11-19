# CloudSathi - Local Testing Guide

This guide provides step-by-step instructions for testing the CloudSathi application on your local machine.

## Prerequisites

Before testing, ensure you have the following installed:

- **Python 3.8+**
- **Node.js 16+** (for frontend)
- **pip** (Python package manager)
- **Git**

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/saugat86/CloudSathi.git
cd CloudSathi
```

### 2. Backend Setup

#### Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Edit `.env` with your credentials (optional for basic testing):

```bash
# AWS Credentials (optional - only needed for AWS cost queries)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# Azure Credentials (optional - only needed for Azure cost queries)
AZURE_SUBSCRIPTION_ID=your_subscription_id
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret
```

> [!NOTE]
> You can test the application without cloud credentials. The API will return appropriate error messages for endpoints that require authentication.

## Running Tests

### Unit Tests

Run all backend unit tests:

```bash
cd backend
export PYTHONPATH=$PYTHONPATH:$(pwd)
pytest tests/ -v
```

Expected output:
```
========== 10 passed, 1 warning in 2.06s ==========
```

### Run Specific Test Files

```bash
# Test AWS endpoints
pytest tests/test_aws_costs.py -v

# Test Azure endpoints
pytest tests/test_azure_costs.py -v

# Test recommendation endpoints
pytest tests/test_recommendations.py -v
```

### Code Quality Checks

Run PyLint to check code quality:

```bash
cd backend
pylint app/ tests/
```

The project maintains a minimum PyLint score of 8.0.

## Running the Application

### Start the Backend Server

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

### Access API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Manual API Testing

### Using cURL

#### 1. Test AWS Costs Endpoint

```bash
curl "http://localhost:8000/api/aws/costs?start_date=2025-06-01&end_date=2025-06-19"
```

**Without credentials**, you'll get:
```json
{"detail": "AWS credentials not configured"}
```

**With valid credentials**, you'll get:
```json
{
  "start_date": "2025-06-01",
  "end_date": "2025-06-19",
  "total_cost": 123.45,
  "currency": "USD",
  "costs_by_service": [...]
}
```

#### 2. Test Azure Costs Endpoint

```bash
curl "http://localhost:8000/api/azure/costs?start_date=2025-06-01&end_date=2025-06-19"
```

#### 3. Test Recommendations Endpoint

```bash
curl -X POST http://localhost:8000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"cost_data": {"EC2": "high usage", "S3": "moderate usage"}}'
```

**Without trained model**, you'll get:
```json
{"detail": "Recommendation model not loaded."}
```

#### 4. Test Date Validation

```bash
# Invalid date range (end_date before start_date)
curl "http://localhost:8000/api/aws/costs?start_date=2025-06-19&end_date=2025-06-01"
```

Expected response:
```json
{"detail": "end_date must be after start_date"}
```

### Using Swagger UI

1. Open http://localhost:8000/docs in your browser
2. Expand any endpoint (e.g., `/api/aws/costs`)
3. Click **"Try it out"**
4. Fill in the parameters
5. Click **"Execute"**
6. View the response

## Testing with Docker

### Build and Run with Docker Compose

```bash
cd infra
docker-compose up --build
```

This will start:
- Backend on http://localhost:8000
- Frontend on http://localhost:3000
- SQLite database

### Stop the containers

```bash
docker-compose down
```

## Training the NLP Model (Optional)

To test the recommendation endpoint with a trained model:

```bash
cd nlp/scripts
python train_t5.py
```

This will:
1. Load training data from `nlp/data/synthetic_cloud_costs.jsonl`
2. Fine-tune a T5 model
3. Save the model to `nlp/model/`

After training, restart the backend server to load the model.

## Common Issues and Solutions

### Issue: Import Errors

**Problem**: `ImportError: cannot import name 'field_validator' from 'pydantic'`

**Solution**: Ensure Pydantic v2 is installed:
```bash
pip install "pydantic>=2.0.0"
```

### Issue: OpenSSL Errors

**Problem**: `AttributeError: module 'lib' has no attribute 'X509_V_FLAG_NOTIFY_POLICY'`

**Solution**: Upgrade pyopenssl and cryptography:
```bash
pip install --upgrade pyopenssl cryptography
```

### Issue: Model Not Loading

**Problem**: `[WARNING] Model directory not found or empty`

**Solution**: This is expected if you haven't trained the model yet. The recommendation endpoint will return an error, but other endpoints will work fine.

### Issue: Port Already in Use

**Problem**: `Error: [Errno 48] Address already in use`

**Solution**: Either stop the process using port 8000 or use a different port:
```bash
uvicorn app.main:app --port 8001
```

## Continuous Integration

The project uses GitHub Actions for CI/CD. On every push:

1. **PyLint** checks code quality (minimum score: 8.0)
2. **Pytest** runs all unit tests
3. Build status is shown in README badges

View the workflow: `.github/workflows/python-tests.yml`

## Test Coverage

Generate a test coverage report:

```bash
cd backend
pytest tests/ --cov=app --cov-report=html
```

Open `htmlcov/index.html` in your browser to view the coverage report.

## Performance Testing

### Load Testing with Apache Bench

```bash
# Test AWS costs endpoint
ab -n 100 -c 10 "http://localhost:8000/api/aws/costs?start_date=2025-06-01&end_date=2025-06-19"
```

### Response Time Testing

```bash
# Measure response time
time curl "http://localhost:8000/api/aws/costs?start_date=2025-06-01&end_date=2025-06-19"
```

## Frontend Testing (Optional)

If you want to test the frontend:

```bash
cd frontend
npm install
npm start
```

The frontend will be available at http://localhost:3000

## Troubleshooting

### Enable Debug Logging

Set the log level to DEBUG in the backend:

```bash
export LOG_LEVEL=DEBUG
uvicorn app.main:app --log-level debug
```

### Check Dependencies

Verify all dependencies are installed correctly:

```bash
pip list | grep -E "fastapi|pydantic|boto3|azure"
```

### Reset Environment

If you encounter persistent issues:

```bash
cd backend
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

After successful local testing:

1. **Deploy to staging** - Test with real cloud credentials
2. **Set up monitoring** - Add logging and metrics
3. **Configure CI/CD** - Automate deployments
4. **Add integration tests** - Test with real AWS/Azure APIs

## Support

If you encounter issues:

1. Check the [TEST_REPORT.md](TEST_REPORT.md) for known issues
2. Review the [CONTRIBUTING.md](../CONTRIBUTING.md) guide
3. Open an issue on GitHub

---

**Happy Testing! 🚀**
