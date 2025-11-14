# CloudSathi Frontend

This is the React dashboard for CloudSathi, providing cloud cost analytics and visualization for AWS and Azure.

## Features
- Fetches and displays cost data from `/api/aws/costs` and `/api/azure/costs`
- Line chart (Chart.js) for daily costs by service/resource group
- Dropdown to select cloud provider and date range
- Responsive design with Tailwind CSS (mobile & desktop)
- Error handling with toast notifications

## Getting Started

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation & Running
```bash
cd frontend
npm install
npm start
```
The app will run at [http://localhost:3000](http://localhost:3000) and expects the backend API to be available at `/api` (see Docker setup or proxy config for local development).

## Project Structure
- `src/components/CloudCostDashboard.tsx` — Main dashboard UI
- `src/utils/toast.tsx` — Toast notification hook
- `src/App.tsx` — App entry

## Customization
- Update API endpoints or chart logic as needed for your backend.
- Tailwind CSS is used for all styling.

## Troubleshooting
- If you see CORS or network errors, ensure the backend is running and accessible from the frontend.
- For styling issues, check Tailwind CSS setup and rebuild if needed.

---
Made with ❤️ by Saugat Tiwari
