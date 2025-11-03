# Frontend

This directory contains the frontend code for the AI Readiness Score tool.

## Overview

The frontend will be built using Next.js and React. It will allow agencies and users to submit websites for scanning and view AI‑readiness scores and recommendations. It integrates with the FastAPI backend API and provides a dashboard for monitoring multiple sites.

### Features

- Input form to add website URLs to be scanned.
- Display the readiness score and recommendations returned by the backend.
- Table or list to manage multiple websites and show their current scores.
- Periodic refresh for monitoring.

## Development

1. Initialize a new Next.js project in this directory:

```
npx create-next-app@latest frontend
```

2. Install dependencies such as axios or use the native fetch API.

3. Configure environment variables to point to the backend FastAPI server (for example, `NEXT_PUBLIC_API_URL`).

4. Implement pages:
   - `/` – home page with a form to add a website.
   - `/sites` – dashboard listing added sites with scores.

5. Use a state management solution like React Context or Redux if necessary.

## Running

Ensure the backend is running (see the `backend` directory). Then start the Next.js development server:

```
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:3000`.
