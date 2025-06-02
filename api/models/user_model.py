from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    israel_id: str
    name: str
    phone_number: str
    address: str
