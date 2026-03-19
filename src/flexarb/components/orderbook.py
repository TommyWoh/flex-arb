"""Represent a simple orderbook to see represent how the prices vary."""


class Supply:
    """Represent a single power supplier with its given supply and price."""

    def __init__(self, power_supply_kwh: float, price_per_kwh: float):
        self.size_kwh = power_supply_kwh
        self.price_per_kwh = price_per_kwh


class OrderBook:
    """Represent multiple suppliers."""

    def __init__(self, supplies: list[Supply]):
        self.supplies = supplies
