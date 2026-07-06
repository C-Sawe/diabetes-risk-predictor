# Diabetes Risk Prediction

This project is a web application that predicts a patient's risk of diabetes based on various health metrics and lifestyle factors. It uses a machine learning model trained on BRFSS (Behavioral Risk Factor Surveillance System) data.

## Project Structure

The project consists of two main components:
- **Backend (`/backend`)**: A FastAPI application that serves the machine learning model and provides REST API endpoints for inference, metrics, and dataset statistics.
- **Frontend (`/frontend`)**: A React application built with Vite and TypeScript that provides an interactive dashboard for users to input their data and view their risk assessment.

## Features

The model uses the following patient features to predict diabetes risk:
- Age & Gender
- High Blood Pressure
- High Cholesterol
- Smoking History
- History of Stroke
- Heart Disease or Attack
- Physical Activity
- Heavy Alcohol Consumption
- Difficulty Walking or Climbing Stairs

## Prerequisites

- Node.js & npm (for the frontend)
- Python 3.8+ (for the backend)
- Homebrew (optional, for Mac users as `start.sh` adds Homebrew to PATH)

## Running the Application Locally

You can launch both the backend API and the frontend dashboard simultaneously using the provided startup script.

Run the following command from the project root:

```bash
./start.sh
```

This will:
1. Start the FastAPI backend on `http://localhost:8000`.
2. Start the React frontend on `http://localhost:5173`.

To stop the application, simply press `Ctrl-C` in the terminal.

## Backend Endpoints

- `GET /health`: Health check endpoint.
- `GET /features`: Returns the features required by the model.
- `GET /metrics`: Returns model performance metrics.
- `GET /dataset`: Returns dataset statistics.
- `POST /predict`: Expects patient feature data and returns the probability and classified risk of diabetes.

## Development

- **Backend**: Python environment is managed in `backend/venv`. Ensure you activate it (`source venv/bin/activate`) before installing new dependencies or making changes to the ML model. The model artifacts are saved in `backend/artifacts`.
- **Frontend**: Navigate to `frontend/` and run `npm install` to install dependencies. You can run `npm run dev` to start the frontend development server independently.
