"""A port is a connection of a component; a component can have multiple ports."""

from linopy import Model, Variable


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
