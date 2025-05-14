from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.db_models import MeetingInformation
from app.models.schemas import SummaryResponse
from app.services.summarizer import generate_summary


router = APIRouter()


@router.post("/upload", response_model=SummaryResponse)
async def upload_file(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    """
    Upload a text file and store its content in the database.
    """
    if not file.filename.endswith(".txt"):
        raise HTTPException(
            status_code=400, detail="Only .txt files are supported"
        )

    content = await file.read()
    content_str = content.decode("utf-8")

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
