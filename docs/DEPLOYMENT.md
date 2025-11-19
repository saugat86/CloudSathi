# CloudSathi AWS Deployment Guide

This guide details how to deploy the CloudSathi application to AWS using a modern, scalable, and cost-effective architecture.

## Architecture Overview

- **Backend**: **AWS App Runner** (Managed container service)
  - Automatically builds and deploys from your GitHub repository or container registry.
  - Handles load balancing, SSL/TLS, and auto-scaling.
- **Frontend**: **AWS Amplify** (Static web hosting)
  - Connects to your Git repository.
  - Automatically builds and deploys the React application.
  - Provides global CDN content delivery.

---

## Prerequisites

1. **AWS Account**: You need an active AWS account.
2. **GitHub Repository**: The code must be pushed to a GitHub repository.
3. **AWS CLI** (Optional): For local testing and configuration.

---

## Part 1: Backend Deployment (AWS App Runner)

App Runner is the easiest way to deploy containerized web applications on AWS.

### Option A: Deploy from Source (Recommended)

1. **Go to AWS App Runner Console** and click **Create service**.
2. **Source**: Select **Source code repository**.
3. **Connect to GitHub**: Link your AWS account to your GitHub account and select the `CloudSathi` repository.
4. **Branch**: Select `main`.
5. **Configuration**:
   - **Runtime**: Python 3
   - **Build command**: `pip install -r backend/requirements.txt`
   - **Start command**: `uvicorn app.main:app --host 0.0.0.0 --port 8080 --app-dir backend`
   - **Port**: `8080`
6. **Environment Variables**: Add the following secrets/variables:
   - `AWS_ACCESS_KEY_ID`: (Your AWS Access Key)
   - `AWS_SECRET_ACCESS_KEY`: (Your AWS Secret Key)
   - `AWS_REGION`: `us-east-1`
   - `AWS_ATHENA_DATABASE`: (Your Athena Database)
   - `AWS_ATHENA_TABLE`: (Your Athena Table)
   - `AWS_ATHENA_OUTPUT_LOCATION`: (Your S3 Bucket for Athena results)
7. **Create & Deploy**: Click **Create service**. AWS will build and deploy your application.
8. **Copy URL**: Once deployed, copy the **Default domain** (e.g., `https://xyz.us-east-1.awsapprunner.com`). You will need this for the frontend.

### Option B: Deploy from Container Image (ECR)

If you prefer to build the Docker image yourself:

1. **Build & Push**:
   ```bash
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

   # Build
   docker build -t cloudsathi-backend ./backend

   # Tag & Push
   docker tag cloudsathi-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/cloudsathi-backend:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/cloudsathi-backend:latest
   ```
2. **App Runner**: Select **Container registry** as source and point to your ECR image.

---

## Part 2: Frontend Deployment (AWS Amplify)

Amplify Hosting provides a git-based workflow for hosting fullstack serverless web apps.

1. **Go to AWS Amplify Console** and click **New app** > **Host web app**.
2. **Source Code**: Select **GitHub**.
3. **Repository**: Select `CloudSathi` and the `main` branch.
4. **Build Settings**:
   - Amplify should automatically detect the settings. Ensure `appRoot` is set to `frontend` if it asks, or modify `amplify.yml` if needed.
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
5. **Environment Variables**:
   - Click **Advanced settings** > **Environment variables**.
   - Key: `REACT_APP_API_URL`
   - Value: (The App Runner URL from Part 1, e.g., `https://xyz.us-east-1.awsapprunner.com`)
   - Key: `REACT_APP_USE_MOCK_DATA`
   - Value: `false` (for production)
6. **Save and Deploy**: Click **Save and deploy**.
7. **Verify**: Once the build completes, click the provided URL to access your live CloudSathi application.

---

## Part 3: Local Development with Docker

To run the entire stack locally using Docker Compose:

1. **Configure Environment**:
   Create a `.env` file in the root directory (or rely on `docker-compose.yml` defaults).

2. **Run**:
   ```bash
   docker-compose up --build
   ```

3. **Access**:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Troubleshooting

- **Backend Health Check Fails**: Ensure the `PORT` environment variable matches what App Runner expects (default 8080) or configure App Runner to use port 8000.
- **CORS Errors**: Ensure the backend `CORSMiddleware` allows the Amplify domain. You may need to update `backend/app/main.py` to include your Amplify URL in `allow_origins`.
