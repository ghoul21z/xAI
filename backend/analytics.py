from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from backend.database import get_db
from backend.models import AnalysisRecord
from backend.schemas import AnalyticsResponse

# Initialize Router
router = APIRouter(tags=["analytics"])

def get_face_score(r) -> float:
    """Helper to safely extract face_score from quality_metrics JSON."""
    if not r.quality_metrics:
        return 0.0
    metrics = r.quality_metrics
    if isinstance(metrics, str):
        import json
        try:
            metrics = json.loads(metrics)
        except Exception:
            metrics = {}
    return float(metrics.get("face_score", 0.0))

@router.get("/api/analytics", response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    """Retrieve dashboard aggregates for data charts (Face scores, Emotion distribution, Quality trends)."""
    try:
        records = db.query(AnalysisRecord).all()
        total_scans = len(records)
        
        if total_scans == 0:
            return {
                "total_scans": 0,
                "average_quality": 0.0,
                "average_face_score": 0.0,
                "emotion_distribution": {},
                "face_score_groups": {"5.0 - 6.0": 0, "6.1 - 7.0": 0, "7.1 - 8.0": 0, "8.1 - 9.0": 0, "9.1 - 10.0": 0},
                "quality_trend": []
            }
            
        avg_quality = round(sum(r.quality_score for r in records) / total_scans, 1)
        
        valid_scores = [get_face_score(r) for r in records if get_face_score(r) > 0.0]
        avg_face_score = round(sum(valid_scores) / len(valid_scores), 1) if valid_scores else 0.0
        
        # 1. Emotion distribution
        emotion_counts = {}
        for r in records:
            emotion = r.primary_emotion.capitalize()
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
        # 2. Face score groups aggregation
        face_score_groups = {
            "5.0 - 6.0": 0,
            "6.1 - 7.0": 0,
            "7.1 - 8.0": 0,
            "8.1 - 9.0": 0,
            "9.1 - 10.0": 0
        }
        
        for r in records:
            score = get_face_score(r)
            if score <= 0.0:
                continue
            if score <= 6.0:
                face_score_groups["5.0 - 6.0"] += 1
            elif score <= 7.0:
                face_score_groups["6.1 - 7.0"] += 1
            elif score <= 8.0:
                face_score_groups["7.1 - 8.0"] += 1
            elif score <= 9.0:
                face_score_groups["8.1 - 9.0"] += 1
            else:
                face_score_groups["9.1 - 10.0"] += 1
                
        # 3. Chronological timeline of recent scans (Last 10 scans)
        sorted_records = sorted(records, key=lambda x: x.created_at)
        recent_scans = sorted_records[-10:]
        quality_trend = [
            {
                "date": r.created_at.strftime("%m/%d %H:%M"),
                "score": round(r.quality_score, 1),
                "face_score": get_face_score(r)
            } for r in recent_scans
        ]
        
        return {
            "total_scans": total_scans,
            "average_quality": avg_quality,
            "average_face_score": avg_face_score,
            "emotion_distribution": emotion_counts,
            "face_score_groups": face_score_groups,
            "quality_trend": quality_trend
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not load analytics metrics from database: {e}"
        )
