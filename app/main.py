from app.models import Booking
from app.schedule import LONDON_TZ, get_available_slots
from app.services import SERVICE_DURATIONS, ServiceType
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, get_db
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from app.notifications import send_telegram_notification
import uuid

app = FastAPI(title="Grooming Loft Booking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class BookingRequest(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: str
    service_type: ServiceType
    appointment_start: datetime


class BookingResponse(BaseModel):
    id: uuid.UUID
    customer_name: str
    service_type: ServiceType
    appointment_start: datetime
    appointment_end: datetime
    message: str


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/available-slots")
async def get_slots(
    date: str, service: ServiceType, db: AsyncSession = Depends(get_db)
):
    """returns available slots for given date and service"""
    try:
        requested_date = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=LONDON_TZ)

    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
        )

    # fetching existing bookings for day
    day_start = requested_date.replace(hour=0, minute=0, second=0)
    day_end = requested_date.replace(hour=23, minute=59, second=59)

    result = await db.execute(
        select(Booking).where(
            and_(
                Booking.appointment_start >= day_start,
                Booking.appointment_start <= day_end,
            )
        )
    )
    existing_bookings = result.scalars().all()

    booked_slots = [(b.appointment_start, b.appointment_end) for b in existing_bookings]

    slots = get_available_slots(requested_date, service, booked_slots)

    return {
        "date": date,
        "service": service,
        "available_slots": [s.isoformat() for s in slots],
    }


@app.post("/bookings", response_model=BookingResponse)
async def create_booking(booking: BookingRequest, db: AsyncSession = Depends(get_db)):
    """create new booking and send telegram notification"""
    try:
        service_duration = SERVICE_DURATIONS[booking.service_type]
        appointment_end = booking.appointment_start + service_duration

        # checking slot is still available
        result = await db.execute(
            select(Booking).where(
                or_(
                    and_(
                        Booking.appointment_start < appointment_end,
                        Booking.appointment_end > booking.appointment_start,
                    )
                )
            )
        )
        # get instance without tuple wrapping
        conflict = result.scalars().first()
        if conflict:
            raise HTTPException(
                status_code=409, detail="This time slot is no longer available"
            )

        # saving booking
        new_booking = Booking(
            customer_name=booking.customer_name,
            customer_email=booking.customer_email,
            customer_phone=booking.customer_phone,
            service_type=booking.service_type,
            appointment_start=booking.appointment_start,
            appointment_end=appointment_end,
        )

        db.add(new_booking)
        await db.commit()
        await db.refresh(new_booking)

        formatted_start = booking.appointment_start.astimezone(LONDON_TZ).strftime(
            "%A, %d %B %Y at %I:%M %p"
        )
        formatted_end = appointment_end.astimezone(LONDON_TZ).strftime("%I:%M %p")

        await send_telegram_notification(
            customer_name=booking.customer_name,
            service_type=booking.service_type.value,
            appointment_datetime=f"{formatted_start} - {formatted_end}",
            customer_phone=booking.customer_phone,
            customer_email=booking.customer_email,
        )

        return BookingResponse(
            id=new_booking.id,
            customer_name=new_booking.customer_name,
            service_type=new_booking.service_type,
            appointment_start=new_booking.appointment_start,
            appointment_end=new_booking.appointment_end,
            message="Booking confirmed! We will be in touch shortly to confirm your appointment",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create booking: {str(e)}"
        )
