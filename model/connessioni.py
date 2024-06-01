from dataclasses import dataclass
from model.retailers import Retailers
@dataclass
class Connessioni:
    Retailer1: Retailers
    Retailer2: Retailers
    peso: int

    def __str__(self):
        return f"{self.Retailer1.Retailer_code} - {self.Retailer2.Retailer_code} - {self.peso}"
