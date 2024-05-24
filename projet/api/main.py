from fastapi import FastAPI, Depends
from pydantic import BaseModel
import predict
from utils import has_access


app = FastAPI()

class Item(BaseModel):
    Descriptif: str
    Note: str
    Marque: str
    Consommation: str
    Indice_Pluie: str
    Bruit: int
    Saisonalite: str
    Type_Vehicule: str
    Runflat: str
    Largeur: int
    Hauteur: int
    Diametre: int
    Charge: int
    Vitesse: str

@app.get("/")
def read_root():
    return "Server is running."

@app.post("/predict/")
def get_prediction(item: Item, token: str = Depends(has_access)):
    prediction = predict.predict(item.dict())
    return {"prediction": prediction}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)