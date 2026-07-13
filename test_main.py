import pandas as pd
from requests.exceptions import RequestException
from unittest.mock import Mock, patch

from main import (
    build_url,
    fetch_indicator,
    clean_indicator_data,
    merge_indicators,
    save_to_csv,
    main,
    GDP_INDICATOR,
)


# ============================================================================
# build_url()
# ============================================================================

def test_build_url():
    url = build_url("FIN", GDP_INDICATOR)

    expected = (
        "https://api.worldbank.org/v2/country/"
        "FIN/indicator/NY.GDP.PCAP.CD"
        "?format=json&per_page=100"
    )

    assert url == expected


def test_build_url_contains_country_and_indicator():
    url = build_url("SWE", "TEST")

    assert "SWE" in url
    assert "TEST" in url


# ============================================================================
# fetch_indicator()
# ============================================================================

@patch("main.requests.get")
def test_fetch_indicator_success(mock_get):
    mock_response = Mock()

    expected_json = [
        {},
        [{"date": "2023", "value": 50000}],
    ]

    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = expected_json

    mock_get.return_value = mock_response

    result = fetch_indicator(
        "FIN",
        GDP_INDICATOR,
    )

    assert result == expected_json


@patch("main.requests.get")
def test_fetch_indicator_calls_correct_url(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = []

    mock_get.return_value = mock_response

    fetch_indicator(
        "FIN",
        GDP_INDICATOR,
    )

    expected_url = build_url(
        "FIN",
        GDP_INDICATOR,
    )

    mock_get.assert_called_once_with(
        expected_url,
        timeout=10,
    )


@patch("main.requests.get")
def test_fetch_indicator_network_error_returns_none(mock_get):
    mock_get.side_effect = RequestException(
        "Connection failed"
    )

    result = fetch_indicator(
        "FIN",
        GDP_INDICATOR,
    )

    assert result is None


@patch("main.requests.get")
def test_fetch_indicator_unexpected_error_returns_none(mock_get):
    mock_get.side_effect = ValueError(
        "Unexpected error"
    )

    result = fetch_indicator(
        "FIN",
        GDP_INDICATOR,
    )

    assert result is None


# ============================================================================
# clean_indicator_data()
# ============================================================================

def test_clean_indicator_data_returns_dataframe():
    api_data = [
        {},
        [
            {"date": "2023", "value": 50000},
            {"date": "2022", "value": 48000},
        ],
    ]

    result = clean_indicator_data(
        api_data,
        "Finland",
        "GDP",
    )

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2


def test_clean_indicator_data_renames_columns():
    api_data = [
        {},
        [
            {"date": "2023", "value": 50000},
        ],
    ]

    result = clean_indicator_data(
        api_data,
        "Finland",
        "GDP",
    )

    assert "year" in result.columns
    assert "GDP" in result.columns


def test_clean_indicator_data_adds_country_column():
    api_data = [
        {},
        [
            {"date": "2023", "value": 50000},
        ],
    ]

    result = clean_indicator_data(
        api_data,
        "Finland",
        "GDP",
    )

    assert "country" in result.columns
    assert result.iloc[0]["country"] == "Finland"


def test_clean_indicator_data_removes_null_values():
    api_data = [
        {},
        [
            {"date": "2023", "value": 50000},
            {"date": "2022", "value": None},
        ],
    ]

    result = clean_indicator_data(
        api_data,
        "Finland",
        "GDP",
    )

    assert len(result) == 1
    assert result["GDP"].isna().sum() == 0


def test_clean_indicator_data_converts_year_to_integer():
    api_data = [
        {},
        [
            {"date": "2023", "value": 50000},
        ],
    ]

    result = clean_indicator_data(
        api_data,
        "Finland",
        "GDP",
    )

    assert pd.api.types.is_integer_dtype(
        result["year"]
    )


def test_clean_indicator_data_none_returns_empty_dataframe():
    result = clean_indicator_data(
        None,
        "Finland",
        "GDP",
    )

    assert result.empty


def test_clean_indicator_data_empty_list_returns_empty_dataframe():
    result = clean_indicator_data(
        [],
        "Finland",
        "GDP",
    )

    assert result.empty


def test_clean_indicator_data_invalid_payload_returns_empty_dataframe():
    result = clean_indicator_data(
        [{}],
        "Finland",
        "GDP",
    )

    assert result.empty


# ============================================================================
# merge_indicators()
# ============================================================================

def test_merge_indicators():
    gdp = pd.DataFrame({
        "country": ["Finland"],
        "year": [2023],
        "GDP": [50000],
    })

    internet = pd.DataFrame({
        "country": ["Finland"],
        "year": [2023],
        "Internet": [95.5],
    })

    population = pd.DataFrame({
        "country": ["Finland"],
        "year": [2023],
        "Population": [5600000],
    })

    result = merge_indicators(
        [gdp, internet, population]
    )

    assert len(result) == 1

    assert "GDP" in result.columns
    assert "Internet" in result.columns
    assert "Population" in result.columns


def test_merge_indicators_inner_join():
    gdp = pd.DataFrame({
        "country": ["Finland"],
        "year": [2023],
        "GDP": [50000],
    })

    internet = pd.DataFrame({
        "country": ["Finland"],
        "year": [2022],
        "Internet": [95.5],
    })

    result = merge_indicators(
        [gdp, internet]
    )

    assert result.empty


# ============================================================================
# save_to_csv()
# ============================================================================

def test_save_to_csv_creates_file(tmp_path):
    df = pd.DataFrame({
        "country": ["Finland"],
        "year": [2023],
        "GDP": [50000],
    })

    output_file = tmp_path / "output.csv"

    save_to_csv(df, output_file)

    assert output_file.exists()


def test_save_to_csv_preserves_data(tmp_path):
    df = pd.DataFrame({
        "country": ["Finland"],
        "year": [2023],
        "GDP": [50000],
    })

    output_file = tmp_path / "output.csv"

    save_to_csv(df, output_file)

    loaded = pd.read_csv(output_file)

    pd.testing.assert_frame_equal(
        df,
        loaded,
    )


# ============================================================================
# main()
# ============================================================================

@patch("main.save_to_csv")
@patch("main.fetch_indicator")
def test_main_workflow(mock_fetch, mock_save):
    mock_fetch.return_value = [
        {},
        [
            {
                "date": "2023",
                "value": 100,
            }
        ],
    ]

    main()

    # 5 countries × 3 indicators
    assert mock_fetch.call_count == 15

    mock_save.assert_called_once()


@patch("main.save_to_csv")
@patch("main.fetch_indicator")
def test_main_saves_dataframe(mock_fetch, mock_save):
    mock_fetch.return_value = [
        {},
        [
            {
                "date": "2023",
                "value": 100,
            }
        ],
    ]

    main()

    saved_df = mock_save.call_args[0][0]

    assert isinstance(saved_df, pd.DataFrame)
    assert not saved_df.empty