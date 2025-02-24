from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.database import get_db
from app.events import models as event_models
from app.eventpayment import models as eventpayment_models, schemas as eventpayment_schemas
from app.users import schemas as user_schemas
from app.users.auth import get_current_user
from typing import List
from sqlalchemy import and_
from datetime import datetime, timedelta, date
from sqlalchemy.sql import  case
from sqlalchemy.orm import aliased
from typing import Optional 
from loguru import logger




router = APIRouter()



@router.post("/", response_model=eventpayment_schemas.EventPaymentResponse)
def create_event_payment(
    payment_data: eventpayment_schemas.EventPaymentCreate,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserDisplaySchema = Depends(get_current_user),
):
    # Fetch the event using event_id
    event = db.query(event_models.Event).filter(event_models.Event.id == payment_data.event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # 🚨 Check if the event is canceled before proceeding with payment
    if event.payment_status.lower() == "cancelled":
        raise HTTPException(
            status_code=400,
            detail=f"Payment cannot be processed because Event ID {payment_data.event_id} is cancelled."
        )

    # Fetch all previous payments for this event, excluding voided payments
    total_paid = db.query(func.coalesce(func.sum(eventpayment_models.EventPayment.amount_paid), 0)).filter(
        eventpayment_models.EventPayment.event_id == payment_data.event_id,
        eventpayment_models.EventPayment.payment_status != "voided"  # Exclude voided payments
    ).scalar()

    total_discount = db.query(func.coalesce(func.sum(eventpayment_models.EventPayment.discount_allowed), 0)).filter(
        eventpayment_models.EventPayment.event_id == payment_data.event_id,
        eventpayment_models.EventPayment.payment_status != "voided"  # Exclude voided discounts
    ).scalar()

    # Compute new total payment and discount including the new payment
    new_total_paid = total_paid + payment_data.amount_paid
    new_total_discount = total_discount + payment_data.discount_allowed

    # Compute balance due (excluding caution fee)
    balance_due = event.event_amount - (new_total_paid + new_total_discount)

    # Determine payment status
    if balance_due > 0:
        payment_status = "incomplete"
    elif balance_due == 0:
        payment_status = "complete"
    else:
        payment_status = "excess"  # Payment exceeded the event amount

    # Proceed to create the payment since the event is active
    new_payment = eventpayment_models.EventPayment(
        event_id=payment_data.event_id,
        organiser=payment_data.organiser,
        event_amount=event.event_amount,
        amount_paid=payment_data.amount_paid,
        discount_allowed=payment_data.discount_allowed,
        balance_due=balance_due,
        payment_method=payment_data.payment_method,
        payment_status=payment_status,  # Automatically set status
        created_by=current_user.username
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment



@router.get("/", response_model=List[eventpayment_schemas.EventPaymentResponse])
def list_event_payments(
    start_date: str = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(None, description="End date in YYYY-MM-DD format"),
    db: Session = Depends(get_db),
    current_user: user_schemas.UserDisplaySchema = Depends(get_current_user),
):
    query = db.query(eventpayment_models.EventPayment)

    # Apply date filter if both start_date and end_date are provided
    if start_date and end_date:
        try:
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
            # Extending end_date to include the whole day (23:59:59)
            
            query = query.filter(
                and_(
                    eventpayment_models.EventPayment.payment_date >= start_date_dt,
                    eventpayment_models.EventPayment.payment_date <= end_date_dt,
                )
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    payments = query.all()

    # Process and format the response
    formatted_payments = []
    for payment in payments:
        event = db.query(event_models.Event).filter(
            event_models.Event.id == payment.event_id
        ).first()

        if not event:
            continue  # Skip if event is not found

        # Compute balance_due correctly
        total_paid = (
            db.query(func.sum(eventpayment_models.EventPayment.amount_paid))
            .filter(eventpayment_models.EventPayment.event_id == payment.event_id)
            .scalar()
        ) or 0

        total_discount = (
            db.query(func.sum(eventpayment_models.EventPayment.discount_allowed))
            .filter(eventpayment_models.EventPayment.event_id == payment.event_id)
            .scalar()
        ) or 0

        balance_due = event.event_amount - (total_paid + total_discount)

        # Construct response object
        formatted_payments.append({
            "id": payment.id,  # ✅ Ensure 'id' is included
            "event_id": payment.event_id,
            "organiser": payment.organiser,
            "event_amount": event.event_amount,
            "amount_paid": payment.amount_paid,
            "discount_allowed": payment.discount_allowed,
            "balance_due": balance_due,
            "payment_method": payment.payment_method,
            "payment_status": payment.payment_status,
            "payment_date": payment.payment_date,  # ✅ Ensure 'payment_date' is included
            "created_by": payment.created_by,
        })

    return formatted_payments

@router.get("/status", response_model=List[eventpayment_schemas.EventPaymentResponse])
def list_event_payments_by_status(
    status: Optional[str] = Query(None, description="Payment status to filter by (pending, complete, incomplete, voided)"),
    start_date: Optional[date] = Query(None, description="Filter by payment date (start) in format yyyy-mm-dd"),
    end_date: Optional[date] = Query(None, description="Filter by payment date (end) in format yyyy-mm-dd"),
    db: Session = Depends(get_db),
    current_user: user_schemas.UserDisplaySchema = Depends(get_current_user),
):
    query = db.query(eventpayment_models.EventPayment)

    if status:
        valid_statuses = {"pending", "complete", "incomplete", "voided"}
        if status.lower() not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Choose from: {valid_statuses}")
        query = query.filter(eventpayment_models.EventPayment.payment_status == status)

    if start_date:
        query = query.filter(eventpayment_models.EventPayment.payment_date >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        query = query.filter(eventpayment_models.EventPayment.payment_date <= datetime.combine(end_date, datetime.max.time()))

    payments = query.all()
    
    if not payments:
        return []  # ✅ Return an empty list if no records are found

    return payments  # ✅ Return list as expected


@router.put("/void/{payment_id}/", response_model=dict)
def void_event_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserDisplaySchema = Depends(get_current_user),
):
    # Only admins can void payments
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    try:
        # Retrieve the payment record by ID
        payment = db.query(eventpayment_models.EventPayment).filter(
            eventpayment_models.EventPayment.id == payment_id
        ).first()

        if not payment:
            logger.warning(f"Event Payment with ID {payment_id} does not exist.")
            raise HTTPException(status_code=404, detail=f"Payment with ID {payment_id} not found.")

        # Check if payment has already been voided
        if payment.payment_status == "voided":
            raise HTTPException(status_code=400, detail="Payment has already been voided")

        # Retrieve the associated event
        event = db.query(event_models.Event).filter(event_models.Event.id == payment.event_id).first()

        if not event:
            logger.warning(f"Event with ID {payment.event_id} not found.")
            raise HTTPException(status_code=404, detail="Associated event not found")

        # Store the event total cost
        event_total_cost = event.event_amount

        # Mark the payment as voided
        payment.payment_status = "voided"

        # Calculate total valid payments (excluding voided ones)
        total_valid_payments = db.query(
            func.coalesce(func.sum(eventpayment_models.EventPayment.amount_paid), 0)
        ).filter(
            eventpayment_models.EventPayment.event_id == event.id,
            eventpayment_models.EventPayment.payment_status != "voided"  # Exclude voided payments
        ).scalar()

        # Update the event's balance due
        event.balance_due = event_total_cost - total_valid_payments

        # Update event's payment status based on the new balance
        event.payment_status = "pending" if event.balance_due > 0 else "paid"

        # Commit changes
        db.commit()

        logger.info(f"Event Payment with ID {payment_id} marked as void. Event balance recalculated.")

        return {
            "message": f"Event Payment with ID {payment_id} has been voided. Event balance updated.",
            "payment_details": {
                "payment_id": payment.id,
                "status": payment.payment_status,
            },
            "event_details": {
                "event_id": event.id,
                "balance_due": event.balance_due,
                "payment_status": event.payment_status,
            },
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        logger.error(f"Error voiding event payment: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while voiding the event payment: {str(e)}"
        )






@router.get("/{payment_id}")
def get_event_payment_by_id(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserDisplaySchema = Depends(get_current_user),
):
    # Fetch the payment record
    payment = db.query(eventpayment_models.EventPayment).filter(
        eventpayment_models.EventPayment.id == payment_id
    ).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    # Fetch related event details
    event = db.query(event_models.Event).filter(
        event_models.Event.id == payment.event_id
    ).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Compute balance_due correctly
    total_paid = (
        db.query(func.sum(eventpayment_models.EventPayment.amount_paid))
        .filter(eventpayment_models.EventPayment.event_id == payment.event_id)
        .scalar()
    ) or 0

    total_discount = (
        db.query(func.sum(eventpayment_models.EventPayment.discount_allowed))
        .filter(eventpayment_models.EventPayment.event_id == payment.event_id)
        .scalar()
    ) or 0

    balance_due = event.event_amount - (total_paid + total_discount)

    # Construct response including required fields
    formatted_payment = {
        "id": payment.id,  # ✅ Add the missing 'id' field
        "event_id": payment.event_id,
        "organiser": payment.organiser,
        "event_amount": event.event_amount,
        "amount_paid": payment.amount_paid,
        "discount_allowed": payment.discount_allowed,
        "balance_due": balance_due,
        "payment_method": payment.payment_method,
        "payment_status": payment.payment_status,
        "payment_date": payment.payment_date,  # ✅ Add the missing 'payment_date' field
        "created_by": payment.created_by,
    }

    return formatted_payment








