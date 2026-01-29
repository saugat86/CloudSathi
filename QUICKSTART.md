# CloudSathi Quick Start Guide

Welcome to CloudSathi! This guide will help you get the application up and running in minutes.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **npm** (comes with Node.js)

## Quick Start (Easiest Method)

### For Linux/macOS:

```bash
./start.sh
```

### For Windows:

```cmd
start.bat
```

That's it! The script will:
1. Check if dependencies are installed
2. Install any missing dependencies
3. Create a `.env` configuration file
4. Start both the backend and frontend servers

## Manual Setup (Alternative)

If you prefer to set up manually or the automatic script doesn't work:

### Step 1: Install Backend Dependencies

```bash
cd backend
pip3 install -r requirements.txt
```

### Step 2: Configure Backend Environment

```bash
# Create .env file from template
cp .env.example .env

# The .env file is pre-configured for development with mock data
# No AWS/Azure credentials needed for testing!
```

### Step 3: Install Frontend Dependencies

```bash
cd frontend
npm install
```

### Step 4: Start the Backend

```bash
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Step 5: Start the Frontend (in a new terminal)

```bash
cd frontend
npm start
```

## Accessing the Application

Once both servers are running:

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Development Mode

The application runs in **development mode** by default with:

- ✅ **Mock Data Enabled** - No cloud credentials needed
- ✅ **Hot Reload** - Frontend and backend automatically reload on code changes
- ✅ **Sample Cost Data** - Pre-populated with AWS and Azure cost examples

### Mock Data

The application comes with built-in mock data for testing:

- AWS cost data for EC2, S3, RDS, Lambda, and CloudFront
- Azure cost data for multiple resource groups
- AI-powered cost optimization recommendations
- Sample budget and forecasting data

## Using Real Cloud Credentials (Optional)

If you want to connect to your real AWS/Azure accounts:

### AWS Configuration

Edit `backend/.env`:

```bash
AWS_ACCESS_KEY_ID=your-actual-access-key
AWS_SECRET_ACCESS_KEY=your-actual-secret-key
AWS_REGION=us-east-1

# Disable mock data
USE_MOCK_DATA=false
```

### Azure Configuration

Edit `backend/.env`:

```bash
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret

# Disable mock data
USE_MOCK_DATA=false
```

## Troubleshooting

### Backend won't start

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: Make sure you've installed the backend dependencies:
```bash
cd backend
pip3 install -r requirements.txt
```

### Frontend won't start

**Problem**: `command not found: npm`

**Solution**: Install Node.js from https://nodejs.org/

**Problem**: `Cannot find module 'react'`

**Solution**: Install frontend dependencies:
```bash
cd frontend
npm install
```

### Port already in use

**Problem**: `Error: Port 8000 is already in use`

**Solution**: Stop the existing process:
```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### API returns errors

**Problem**: API endpoints return 500 errors

**Solution**: Check that `USE_MOCK_DATA=true` is set in `backend/.env`

## Next Steps

- 📖 Read the full [README.md](README.md) for detailed documentation
- 🔧 Check out the [CLI Guide](docs/CLI_GUIDE.md) for command-line usage
- 🧪 See [TESTING_GUIDE.md](docs/TESTING_GUIDE.md) for running tests
- 🚀 Deploy to AWS using [DEPLOYMENT.md](docs/DEPLOYMENT.md)

## Docker Setup (Alternative)

If you prefer using Docker:

```bash
docker-compose up --build
```

This will start:
- Backend on http://localhost:8000
- Frontend on http://localhost:3000

## Features to Explore

Once the application is running, try:

1. **Dashboard** - View overall cloud spending trends
2. **Optimization** - See AI-powered cost optimization recommendations
3. **Cost Analyzer** - Deep dive into Cost and Usage Reports (CUR)
4. **API Docs** - Test API endpoints at http://localhost:8000/docs

## Getting Help

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review the main [README.md](README.md)
3. Open an issue on GitHub

---

Made with ❤️ for Nepal's startups 🇳🇵
