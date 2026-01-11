from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from insuremate.db.base import Base

class PredictionResult(Base):
    __tablename__ = "prediction_results"

    id = Column(Integer, primary_key=True, index=True)

    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    income_lpa = Column(Float, nullable=False)
    smoker = Column(Boolean, nullable=False)
    city = Column(String, nullable=False)
    occupation = Column(String, nullable=False)

    bmi = Column(Float, nullable=False)
    lifestyle_risk = Column(String, nullable=False)
    age_group = Column(String, nullable=False)
    city_tier = Column(Integer, nullable=False)

    predicted_category = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<PredictionResult(id={self.id}, city={self.city}, predicted_category={self.predicted_category})>"
