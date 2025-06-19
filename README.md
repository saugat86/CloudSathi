# CloudSathi 🚀

[![Python Tests](https://github.com/saugat86/CloudSathi/actions/workflows/python-tests.yml/badge.svg)](https://github.com/saugat86/CloudSathi/actions/workflows/python-tests.yml)
[![Code style: pylint](https://img.shields.io/badge/code%20style-pylint-green)](https://github.com/PyCQA/pylint)

An open-source, GenAI-powered cloud cost optimization tool designed specifically for Nepal's startups.

## Overview

CloudSathi helps Nepali startups optimize their cloud costs using artificial intelligence. By analyzing cloud usage patterns and providing intelligent recommendations, it helps businesses save money while maintaining optimal performance.

## Features

- 🤖 AI-powered cost optimization recommendations
- 📊 Real-time cloud spending analytics
- 💡 Smart resource allocation suggestions
- 🔄 Automated cost optimization workflows
- 📈 Cost trend analysis and forecasting
- 🌐 Multi-cloud support (AWS, Azure, GCP)

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- Docker and Docker Compose
- AWS Account (for AWS cost analysis)
- Azure Account (for Azure cost analysis)

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/saugat86/CloudSathi.git
cd CloudSathi
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd ../frontend
npm install
```

4. Configure environment variables:
```bash
cd ../backend
cp .env.example .env
# Edit .env with your AWS and Azure credentials

# Run the application
docker-compose up
```

## Project Structure

```
CloudSathi/
├── backend/        # Python FastAPI backend
├── frontend/       # React.js frontend
├── infra/         # Infrastructure as Code (Terraform)
├── docs/          # Documentation
└── nlp/           # Natural Language Processing modules
```

## Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_region

# Azure Credentials
AZURE_SUBSCRIPTION_ID=your_subscription_id
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret
```

⚠️ Never commit your `.env` file to version control!

## API Documentation

### AWS Cost Endpoint

```
GET /api/aws/costs
```

Query Parameters:
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)

Example:
```bash
curl "http://localhost:8000/api/aws/costs?start_date=2025-06-01&end_date=2025-06-19"
```

Response:
```json
{
  "start_date": "2025-06-01",
  "end_date": "2025-06-19",
  "total_cost": 123.45,
  "currency": "USD",
  "costs_by_service": [
    {
      "service_name": "Amazon Elastic Compute Cloud",
      "amount": 45.67,
      "currency": "USD"
    }
  ]
}
```

### Azure Cost Endpoint

```
GET /api/azure/costs
```

Query Parameters:
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)

Example:
```bash
curl "http://localhost:8000/api/azure/costs?start_date=2025-06-01&end_date=2025-06-19"
```

Response:
```json
{
  "start_date": "2025-06-01",
  "end_date": "2025-06-19",
  "total_cost": 123.45,
  "currency": "USD",
  "costs_by_resource_group": [
    {
      "resource_group": "production-rg",
      "amount": 45.67,
      "currency": "USD"
    }
  ],
  "time_period_start": "2025-06-01",
  "time_period_end": "2025-06-19"
}
```

## Development Environment (Docker)

This project uses Docker Compose for local development. It spins up:

- **Backend**: FastAPI (Python 3.8) on port 8000
- **Frontend**: React (Node.js 16) on port 3000
- **Database**: SQLite (data persisted in `infra/db`)

### Commands

Start the environment:

```bash
cd infra
docker-compose up --build
```

Stop the environment:

```bash
docker-compose down
```

## Development

### Code Quality

We maintain high code quality standards using:
- **PyLint**: For Python code style and error checking
- **Pytest**: For unit testing
- **GitHub Actions**: For continuous integration

To run code quality checks locally:

```bash
cd backend

# Run PyLint
pylint app/ tests/

# Run Tests
PYTHONPATH=/path/to/CloudSathi/backend pytest tests/ -v
```

The GitHub Actions workflow automatically runs these checks on every push and pull request.

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

Before submitting a pull request:
1. Ensure all tests pass
2. Run PyLint and fix any issues
3. Update documentation as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you need help or have questions:

- Open an issue

## Authors

- Initial work - [Saugat Tiwari]

Made with ❤️ in Nepal 🇳🇵
