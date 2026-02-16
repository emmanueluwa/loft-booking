from telegram import Bot
from app.config import settings
import asyncio


async def send_telegram_notification(
    customer_name: str,
    service_type: str,
    appointment_datetime: str,
    customer_phone: str,
    customer_email: str,
) -> None:
    """Send booking notification via Telegram"""
    bot = Bot(token=settings.telegram_bot_token)

    message = f"""
    *New Booking*

*Customer:* {customer_name}
*Service:* {service_type}
*Date/Time:* {appointment_datetime}
*Phone:* {customer_phone}
*Email* {customer_email}
    
    """

    await bot.send_message(
        chat_id=settings.telegram_chat_id, text=message, parse_mode="Markdown"
    )
