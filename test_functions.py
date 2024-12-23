"""Module with unit tests for the helper functions."""

from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

import functions


@pytest.fixture
def mock_customers_df() -> pd.DataFrame:
    """Return a fake customers dataframe for testing.

    Returns:
        pd.DataFrame: a pandas dataframe with dummy data.

    """
    return pd.DataFrame(
        {
            "lat": [40.785091, 40.748817, 40.730610, 40.712776],
            "lon": [-73.968285, -73.985428, -73.935242, -74.005974],
            "demands": [0, 20, 5, 10],
        },
    )


@pytest.fixture
def mock_vehicles_df() -> pd.DataFrame:
    """Return a fake vehicles dataframe for testing.

    Returns:
        pd.DataFrame: a pandas dataframe with dummy data.

    """
    return pd.DataFrame({"id": [1, 2, 3], "capacity": [15, 30, 10]})


def test_generate_distance_matrix(mock_customers_df: pd.DataFrame) -> None:
    """Assert the created distance matrix.

    This test checks that the generated matrix is a n*n square matrix, it
    doesn't contain any nan values for distance and it returns a list. Then it
    checks if the main diagonal row is zero.

    Args:
        mock_customers_df (pd.DataFrame): a pandas dataframe with dummy
        customers data.

    """
    result = functions.generate_distance_matrix(mock_customers_df)

    assert len(result) == mock_customers_df.shape[0]
    assert not np.isnan(result).any()
    assert isinstance(result, list)

    for i, row in enumerate(result):
        assert isinstance(row, list)
        assert len(row) == mock_customers_df.shape[0]
        assert row[i] == 0


def test_create_data_model(
    mock_customers_df: pd.DataFrame,
    mock_vehicles_df: pd.DataFrame,
) -> None:
    """Assert the creation of customers df.

    This test checks that the create data model returns a dictionary and it
    contains all the necessary columns.

    Args:
        mock_customers_df (pd.DataFrame): a pandas dataframe with dummy
        customers data.
        mock_vehicles_df (pd.DataFrame): a pandas dataframe with dummy
        vehicles data.

    """
    with patch("functions.generate_distance_matrix") as mock_distance_matrix:
        mock_distance_matrix.return_value = [
            [0, 4.28, 6.662, 8.638],
            [4.28, 0, 4.696, 4.362],
            [6.662, 4.696, 0, 6.296],
            [8.638, 4.362, 6.296, 0],
        ]

        result = functions.create_data_model(
            mock_customers_df,
            mock_vehicles_df,
            )

        # Assertions
        assert isinstance(result, dict)
        assert "distance_matrix" in result
        assert "demands" in result
        assert "vehicle_capacities" in result
        assert "num_vehicles" in result
        assert "depot" in result
        assert "vehicle_name" in result
        assert "locations" in result
