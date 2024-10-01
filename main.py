from fastapi import Depends, FastAPI, HTTPException
from models import Base
from sqlalchemy.orm import Session

from . import crud, models, schemas
from database import SessionLocal, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/subject/all", response_model=list[schemas.Subjects])
def read_subjects(db: Session=Depends(get_db)):
    subjects=crud.get_subjects(db)
    return subjects

@app.get("/level/all", response_model=list[schemas.Levels])
def read_levels(db: Session=Depends(get_db)):
    levels=crud.get_levels(db)
    return levels

@app.get("/disability_type/all", response_model=list[schemas.DisabilityTypes])
def read_disability_types(db: Session=Depends(get_db)):
    disability_types=crud.get_disability_types(db)
    return disability_types

@app.get("/facility", response_model=list[schemas.Facilities])
def read_facilities(subject_ids: list[int], level_ids:list[int], disability_type_ids:list[int], db: Session=Depends(get_db)):
    facilities=crud.get_facilities(db,subject_ids=subject_ids, level_ids=level_ids, disability_type_ids=disability_type_ids)
    return facilities

# @app.get("/review")
# def read_reviews(facility_id: int):
#     reviews=session.query(ReviewTable).filter(ReviewTable.id == facility_id )
#     return reviews

# @app.post("/review") 
# def create_reviews():
#     review = ReviewTable()
#     review.
#     return {"message": "Hello World"}

@app.post("/club", response_model=schemas.Clubs)
def create_clubs(club: schemas.ClubCreate, db: Session = Depends(get_db)):
    new_club = models.Clubs(
        creator_id=club.creator_id,
        facility_id=club.facility_id,
        min_capacity=club.min_capacity,
        max_capacity=club.max_capacity,
        time=club.time,
        repeat=club.repeat,
        start_period=club.start_period,
        end_period=club.end_period,
        fee=club.fee,
        img_url=club.img_url,
        title=club.title,
        content=club.content
    )
    db.add(new_club)
    db.commit()
    db.refresh(new_club) 
    return new_club