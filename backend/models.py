import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from backend.database import Base

class AnalysisRecord(Base):
    __tablename__ = "analysis_records"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String(255), nullable=False)
    saved_path = Column(String(512), nullable=False)
    age = Column(Integer, nullable=False)
    primary_emotion = Column(String(50), nullable=False)
    emotion_details = Column(JSON, nullable=False)  # Map of emotion -> percentage
    quality_score = Column(Float, nullable=False)   # 0 to 100
    quality_metrics = Column(JSON, nullable=False)  # Breakdown: sharpness, brightness, contrast, resolution, feedback
    
    # Advanced Facial Feature Columns
    eyes_details = Column(String(255), nullable=True)
    lips_details = Column(String(255), nullable=True)
    nose_details = Column(String(255), nullable=True)
    skin_details = Column(String(255), nullable=True)  # Format: "HEX|Label", e.g., "#ebd0c0|Sáng hồng"
    hair_details = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        """Converts model to dictionary for easier serialization."""
        return {
            "id": self.id,
            "image_name": self.image_name,
            "saved_path": self.saved_path,
            "age": self.age,
            "primary_emotion": self.primary_emotion,
            "emotion_details": self.emotion_details,
            "quality_score": self.quality_score,
            "quality_metrics": self.quality_metrics,
            "eyes_details": self.eyes_details,
            "lips_details": self.lips_details,
            "nose_details": self.nose_details,
            "skin_details": self.skin_details,
            "hair_details": self.hair_details,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
