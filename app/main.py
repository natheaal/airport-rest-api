from fastapi import FastAPI, HTTPException, Depends, Query, Header
from pydantic import BaseModel, Field
from typing import List, Optional
import math

app = FastAPI(title="Gestione Aeroporti API")

class AeroportoBase(BaseModel):
    codice: str = Field(..., min_length=3, max_length=3, description="Codice IATA di 3 caratteri")
    citta: str = Field(..., min_length=1, description="Nome della città obbligatorio")

class Aeroporto(AeroportoBase):
    id: int

class PaginatedAeroporti(BaseModel):
    page: int
    size: int
    total_pages: int
    data: List[Aeroporto]

db_aeroporti = [
    {"id": 1, "codice": "MXP", "citta": "Milano"},
    {"id": 2, "codice": "FCO", "citta": "Roma"},
    {"id": 3, "codice": "BGY", "citta": "Bergamo"},
]
id_counter = 4

def verify_token(authorization: str = Header(...)):
    if authorization != "Bearer mio-token-segreto":
        raise HTTPException(status_code=401, detail="Non autorizzato")
    return authorization


@app.get("/aeroporti", response_model=PaginatedAeroporti)
def get_aeroporti(page: int = Query(1, ge=1), size: int = Query(5, ge=1)):
    start = (page - 1) * size
    end = start + size
    data = db_aeroporti[start:end]
    total_pages = math.ceil(len(db_aeroporti) / size)
    
    return {
        "page": page,
        "size": size,
        "total_pages": total_pages,
        "data": data
    }

@app.get("/aeroporti/{id}", response_model=AeroportoBase)
def get_aeroporto(id: int):
    for a in db_aeroporti:
        if a["id"] == id:
            return a
    raise HTTPException(status_code=404, detail="Aeroporto non trovato")

@app.post("/aeroporti", response_model=Aeroporto, status_code=201)
def create_aeroporto(a: AeroportoBase, token: str = Depends(verify_token)):
    global id_counter
    new_aeroporto = {"id": id_counter, **a.dict()}
    db_aeroporti.append(new_aeroporto)
    id_counter += 1
    return new_aeroporto

@app.delete("/aeroporto/{id}", status_code=204) # Nota: path richiesto dalla consegna
def delete_aeroporto(id: int, token: str = Depends(verify_token)):
    global db_aeroporti
    initial_len = len(db_aeroporti)
    db_aeroporti = [a for a in db_aeroporti if a["id"] != id]
    if len(db_aeroporti) == initial_len:
        raise HTTPException(status_code=404, detail="Aeroporto non trovato")
    return None


























