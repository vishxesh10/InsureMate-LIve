from fastapi import APIRouter
from insuremate.db.database import get_all_results, get_results_by_city, get_results_by_category
from insuremate.services.predict import get_recent_predictions

router = APIRouter()


def _format_results(results):
    return [{**r.__dict__, "created_at": r.created_at.isoformat()} for r in results]


@router.get("/results")
def results():
    res = get_all_results()
    return {"total_results": len(res), "results": _format_results(res)}


@router.get("/results/city/{city}")
def results_city(city: str):
    res = get_results_by_city(city)
    return {"city": city, "total_results": len(res), "results": _format_results(res)}


@router.get("/results/category/{category}")
def results_category(category: str):
    res = get_results_by_category(category)
    return {"category": category, "total_results": len(res), "results": _format_results(res)}


@router.get("/results/recent")
def results_recent():
    res = get_recent_predictions()
    return {"total_results": len(res), "results": res}
