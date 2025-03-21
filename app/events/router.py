from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.events import models as event_models
from app.events import schemas as event_schemas
from app.users import schemas as user_schemas
from app.users.auth import get_current_user
from datetime import datetime, date
import pytz


router = APIRouter()


lagos_tz = pytz.timezone("Africa/Lagos")


# Create Event
@router.post("/", response_model=event_schemas.EventResponse)
def create_event(
    event: event_schemas.EventCreate, 
    db: Session = Depends(get_db), 
    current_user: user_schemas.UserDisplaySchema = Depends(get_current_user),
):
    # Convert date to datetime if needed
    def ensure_datetime(dt):
        if isinstance(dt, date) and not isinstance(dt, datetime):
            return datetime.combine(dt, datetime.min.time())  # Convert date to datetime
        return dt

    try:
        start_datetime = ensure_datetime(event.start_datetime)
        end_datetime = ensure_datetime(event.end_datetime)

        # Convert to timezone-aware datetime if missing tzinfo
        if start_datetime.tzinfo is None:
            start_datetime = lagos_tz.localize(start_datetime)

        if end_datetime.tzinfo is None:
            end_datetime = lagos_tz.localize(end_datetime)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid datetime format: {str(e)}")

    # Check if an event already exists on the requested start date
    existing_event = db.query(event_models.Event).filter(
        event_models.Event.start_datetime == start_datetime
    ).first()

    if existing_event:
        raise HTTPException(
            status_code=400,
            detail=f"An event has already been booked on {start_datetime}. Please choose a different date."
        )

    # Proceed with creating the event if no conflict exists
    db_event = event_models.Event(
        organizer=event.organizer,
        title=event.title,
        description=event.description,
        start_datetime=start_datetime,   # ✅ Ensured datetime format
        end_datetime=end_datetime,       # ✅ Ensured datetime format
        event_amount=event.event_amount,
        caution_fee=event.caution_fee,
        location=event.location,
        phone_number=event.phone_number,
        address=event.address,
        payment_status=event.payment_status or "active",
        created_by=current_user.username
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event



@router.get("/", response_model=List[event_schemas.EventResponse])
def list_events(
    db: Session = Depends(get_db),
    current_user: user_schemas.UserDisplaySchema = Depends(get_current_user),
    start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format"),
):
    query = db.query(event_models.Event)

    if start_date:
        try:
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(event_models.Event.start_datetime >= start_date_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD.")

    if end_date:
        try:
            # Extend end date to cover the whole day (23:59:59)
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
            query = query.filter(event_models.Event.end_datetime <= end_date_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format. Use YYYY-MM-DD.")

    events = query.order_by(event_models.Event.start_datetime).all()
    return events



# Get Event by ID
@router.get("/{event_id}", response_model=event_schemas.EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(event_models.Event).filter(event_models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


# Update Event (Only Creator or Admin)
@router.put("/{event_id}", response_model=dict)
def update_event(
    event_id: int,
    event: event_schemas.EventCreate, 
    db: Session = Depends(get_db), 
    current_user: user_schemas.UserDisplaySchema = Depends(get_current_user),
):
    db_event = db.query(event_models.Event).filter(event_models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    if db_event.created_by != current_user.username and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only event creators or admins can update events")

    for field, value in event.dict(exclude_unset=True).items():
        setattr(db_event, field, value)

    db.commit()
    db.refresh(db_event)

    return {"message": "Event updated successfully"}


# Cancel Event (Only Admin, With Cancellation Reason)
@router.put("/{event_id}/cancel", response_model=dict)
def cancel_event(
    event_id: int, 
    cancellation_reason: str,
    db: Session = Depends(get_db), 
    current_user: user_schemas.UserDisplaySchema = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can cancel events")

    db_event = db.query(event_models.Event).filter(event_models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    db_event.payment_status = "cancelled"
    db_event.cancellation_reason = cancellation_reason  # Store reason in the column

    db.commit()
    db.refresh(db_event)  # Refresh the event to reflect changes in the session
    return {"message": "Event cancellation successful", "cancellation_reason": cancellation_reason}
