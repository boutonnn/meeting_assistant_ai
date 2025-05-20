Meeting Summarizer  

A minimalist web application for uploading meeting audio/text files, analyzing their content using a language model, and generating structured summaries.  

Features

Upload text files containing meeting transcripts.  
Analyze content using OpenAI's API to generate structured summaries.  
Display results with status updates (pending, completed).  
Store analysis data in a PostgreSQL database.  
REST API with endpoints for upload, analysis, and result retrieval.  
Basic unit tests for backend functionality.  

Architecture

Backend: Built with FastAPI, SQLAlchemy for PostgreSQL 
Frontend: React single-page application styled with Tailwind CSS.  
integration, and OpenAI API for summarization.  
Database: PostgreSQL to store file metadata and analysis results.  
API: RESTful endpoints (/upload, /analyze, /results/{id}).  

Installation  
Prerequisites  

Python 3.9+  
Node.js 18+  
PostgreSQL  
OpenAI API key  

Backend Setup  

Navigate to the backend directory:cd backend  


Create a virtual environment and activate it:python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate  


Install dependencies:pip install -r requirements.txt  


Create a .env file in the backend directory:   DATABASE_URL=postgresql://user:password@localhost:5432/meeting_db  
OPENAI_API_KEY=your_openai_api_key_here  


Set up the PostgreSQL database:createdb meeting_db  


Run the backend server:uvicorn app.main:app -- host 0.0.0.0 --port 8000 --reload  

Frontend Setup  

Navigate to the frontend directory:  
cd frontend  


Install dependencies:  
npm install  


Start the development server:  
npm start  


Running the Application  

Ensure the PostgreSQL database is running.  
Start the backend server (http://localhost:8000).  
Start the frontend server (http://localhost:5147).  
Open the frontend in a browser to upload files and view summaries.  

API Documentation  

POST /upload: Upload a text file.  
Request: Form-data with file (text file).  
Response: Analysis object with id, filename, content, status.  


POST /analyze: Analyze the uploaded file and generate a summary.  
Response: Updated analysis object with summary and status.  


GET /results/{id}: Retrieve analysis results.  
Response: Analysis object.  



Points for Improvement  

Add audio file processing (e.g., using speech-to-text libraries like Whisper).  
Implement advanced interactive features (e.g., task extraction, topic detection).  
Add Docker configuration for easier deployment.  
Enhance error handling and user feedback.  
Adding more logging.  
Expand unit tests to cover more edge cases.  

Notes  

The application assumes text input for simplicity. Audio processing can be added with libraries like pydub or speech_recognition.  
The OpenAI API key must be provided via the .env file.  


