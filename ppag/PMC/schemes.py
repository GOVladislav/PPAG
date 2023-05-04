from dataclasses import dataclass


@dataclass
class CSVRow:
    vendor_code: str
    name_detail: str
    quantity: int
    party: int
    price: int
    manufacturer: str

    def to_tuple(self) -> tuple:
        return (self.vendor_code, self.name_detail, self.quantity, self.party, self.price, self.manufacturer)
