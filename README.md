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

## Cloud Cost Recommendation Model (T5)

CloudSathi includes an NLP module to generate cloud cost optimization recommendations using a fine-tuned T5 model.

### Training the Model

1. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
2. Prepare your dataset in `nlp/data/synthetic_cloud_costs.jsonl` (see example rows in the file).
3. Train the model (uses GPU if available, else CPU):
   ```bash
   cd ../nlp/scripts
   python train_t5.py
   ```
4. The trained model will be saved in `nlp/model/`.
5. (Optional) To push to Hugging Face Hub, set the `HF_TOKEN` environment variable.

#### Troubleshooting
- If you see errors about tensor dimensions or string types, ensure your training script uses `remove_columns=dataset.column_names` in the `map` call after tokenization.
- If you see errors about missing dependencies, run:
  ```bash
  pip install torch transformers datasets accelerate
  ```

### Using the Model for Recommendations

You can generate recommendations from cost data JSON using:

```python
from nlp.recommend import generate_recommendation

cost_data = {"EC2": "high usage", "S3": "infrequent access"}
rec = generate_recommendation(cost_data)
print(rec)  # e.g., "Switch EC2 to spot instances, move S3 to Glacier."
```

### Notes
- The training script and inference function will use GPU if available, otherwise fallback to CPU.
- You can expand the dataset with more real or synthetic cloud cost scenarios for better results.
- The model is now based on T5, which is suitable for text-to-text generation tasks.

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

## CI/CD & Code Quality

This project uses GitHub Actions for continuous integration and code quality checks. On every push and pull request to the `main` branch:

- **PyLint** checks Python code style and enforces a minimum score of 8.0
- **Pytest** runs all backend unit tests
- Status badges for build and lint are shown at the top of this README

You can find the workflow in `.github/workflows/python-tests.yml`.

### Running Locally

To check code quality and run tests before pushing:

```bash
cd backend
pylint app/ tests/
PYTHONPATH=$(pwd) pytest tests/ -v
```

All code must pass these checks before merging to `main`.

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
