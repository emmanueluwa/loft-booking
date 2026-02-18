from datetime import datetime, timezone
from app.services import ServiceType
from sqlalchemy import String, Enum as SQLEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, server_default=None
    )

    customer_name: Mapped[str] = mapped_column(String(100))
    customer_email: Mapped[str] = mapped_column(String(255))
    customer_phone: Mapped[str] = mapped_column(String(20))

    service_type: Mapped[ServiceType] = mapped_column(SQLEnum(ServiceType))
    appointment_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), unique=True
    )
    appointment_end: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
