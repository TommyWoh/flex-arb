"""Proof of concept of arbitrage opportunity usage between two countries.

This will only work for two countries, but gets the basic elements and structure.
Will not work for multiple connections and a port, because the sum in the flows is
missing.
Used shortcuts just to test the basic idea.
"""

from linopy import Model, Variable

from flexarb.components.country import Country
from flexarb.components.orderbook import OrderBook, Supply

if __name__ == "__main__":
    model = Model()

    order_book_germany = OrderBook(
        supplies=[
            Supply(power_supply_kwh=400, price_per_kwh=0.005),
            Supply(power_supply_kwh=1000, price_per_kwh=0.01),
            Supply(power_supply_kwh=100, price_per_kwh=0.02),
            Supply(power_supply_kwh=5000, price_per_kwh=0.06),
        ]
    )

    germany = Country(
        model=model,
        name="Germany",
        power_demand_kwh=1500,
        order_book=order_book_germany,
    )

    """
    germany_austria_port = germany.add_port(
        name="connection_from_germany_to_austria",
        capacity_import_kwh=100,
        capacity_export_kwh=200,
    )
    """

    order_book_austria = OrderBook(
        supplies=[
            Supply(power_supply_kwh=100, price_per_kwh=0.01),
            Supply(power_supply_kwh=5000, price_per_kwh=0.02),
            Supply(power_supply_kwh=6000, price_per_kwh=0.05),
            Supply(power_supply_kwh=5000, price_per_kwh=0.1),
        ]
    )

    austria = Country(
        model=model,
        name="Austria",
        power_demand_kwh=900,
        order_book=order_book_austria,
    )

    """
    austria_germany_port = austria.add_port(
        name="connection_from_austria_to_germany",
        capacity_import_kwh=900,
        capacity_export_kwh=1200,
    )

    all_countries: list[Country] = [
        germany,
        austria,
    ]

    link_between_germany_and_austria = Link(
        model=model,
        name="germany_to_austria",
        source_object=germany,
        source_port=germany_austria_port,
        target_object=austria,
        target_port=austria_germany_port,
        price_transport_per_kwh=0.01,
        available_kwh=50000,
    )
    """
    germany.add_variables()
    austria.add_variables()
    germany.add_constraints()
    austria.add_constraints()

    """
    all_links = [
        link_between_germany_and_austria,
    ]
    """
    all_objects = [germany, austria]

    all_costs = [obj.get_cost() for obj in all_objects]

    model.add_objective(
        expr=sum(all_costs),  # ty:ignore[invalid-argument-type]
        sense="max",
    )
    model.solve(solver_name="highs")

    all_vars: list[Variable] = []
    for country in all_objects:
        print(country.name, country.power_demand_kwh)
        all_vars.extend(list(country.ports_vars.values()))
        all_vars.extend(list(country.order_book_vars.values()))

    for var in all_vars:
        print(var, var.solution)
