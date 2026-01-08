from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, func
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from insuremate.core.config import DATABASE_URL, get_sqlalchemy_connect_args

connect_args = get_sqlalchemy_connect_args()

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args if connect_args is not None else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


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


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_prediction_result(user_input, predicted_category):
    db = SessionLocal()
    try:
        result = PredictionResult(
            age=user_input.age,
            weight=user_input.weight,
            height=user_input.height,
            income_lpa=user_input.income_lpa,
            smoker=user_input.smoker,
            city=user_input.city,
            occupation=user_input.occupation,
            bmi=user_input.bmi,
            lifestyle_risk=user_input.lifestyle_risk,
            age_group=user_input.age_group,
            city_tier=user_input.city_tier,
            predicted_category=predicted_category
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
    finally:
        db.close()


def get_all_results():
    db = SessionLocal()
    try:
        results = db.query(PredictionResult).all()
        return results
    finally:
        db.close()


def get_results_by_city(city: str):
    db = SessionLocal()
    try:
        results = db.query(PredictionResult).filter(PredictionResult.city == city).all()
        return results
    finally:
        db.close()


def get_results_by_category(category: str):
    db = SessionLocal()
    try:
        results = db.query(PredictionResult).filter(PredictionResult.predicted_category == category).all()
        return results
    finally:
        db.close()


def get_statistics():
    db = SessionLocal()
    try:
        total_predictions = db.query(PredictionResult).count()
        categories = db.query(PredictionResult.predicted_category).distinct().all()
        avg_bmi = db.query(func.avg(PredictionResult.bmi)).scalar()

        return {
            "total_predictions": total_predictions,
            "unique_categories": len(categories),
            "average_bmi": avg_bmi
        }
    finally:
        db.close()
