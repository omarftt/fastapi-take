from fastapi import APIRouter, HTTPException, status
from models import Prediction_Input
from models import Prediction_Output
import numpy as np
import pickle
import pandas as pd
from utils.helper import pre_processing, apply_prediction

router = APIRouter()

# Example in-memory storage
preds = []

# Cargar el modelo y el scaler desde los archivos pickle
with open("model_real.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)


@router.post("/taken/predict",status_code=status.HTTP_201_CREATED,response_model=Prediction_Output)
def predict_pulsar_star(item: Prediction_Input):
    # Obtener los valores de las características desde el objeto item
    print(item)
    print(type(item))
    values = [
        int(item.order_id),
        int(item.store_id),
        float(item.to_user_distance),
        float(item.to_user_elevation),
        int(item.total_earning),
        str(item.created_at)
    ]

    # Realizar el preprocesamiento
    X = pre_processing(values)
    
    # Realizar la predicción
    prediction = apply_prediction(X,model)
    print('prediction', prediction)

    prediction_dict = {"order_id": int(item.order_id),
                        "store_id" : int(item.store_id),
                        "to_user_distance":float(item.to_user_distance),
                        "to_user_elevation":float(item.to_user_elevation),
                        "total_earning":int(item.total_earning),
                        "created_at":str(item.created_at),
                        "pred_taken": bool(prediction)
                        }
    preds.append(prediction_dict)
    
    # Devolver el resultado de la predicción como respuesta
    return prediction_dict



# GET / - Retrieve predictions
@router.get("/taken/all")
def get_preds():
    print(preds)
    return preds