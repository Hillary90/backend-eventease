from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.core.security import get_current_user

from models.booking import Booking
from models.event import Event
from models.user import User
from schemas.booking import BookingResponse, BookingCreate, BookingCancel, BookingWithUser, BookingWithEvent
from schemas.event import EventCreate, EventOut, EventUpdate

router = APIRouter()


@router.post("/rsvp", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def rsvp_to_event(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    User RSVPs to an event
    """
    # Check if event exists
    event = db.query(Event).filter(Event.id == booking.event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check if user already has a booking for this event (prevent double booking)
    existing_booking = db.query(Booking).filter(
        Booking.user_id == current_user.id,
        Booking.event_id == booking.event_id
    ).first()
    
    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already RSVP'd to this event"
        )
    
    # Create new booking
    new_booking = Booking(
        user_id=current_user.id,
        event_id=booking.event_id
    )
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    return new_booking


@router.delete("/cancel", status_code=status.HTTP_200_OK)
def cancel_rsvp(
    booking: BookingCancel,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    User cancels their RSVP for an event
    """
    # Find the booking
    existing_booking = db.query(Booking).filter(
        Booking.user_id == current_user.id,
        Booking.event_id == booking.event_id
    ).first()
    
    if not existing_booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RSVP not found"
        )
    
    # Delete the booking
    db.delete(existing_booking)
    db.commit()
    
    return {"message": "RSVP cancelled successfully"}


@router.get("/event/{event_id}", response_model=List[BookingWithUser])
def get_event_attendees(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get list of attendees for an event (organizers can see attendee list)
    """
    # Check if event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
   
    
    # Get all bookings for this event
    bookings = db.query(Booking).filter(Booking.event_id == event_id).all()
    
    # Format response with user details
    result = []
    for booking in bookings:
        result.append({
            "id": booking.id,
            "user_id": booking.user_id,
            "created_at": booking.created_at,
            "user": {
                "id": booking.user.id,
                "name": booking.user.name,
                "email": booking.user.email
            }
        })
    
    return result


@router.get("/me", response_model=List[BookingWithEvent])
def get_my_rsvps(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all RSVPs for the current user
    """
    # Get all bookings for current user
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all()
    
    # Format response with event details
    result = []
    for booking in bookings:
        result.append({
            "id": booking.id,
            "event_id": booking.event_id,
            "created_at": booking.created_at,
            "event": {
                "id": booking.event.id,
                "title": booking.event.title,
                "description": booking.event.description,
                "date": booking.event.date,
                "location": booking.event.location,
                "organizer_id": booking.event.organizer_id
            }
        })
    
    return result
