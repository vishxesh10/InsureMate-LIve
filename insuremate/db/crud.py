from sqlalchemy import func
from insuremate.db.session import SessionLocal
from insuremate.db.models import PredictionResult

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
