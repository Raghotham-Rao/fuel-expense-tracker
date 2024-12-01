from dataclasses import dataclass


@dataclass
class Expense:
    timestamp: str
    vehicle: str
    amount: str
    quantity: float
    odometer_reading: float
    date: str