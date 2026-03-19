"""Tests for flexarb proof oc concept."""

import pytest
from linopy import Model

from flexarb.components.country import Country
from flexarb.components.orderbook import OrderBook, Supply


class TestProofOfConcept:
    """Tests for the two country proof of concept."""

    @pytest.mark.parametrize(
        (
            "germany_price_buy_per_kwh",
            "germany_price_sell_per_kwh",
            "germany_capacity_export_kwh",
            "germany_capacity_import_kwh",
            "german_expected_buy_kwh",
            "german_expected_sell_kwh",
        ),
        [
            pytest.param(
                0.400, 0.300, 100, 200, 200, 0, id="germany_buys_from_austria"
            ),
            pytest.param(
                0.100, 0.1100, 100, 200, 0, 100, id="germany_sells_to_austria"
            ),
            pytest.param(
                0.400,
                0.300,
                100,
                0,
                0,
                0,
                id="germany_would_buy_from_austria_but_no_capacity",
            ),
            pytest.param(
                0.100,
                0.1100,
                0,
                200,
                0,
                0,
                id="germany_would_sells_to_austria_but_no_capacity",
            ),
        ],
    )
    def test_on(
        self,
        germany_price_buy_per_kwh: float,  # noqa: ARG002
        germany_price_sell_per_kwh: float,  # noqa: ARG002
        germany_capacity_export_kwh: float,  # noqa: ARG002
        germany_capacity_import_kwh: float,  # noqa: ARG002
        german_expected_buy_kwh: float,  # noqa: ARG002
        german_expected_sell_kwh: float,  # noqa: ARG002
    ):
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

        all_countries: list[Country] = [
            germany,
            austria,
        ]

        for country in all_countries:
            country.add_variables()
            country.add_constraints()

        """
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

        assert germany.var_buy_kwh.solution == german_expected_buy_kwh
        assert germany.var_sell_kwh.solution == german_expected_sell_kwh
        # what is bought by austria is sold by germany
        assert austria.var_buy_kwh.solution == german_expected_sell_kwh
        # what is sold by austria is bought by germany
        assert austria.var_sell_kwh.solution == german_expected_buy_kwh
        """
