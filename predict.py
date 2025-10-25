import pickle
import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

class Client(BaseModel):
    lead_source: str
    number_of_courses_viewed: int
    annual_income: float

class PredictResponse(BaseModel):
    convert_prob: float

app = FastAPI(title="customer-convert-prediction")

with open('pipeline_v1.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)


def predict_single(client):
    result = pipeline.predict_proba(client)[0, 1]
    return float(result)


@app.post("/predict")
def predict(client: Client) -> PredictResponse:
    prob = predict_single(client.dict())

    return PredictResponse(
        convert_prob=prob
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)