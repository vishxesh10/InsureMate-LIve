from fastapi import APIRouter
from insuremate.schemas import Userinput
from insuremate.services.predict import predict_from_user

router = APIRouter()


@router.post("/predict")
def predict(data: Userinput):
    prediction, db_record, explain_text, warnings = predict_from_user(data)
    return {
        "predicted_category": prediction,
        "result_id": db_record.id,
        "explain_text": explain_text,
        "warnings": warnings,
        "message": "Prediction saved successfully"
    }
