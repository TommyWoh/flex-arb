"""A link is a connection between a two components and there between two ports."""

from linopy import LinearExpression, Model, Variable

from flexarb.components.country import Country
from flexarb.components.port import Port


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
