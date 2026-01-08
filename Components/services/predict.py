
from pathlib import Path
import pickle
import pandas as pd
import sys
import importlib
from typing import Dict, Any
from collections import deque
from datetime import datetime
import warnings

# Add compatibility for missing _RemainderColsList
import sklearn.compose._column_transformer

class _RemainderColsList(list):
    """Mock class for backward compatibility with older scikit-learn versions."""
    pass

# Make the class available in the module
setattr(sklearn.compose._column_transformer, '_RemainderColsList', _RemainderColsList)

from Components.models import Userinput
from Components.db.database import save_prediction_result
from Components.core.config import MODEL_PATH

# In-memory recent predictions (simple audit log)
_RECENT = deque(maxlen=3)

# Prefer the env-driven MODEL_PATH from config, fallback to package/root locations
_MODEL_PATH = Path(MODEL_PATH)
if not _MODEL_PATH.exists():
    potential = Path(__file__).resolve().parent.parent / "model.pkl"
    if potential.exists():
        _MODEL_PATH = potential
    else:
        root_fallback = Path.cwd() / "model.pkl"
        _MODEL_PATH = root_fallback

try:
    with open(_MODEL_PATH, "rb") as f:
        # Suppress sklearn unpickle/version warnings only during model load
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=Warning)
            _MODEL = pickle.load(f)
    print(f"Model loaded successfully from {_MODEL_PATH}")
except AttributeError as e:
    print(f"Error loading model: {e}")
    print("This is likely due to a version mismatch with scikit-learn.")
    print("Please ensure you're using the same version of scikit-learn that was used to train the model.")
    raise


def predict_from_user(user: Userinput):
    """Run prediction and persist result to DB.
    Returns (prediction, db_record, explain_text, warnings)
    """
    input_df = pd.DataFrame([{
        "bmi": user.bmi,
        "lifestyle_risk": user.lifestyle_risk,
        "age_group": user.age_group,
        "city_tier": user.city_tier,
        "occupation": user.occupation,
        "income_lpa": user.income_lpa
    }])

    # Run model
    prediction = _MODEL.predict(input_df)[0]

    # Generate warnings for unrealistic combos
    warnings: list[str] = []
    if getattr(user, "occupation", None) == "retired" and getattr(user, "age", 0) < 40:
        warnings.append("Occupation is 'retired' but age is under 40 — verify input.")

    # Compose a small explainability text
    reasons: list[str] = []
    try:
        bmi_val = float(user.bmi)
    except Exception:
        bmi_val = None

    if bmi_val is not None:
        if 18.5 <= bmi_val < 25:
            reasons.append("BMI is normal")
        elif bmi_val >= 30:
            reasons.append("high BMI")
        elif bmi_val >= 25:
            reasons.append("slightly elevated BMI")

    if not getattr(user, "smoker", False):
        reasons.append("non-smoker")
    else:
        reasons.append("smoker")

    if getattr(user, "age", 0) < 40:
        reasons.append("age is under 40")
    elif getattr(user, "age", 0) < 60:
        reasons.append("age is between 40 and 59")
    else:
        reasons.append("age is 60 or above")

    pred_label = str(prediction).capitalize()
    explain_text = f"{pred_label} premium because " + ", ".join(reasons) if reasons else None

    # Persist to DB
    db_record = save_prediction_result(user, prediction)

    # Add to in-memory recent log
    _RECENT.appendleft({
        "result_id": db_record.id,
        "predicted_category": prediction,
        "timestamp": datetime.utcnow().isoformat(),
        "explain_text": explain_text,
    })

    return prediction, db_record, explain_text, warnings


def get_recent_predictions():
    """Return the last few predictions kept in-memory (simple audit log)."""
    return list(_RECENT)
