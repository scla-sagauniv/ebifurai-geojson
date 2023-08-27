from fastapi import APIRouter, FastAPI
from geojson import get_rondom_country_data, compare_contour
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

router = APIRouter(prefix="/geojson", tags=["article"])


class QuestionRes(BaseModel):
    NAME_JA: str

@router.get("/question", response_model=QuestionRes)
async def question():
    record = get_rondom_country_data()
    country: str = record["NAME_JA"]
    return {"NAME_JA": country}


class CompareReq(BaseModel):
    question_country: str
    choiced_country: str

class CompareRes(BaseModel):
    score: int

@router.post("/compare", response_model=CompareRes)
async def compare(req: CompareReq):
    score: int = compare_contour(req.choiced_country, req.question_country)
    return {"score": score}
    

app.include_router(router)

