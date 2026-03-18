"""Proof of concept of arbitrage opportunity usage between two countries.

This will only work for two countries, but gets the basic elements and structure.
Will not work for multiple connections and a port, because the sum in the flows is
missing.
Used shortcuts just to test the basic idea.
"""

from linopy import LinearExpression, Model, Variable


class Port:
    """Represent a single port where a link can be added."""

    def __init__(self, model: Model, name: str, capacity_kwh: float):
        self.model = model
        self.name = name
        self.capacity_kwh = capacity_kwh
        self.var_used_capacity_kwh = self.add_variables()

    def __str__(self) -> str:
        return f"Port: {self.name}"

    def __repr__(self) -> str:
        return self.__str__()

    def add_variables(self) -> Variable:
        return self.model.add_variables(
            lower=0, upper=self.capacity_kwh, name=f"{self.__str__()}_used_capacity_kwh"
        )


class Country:
    """Represent a single country."""

    def __init__(
        self,
        model: Model,
        name: str,
        price_buy_per_kwh: float,
        price_sell_per_kwh: float,
        capacity_export_kwh: float,
        capacity_import_kwh: float,
    ):
        """Setup the Country"""
        self.model = model
        self.name = name
        self.price_buy_per_kwh = price_buy_per_kwh
        self.price_sell_per_kwh = price_sell_per_kwh
        self.capacity_export_kwh = capacity_export_kwh
        self.capacity_import_kwh = capacity_import_kwh

        self.port_import = Port(
            model=model,
            name=f"{self.__str__()}_import",
            capacity_kwh=self.capacity_import_kwh,
        )
        self.port_export = Port(
            model=model,
            name=f"{self.__str__()}_export",
            capacity_kwh=self.capacity_export_kwh,
        )
        self.var_buy_kwh, self.var_sell_kwh = self.add_variables()
        self.add_constraints()

    def __str__(self) -> str:
        return f"Country: {self.name}"

    def __repr__(self) -> str:
        return self.__str__()

    def add_variables(self) -> tuple[Variable, Variable]:
        var_buy_kwh = self.model.add_variables(
            lower=0, upper=self.capacity_import_kwh, name=f"{self.__str__()}_buy_kwh"
        )
        var_sell_kwh = self.model.add_variables(
            lower=0, upper=self.capacity_export_kwh, name=f"{self.__str__()}_sell_kwh"
        )
        return var_buy_kwh, var_sell_kwh

    def add_constraints(self):
        # energy which is sold needs to flow into the export port
        self.model.add_constraints(
            self.var_sell_kwh == self.port_export.var_used_capacity_kwh
        )
        # energy which is bought needs to flow into the import port
        self.model.add_constraints(
            self.var_buy_kwh == self.port_import.var_used_capacity_kwh
        )

    def get_cost(self) -> LinearExpression:
        return (
            -1 * self.price_sell_per_kwh * self.var_sell_kwh
            + self.price_buy_per_kwh * self.var_buy_kwh
        )


class Link:
    """Represent a link between two countries with a given direction."""

    def __init__(
        self,
        model: Model,
        name: str,
        source_object: Country,
        source_port: Port,
        target_object: Country,
        target_port: Port,
        price_transport_per_kwh: float,
        available_kwh: float,
    ):
        self.model = model
        self.name = name
        self.source_object = source_object
        self.source_port = source_port
        self.target_object = target_object
        self.target_port = target_port
        self.price_transport_per_kwh = price_transport_per_kwh
        self.available_kwh = available_kwh

        self.var_transport_kwh = self.add_variables()
        self.add_constraints()

    def __str__(self) -> str:
        return f"Link from {self.source_object.name} to {self.target_object.name}"

    def __repr__(self) -> str:
        return self.__str__()

    def add_variables(self) -> Variable:
        return self.model.add_variables(
            lower=0,
            upper=self.available_kwh,
            name=f"{self.__str__()}",
        )

    def add_constraints(self):
        # energy flow from source port must match energy from target port
        self.model.add_constraints(
            self.source_port.var_used_capacity_kwh
            == self.target_port.var_used_capacity_kwh
        )
        # energy flow from source port must match the energy transported
        # together with the above constraint it makes sure that
        # transport equals target port
        self.model.add_constraints(
            self.source_port.var_used_capacity_kwh == self.var_transport_kwh
        )

    def get_cost(self) -> LinearExpression:
        return -1 * self.var_transport_kwh * self.price_transport_per_kwh


if __name__ == "__main__":
    model = Model()

    germany = Country(
        model=model,
        name="Germany",
        price_buy_per_kwh=0.401,
        price_sell_per_kwh=0.395,
        capacity_export_kwh=1234,
        capacity_import_kwh=456,
    )
    austria = Country(
        model=model,
        name="Austria",
        price_buy_per_kwh=0.280,
        price_sell_per_kwh=0.275,
        capacity_export_kwh=789,
        capacity_import_kwh=987,
    )

    all_countries: list[Country] = [
        germany,
        austria,
    ]

    link_germany_to_austria = Link(
        model=model,
        name="germany_to_austria",
        source_object=germany,
        source_port=germany.port_export,
        target_object=austria,
        target_port=austria.port_import,
        price_transport_per_kwh=0.01,
        available_kwh=50000,
    )

    link_austria_to_germany = Link(
        model=model,
        name="austria_to_germany",
        source_object=austria,
        source_port=austria.port_export,
        target_object=germany,
        target_port=germany.port_import,
        price_transport_per_kwh=0.015,
        available_kwh=40000,
    )

    all_links = [
        link_germany_to_austria,
        link_austria_to_germany,
    ]

    all_objects = [*all_countries, *all_links]

    all_costs = [obj.get_cost() for obj in all_objects]

    model.add_objective(
        expr=sum(all_costs),  # ty:ignore[invalid-argument-type]
        sense="max",
    )
    model.solve(solver_name="highs")

    # extra all vars
    all_vars: list[Variable] = []
    for country in all_countries:
        all_vars.append(country.var_buy_kwh)
        all_vars.append(country.var_sell_kwh)
    for link in all_links:
        all_vars.append(link.var_transport_kwh)

    for var in all_vars:
        print(var, var.solution)
