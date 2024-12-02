from dataclasses import dataclass


@dataclass
class Expense:
    timestamp: str
    vehicle: str
    amount: str
    quantity: float
    odometer_reading: float
    date: str
    is_refuel_indicator_on: bool