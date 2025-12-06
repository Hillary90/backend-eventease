from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import get_current_user

from models.event import Event
from schemas.event import EventCreate, EventOut, EventUpdate

router = APIRouter()


# CREATE EVENT
@router.post("/create", response_model=EventOut)
def create_event(event: EventCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    new_event = Event(
        title=event.title,
        description=event.description,
        date=event.date,
        organizer_id=current_user["id"]
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


# GETting  ALL EVENTS
@router.get("/all", response_model=list[EventOut])
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()


#to  get EVENT BY ID
@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(404, "Event not found")

    return event


# UPDATE EVENT
@router.put("/update/{event_id}", response_model=EventOut)
def update_event(event_id: int, update: EventUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(404, "Event not found")

    if event.organizer_id != current_user["id"]:
        raise HTTPException(403, "Not authorized")

    event.title = update.title
    event.description = update.description
    event.date = update.date

    db.commit()
    db.refresh(event)
    return event

# DELETE EVENT
@router.delete("/delete/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(404, "Event not found")

    if event.organizer_id != current_user["id"]:
        raise HTTPException(403, "Not authorized")

    db.delete(event)
    db.commit()
    return {"message": "Event deleted successfully"}

# DELETE EVENT
@router.delete("/delete/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(404, "Event not found")

    if event.organizer_id != current_user["id"]:
        raise HTTPException(403, "Not authorized")

    db.delete(event)
    db.commit()

    return {"message": "Event deleted successfully"}
