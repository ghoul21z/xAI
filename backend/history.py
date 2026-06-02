import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import AnalysisRecord
from backend.schemas import AnalysisRecordResponse

# Initialize Router
router = APIRouter(tags=["history"])

# Define upload directory relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

@router.get("/api/history", response_model=List[AnalysisRecordResponse])
def get_history(db: Session = Depends(get_db)):
    """Retrieve full scanning history logs, sorted by creation date."""
    try:
        records = db.query(AnalysisRecord).order_by(AnalysisRecord.created_at.desc()).all()
        return [r.to_dict() for r in records]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not load scan logs from database: {e}"
        )

@router.delete("/api/history/{record_id}")
def delete_history_item(record_id: int, db: Session = Depends(get_db)):
    """Delete a scan record from the database and remove its corresponding image file."""
    record = db.query(AnalysisRecord).filter(AnalysisRecord.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found in system logs."
        )
        
    # Delete associated image file
    file_path = os.path.join(UPLOAD_DIR, record.saved_path)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error removing image file {file_path}: {e}")
            
    try:
        db.delete(record)
        db.commit()
        return {"status": "success", "message": f"Successfully deleted record #{record_id}"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not remove database record: {e}"
        )
