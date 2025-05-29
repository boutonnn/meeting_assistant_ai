from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.db_models import MeetingInformation
from app.models.schemas import SummaryResponse
from app.services.summarizer import generate_summary, transcribe_audio
import shutil
import os
import tempfile


router = APIRouter()


@router.get("/")
async def root():
    return {"msg": "welcome to the meeting assistant ai"}


@router.post("/upload", response_model=SummaryResponse)
async def upload_file(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    """
    Upload a text or audio file and store its content in the database.
    """
    valid_extensions = {".txt", ".mp3", ".wav"}
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in valid_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only .txt, .mp3, or .wav files are supported",
        )

    if file_extension == ".txt":
        content = await file.read()
        content_str = content.decode("utf-8")
    else:
        # Save audio file temporarily
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=file_extension
        ) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_file_path = tmp_file.name

        try:
            # Transcribe audio
            content_str = transcribe_audio(tmp_file_path)
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)

    meeting_content = MeetingInformation(
        filename=file.filename, content=content_str, status="pending"
    )
    db.add(meeting_content)
    db.commit()
    db.refresh(meeting_content)

    return meeting_content


@router.post("/analyze", response_model=SummaryResponse)
async def analyze_file(id: int, db: Session = Depends(get_db)):
    """
    Analyze the content of a file and generate a summary.
    """
    meeting_info = (
        db.query(MeetingInformation)
        .filter(MeetingInformation.id == id)
        .first()
    )
    if not meeting_info:
        raise HTTPException(
            status_code=404, detail="Meeting information not found"
        )

    if meeting_info.status == "completed":
        return meeting_info

    try:
        meeting_info.status = "in progress"
        meeting_info.summary = generate_summary(meeting_info.content)
        meeting_info.status = "completed"
        db.commit()
        db.refresh(meeting_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return meeting_info


@router.get("/results/{id}", response_model=SummaryResponse)
async def get_results(id: int, db: Session = Depends(get_db)):
    """
    Retrieve the meeting summary for a given ID.
    """
    meeting_info = (
        db.query(MeetingInformation)
        .filter(MeetingInformation.id == id)
        .first()
    )
    if not meeting_info:
        raise HTTPException(
            status_code=404, detail="Meeting information not found"
        )

    return meeting_info
