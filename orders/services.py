from decimal import Decimal


def calculate_transport_cost(order):
    distance = Decimal(order.distance_km)
    liters_used = (distance / Decimal("100")) * order.vehicle.fuel_consumption
    return liters_used * order.fuel_price


def calculate_profit(order):
    return order.price - calculate_transport_cost(order)
