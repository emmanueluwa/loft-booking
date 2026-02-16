from app.notifications import send_telegram_notification
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime

app = FastAPI()


class BookingRequest(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: str
    service_type: str
    appointment_datetime: datetime


@app.post("/bookings")
async def create_booking(booking: BookingRequest):
    """create new booking and send telegram notification"""
    try:
        formatted_time = booking.appointment_datetime.strftime(
            "%A, %d %B %Y at %I:%M %p"
        )

        await send_telegram_notification(
            customer_name=booking.customer_name,
            service_type=booking.service_type,
            appointment_datetime=formatted_time,
            customer_phone=booking.customer_phone,
            customer_email=booking.customer_email,
        )

        return {"success": True, "message": "Booking created successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create booking: {str(e)}"
        )


@app.get("/health")
async def health():
    return {"status": "healthy"}
