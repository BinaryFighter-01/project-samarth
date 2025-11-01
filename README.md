# Project Samarth

An intelligent Q&A system for querying Indian government agricultural and climate data using natural language.

## Overview

Project Samarth allows users to ask questions about Indian agriculture and climate data in plain English. The system uses Google Gemini AI to understand questions, fetch relevant data, and provide accurate answers with source citations.

## Features

- Natural language query processing
- Multi-dataset integration
- Automatic source citations
- Real-time chat interface
- Smart data filtering
- Works with sample data (no API required initially)

## Tech Stack

### Backend
- Python 3.11+
- Flask
- Google Gemini API
- Pandas

### Frontend
- React
- Tailwind CSS
- Lucide React

## Installation

### Backend Setup

```bash
# Create project directory
mkdir project-samarth
cd project-samarth
mkdir backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies (pre-built binaries)
pip install --only-binary :all: numpy pandas
pip install flask flask-cors google-generativeai requests python-dotenv
```

### Frontend Setup

```bash
# Navigate to project root
cd ..

# Create React app
npx create-react-app frontend
cd frontend

# Install dependencies
npm install lucide-react
```

## Configuration

### Get Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key

### Create .env File

Create `.env` file in `backend` directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
DATA_GOV_IN_API_KEY=
DEBUG=True
PORT=5000
```

## Project Structure

```
project-samarth/
├── backend/
│   ├── app.py
│   ├── query_processor.py
│   ├── data_fetcher.py
│   ├── requirements.txt
│   ├── .env
│   └── datasets/
│       ├── crop_production.csv
│       ├── rainfall_data.csv
│       └── agricultural_statistics.csv
└── frontend/
    ├── src/
    │   └── App.jsx
    └── package.json
```

## Running the Application

### Start Backend

```bash
cd backend
python app.py
```

Server runs on: http://localhost:5000

### Start Frontend

```bash
cd frontend
npm start
```

App opens at: http://localhost:3000

## Sample Questions

- Compare rainfall in Maharashtra and Punjab for last 5 years
- What are the top 3 crops produced in Kerala?
- Analyze wheat production trends in North India
- Why should we promote millets over rice in drought-prone regions?

## API Endpoints

### POST /api/query
Process a question and return answer with citations

Request:
```json
{
  "question": "Compare rainfall in Maharashtra and Punjab"
}
```

Response:
```json
{
  "answer": "Maharashtra receives...",
  "citations": [...],
  "query_plan": {...}
}
```

### GET /api/health
Check if API is running

### GET /api/datasets
List available datasets

## Data Sources

### Sample Datasets Included

1. Crop Production Statistics
   - States: Maharashtra, Punjab, Kerala, Uttar Pradesh
   - Years: 2019-2023
   - Crops: Rice, Wheat, Cotton, Coconut, Banana, Sugarcane

2. Rainfall Data
   - Annual rainfall, Monsoon rainfall, Rainy days
   - Years: 2019-2023

3. Agricultural Statistics
   - Total area, Irrigated area, Number of farmers
   - Years: 2019-2023

## Troubleshooting

### NumPy/Pandas Installation Error

If you get build errors, use pre-built binaries:
```bash
pip install --only-binary :all: numpy pandas
```

Or use Conda:
```bash
conda create -n samarth python=3.11
conda activate samarth
conda install pandas numpy
pip install flask flask-cors google-generativeai python-dotenv requests
```

### API Key Not Found

1. Check .env file exists in backend directory
2. Verify API key is correct
3. Restart Flask server

### CORS Errors

1. Ensure Flask-CORS is installed
2. Backend must be running on port 5000
3. Frontend should call http://localhost:5000

## How It Works

1. User asks question in chat interface
2. Gemini AI analyzes question and extracts parameters (states, crops, years)
3. System fetches relevant datasets and filters data
4. Gemini generates answer from the data
5. Response displayed with source citations

## Future Enhancements

- Live data.gov.in API integration
- More states and datasets
- Data visualizations
- Export to PDF/CSV
- Multi-language support
- Voice queries

## License

MIT License
