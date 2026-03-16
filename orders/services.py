from decimal import Decimal


def calculate_transport_cost(order):
    vehicle = order.safe_vehicle
    if not vehicle or order.fuel_price is None:
        return Decimal("0")
    distance = Decimal(order.distance_km)
    liters_used = (distance / Decimal("100")) * vehicle.fuel_consumption
    return liters_used * order.fuel_price


def calculate_profit(order):
    if order.price is None:
        return Decimal("0")
    if not order.safe_vehicle or order.fuel_price is None:
        return Decimal("0")
    return order.price - calculate_transport_cost(order)
