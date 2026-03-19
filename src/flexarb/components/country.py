"""A country represents a given price zone."""

from linopy import LinearExpression, Model, Variable

from flexarb.components.orderbook import OrderBook
from flexarb.components.port import Port


class Country:
    """Represent a single country."""

    def __init__(
        self,
        model: Model,
        name: str,
        power_demand_kwh: float,
        order_book: OrderBook,
    ):
        """Setup country

        Parameters
        ----------
        model : Model
            linopy Model instance.
        name : str
            Name of the country
        power_demand_kwh : float
            How much power is needed in kWh.
            This is the amount of power that is needed and thus can be either produced
            in the country or can be
        order_book : OrderBook
            How much supply is available and how much it costs.
        """
        self.model = model
        self.name = name
        self.power_demand_kwh = power_demand_kwh
        self.order_book = order_book
        self.order_book_vars: dict[int, Variable] = {}

        self.ports: dict[str, Port] = {}
        self.ports_vars: dict[str, Variable] = {}

    def __str__(self) -> str:
        return f"Country: {self.name}"

    def __repr__(self) -> str:
        return self.__str__()

    def add_variables(self):
        """Add the variables that define the country."""
        # Each supply in the order book can be used, but it does not have to
        for i, supply in enumerate(self.order_book.supplies):
            self.order_book_vars[i] = self.model.add_variables(
                lower=0,
                upper=supply.size_kwh,
                name=f"{self.__str__()}/{i}/{supply.size_kwh}/{supply.price_per_kwh}",
            )

    def add_port(
        self,
        name: str,
        capacity_import_kwh: float,
        capacity_export_kwh: float,
    ) -> Port:
        """Dynamically add a port to the country."""
        if name in self.ports:
            raise ValueError("It is not possible to have ports with the same name!")
        self.ports[name] = Port(
            model=self.model,
            name=f"Port/{self.__str__()}/{name}",
            capacity_kwh=capacity_export_kwh,
        )
        self.ports_vars[name] = self.model.add_variables(
            lower=-1 * capacity_import_kwh,
            upper=capacity_export_kwh,
            name=f"{self.__str__()}_transport_kwh",
        )
        return self.ports[name]

    def add_constraints(self):
        """Add country level constraints to the model."""
        # the power demand must be met
        # it can either come from the inland suppliers or from other countries via port
        all_supplier_vars = list(self.order_book_vars.values())
        all_port_vars = list(self.ports_vars.values())
        self.model.add_constraints(
            sum([*all_supplier_vars, *all_port_vars])
            == self.power_demand_kwh  # ty:ignore[invalid-argument-type]
        )

        # energy which is sold needs to flow into the export port
        for name in self.ports:
            port = self.ports[name]
            var = self.ports_vars[name]
            self.model.add_constraints(
                port.var_used_capacity_kwh == var,
            )

    def get_cost(self) -> LinearExpression:
        """Calculate how much money it costs to met the power demand."""
        return sum(
            [
                -1 * self.order_book.supplies[i].price_per_kwh * self.order_book_vars[i]
                for i in self.order_book_vars
            ]
        )  # ty:ignore[invalid-return-type]
