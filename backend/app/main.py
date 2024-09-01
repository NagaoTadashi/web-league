from fastapi import FastAPI, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Match
@app.get("/matches/", response_model=list[schemas.Match])
def get_matches(db: Session = Depends(get_db)):
    matches = crud.get_matches(db)
    return matches


@app.post("/match/", response_model=schemas.Match)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    return crud.create_match(db=db, match=match)


# Player
@app.get("/players/", response_model=list[schemas.Player])
def get_players(db: Session = Depends(get_db)):
    players = crud.get_players(db)
    return players


@app.post("/player/", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    return crud.create_player(db=db, player=player)


@app.put("/player/{player_id}", response_model=schemas.Player)
def update_player(
    player_id: int, player_update: schemas.PlayerUpdate, db: Session = Depends(get_db)
):
    updated_player = crud.update_player(
        db=db, player_id=player_id, player_update=player_update
    )
    if update_player is None:
        raise HTTPException(status_code=404, detail="選手情報が見つかりません")
    return updated_player


@app.delete("/player/{player_id}", response_model=schemas.Player)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    deleted_player = crud.delete_player(db=db, player_id=player_id)
    if deleted_player is None:
        raise HTTPException(status_code=404, detail="選手情報が見つかりません")
    return deleted_player
