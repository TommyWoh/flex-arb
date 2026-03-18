"""Tests for flexarb proof oc concept."""

import pytest
from linopy import Model

from flexarb.proof_of_concept import Country, Link


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
        germany_price_buy_per_kwh: float,
        germany_price_sell_per_kwh: float,
        germany_capacity_export_kwh: float,
        germany_capacity_import_kwh: float,
        german_expected_buy_kwh: float,
        german_expected_sell_kwh: float,
    ):
        model = Model()

        germany = Country(
            model=model,
            name="Germany",
            price_buy_per_kwh=germany_price_buy_per_kwh,
            price_sell_per_kwh=germany_price_sell_per_kwh,
            capacity_export_kwh=germany_capacity_export_kwh,
            capacity_import_kwh=germany_capacity_import_kwh,
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

        assert germany.var_buy_kwh.solution == german_expected_buy_kwh
        assert germany.var_sell_kwh.solution == german_expected_sell_kwh
        # what is bought by austria is sold by germany
        assert austria.var_buy_kwh.solution == german_expected_sell_kwh
        # what is sold by austria is bought by germany
        assert austria.var_sell_kwh.solution == german_expected_buy_kwh
