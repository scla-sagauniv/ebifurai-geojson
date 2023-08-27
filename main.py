from fastapi import APIRouter, FastAPI
from geojson_logic import get_rondom_country_data, compare_contour, get_country_polygon
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

router = APIRouter(prefix="/geojson", tags=["article"])


class QuestionRes(BaseModel):
    NAME_JA: str
    data: str

@router.get("/question", response_model=QuestionRes)
async def question():
    record = get_rondom_country_data()
    country: str = record["NAME_JA"]
    geojsonData = get_country_polygon(country)
    return {"NAME_JA": country, "data": geojsonData}


class CompareReq(BaseModel):
    question_country: str
    choiced_country: str

class CompareRes(BaseModel):
    score: int
    choiced_country_geojson: str

@router.post("/compare", response_model=CompareRes)
async def compare(req: CompareReq):
    score: int = compare_contour(req.choiced_country, req.question_country)
    geojsonData = get_country_polygon(req.choiced_country)
    return {"score": score, "choiced_country_geojson": geojsonData}
    

app.include_router(router)

