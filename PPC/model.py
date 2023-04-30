from dataclasses import dataclass


@dataclass
class CSVRow:
    provider: str
    vendor_code: str
    name_detail: str
    quantity: str
    party: str
    price: str
    manufacturer: str

    def to_list(self) -> list:
        return [self.vendor_code, self.name_detail, self.quantity, self.party, self.price, self.manufacturer]

    def formatted_price(self) -> float:
        price = self.price.replace(',', '.').replace('\xa0', '').replace(' ', '')
        return float(price)
