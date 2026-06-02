from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime

class QualityMetricsSchema(BaseModel):
    sharpness: float
    brightness: float
    contrast: float
    resolution: str
    feedback: str

class AnalysisRecordResponse(BaseModel):
    id: int
    image_name: str
    saved_path: str
    age: int
    primary_emotion: str
    emotion_details: Dict[str, float]
    quality_score: float
    quality_metrics: Dict[str, Any]
    
    # Advanced Facial Feature Fields (Optional for smooth schema migrations)
    eyes_details: Optional[str] = None
    lips_details: Optional[str] = None
    nose_details: Optional[str] = None
    skin_details: Optional[str] = None
    hair_details: Optional[str] = None
    
    created_at: datetime

    class Config:
        from_attributes = True

class DatabaseStatusResponse(BaseModel):
    status: str
    connected_url: Optional[str] = None
    error: Optional[str] = None

class AnalyticsResponse(BaseModel):
    total_scans: int
    average_quality: float
    average_face_score: float
    emotion_distribution: Dict[str, int]
    face_score_groups: Dict[str, int]
    quality_trend: List[Dict[str, Any]]
