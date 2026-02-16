from enum import Enum
from datetime import timedelta


class ServiceType(str, Enum):
    # cats
    CAT_FULL_GROOM = "Cat Full Groom"
    CAT_MINI_GROOM = "Cat Mini Groom"

    # dogs - individual
    BATH_AND_BRUSH = "Bath & Brush"
    EMMI_PET_TEETH_CLEANING = "Emmi-pet Teeth Cleaning"
    TINY_FULL_GROOM = "Tiny Full Groom"
    SMALL_FULL_GROOM = "Small Full Groom"
    MEDIUM_FULL_GROOM = "Medium Full Groom"
    LARGE_FULL_GROOM = "Large Full Groom"
    EXTRA_LARGE_FULL_GROOM = "Extra Large Full Groom"
    HAND_STRIPPING = "Hand Stripping"

    # dogs - multiple
    TWO_DOGS_FULL_GROOM = "2 Dogs Full Groom"
    THREE_DOGS_FULL_GROOM = "3 Dogs Full Groom"
    FOUR_DOGS_FULL_GROOM = "4 Dogs Full Groom"


SERVICE_DURATIONS = {
    # cat services (+ 15min buffer)
    ServiceType.CAT_FULL_GROOM: timedelta(hours=1, minutes=30),
    ServiceType.CAT_MINI_GROOM: timedelta(hours=1),
    # dog services (+ 15min buffer)
    ServiceType.BATH_AND_BRUSH: timedelta(hours=1, minutes=15),
    ServiceType.EMMI_PET_TEETH_CLEANING: timedelta(minutes=45),
    ServiceType.TINY_FULL_GROOM: timedelta(hours=1, minutes=25),
    ServiceType.SMALL_FULL_GROOM: timedelta(hours=2),
    ServiceType.MEDIUM_FULL_GROOM: timedelta(hours=2, minutes=15),
    ServiceType.LARGE_FULL_GROOM: timedelta(hours=2, minutes=45),
    ServiceType.EXTRA_LARGE_FULL_GROOM: timedelta(hours=3, minutes=15),
    ServiceType.HAND_STRIPPING: timedelta(hours=2, minutes=15),
    # dogs - multiple (+ 15min buffer)
    ServiceType.TWO_DOGS_FULL_GROOM: timedelta(hours=3, minutes=15),
    ServiceType.THREE_DOGS_FULL_GROOM: timedelta(hours=4, minutes=45),
    ServiceType.FOUR_DOGS_FULL_GROOM: timedelta(hours=6, minutes=15),
}
