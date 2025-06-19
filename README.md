# CloudSathi 🚀

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
- Docker

### Installation

```bash
# Clone the repository
git clone https://github.com/saugat86/CloudSathi.git

# Navigate to the project directory
cd CloudSathi

# Set up the backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up the frontend
cd ../frontend
npm install

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

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you need help or have questions:

- Open an issue

## Authors

- Initial work - [Saugat Tiwari]

Made with ❤️ in Nepal 🇳🇵
