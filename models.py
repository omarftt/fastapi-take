from pydantic import BaseModel


class Prediction_Input(BaseModel):
    order_id: int
    store_id: int
    to_user_distance: float
    to_user_elevation: float
    total_earning: int
    created_at: str

class Prediction_Output(BaseModel):
    order_id: int
    store_id: int
    to_user_distance: float
    to_user_elevation: float
    total_earning: int
    created_at: str
    pred_taken: bool



