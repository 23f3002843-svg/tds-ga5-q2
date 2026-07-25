from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class ProrationRequest(BaseModel):
    old_price: float
    new_price: float
    days_remaining: float
    days_in_actual_month: float
    spec: str


@app.get("/")
def home():
    return {"message": "Proration API is running. Use POST /charge"}


@app.post("/charge")
def calculate_charge(request: ProrationRequest):
    old_price = request.old_price
    new_price = request.new_price
    days_remaining = request.days_remaining
    days_in_actual_month = request.days_in_actual_month
    spec = request.spec

    difference = new_price - old_price

    if spec == "v1":
        charge = difference * (days_remaining / 30)

    elif spec == "v2":
        if days_in_actual_month == 0:
            raise HTTPException(status_code=400, detail="days_in_actual_month cannot be zero")

        charge = difference * (days_remaining / days_in_actual_month)

    else:
        raise HTTPException(status_code=400, detail="spec must be either v1 or v2")

    return {"charge": charge}
