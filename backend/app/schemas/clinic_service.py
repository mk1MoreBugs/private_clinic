from app.schemas.base_item import BaseItem


class ClinicService(BaseItem):
    price: int
    available: bool = True
