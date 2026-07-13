import requests
import pandas as pd

from functools import reduce
from requests.exceptions import RequestException


COUNTRIES = {
    "FIN": "Finland",
    "SWE": "Sweden",
    "NOR": "Norway",
    "DNK": "Denmark",
    "ISL": "Iceland",
}

DATA_FILE = "nordic_indicators.csv"

GDP_INDICATOR = "NY.GDP.PCAP.CD"
INTERNET_INDICATOR = "IT.NET.USER.ZS"
POPULATION_INDICATOR = "SP.POP.TOTL"

BASE_URL = (
    "https://api.worldbank.org/v2/country/"
    "{country}/indicator/{indicator}"
    "?format=json&per_page=100"
)

def build_url(country_code, indicator_code):
    """
    Build World Bank API URL.
    """
    return BASE_URL.format(
        country=country_code,
        indicator=indicator_code,
    )

def fetch_indicator(country_code, indicator_code):
    """
    Fetch raw indicator JSON from World Bank API.
    """
    url = build_url(country_code, indicator_code)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        return response.json()

    except RequestException as error:
        print(f"Network error: {error}")
        return None

    except Exception as error:
        print(f"Unexpected error: {error}")
        return None

def clean_indicator_data(
    api_data,
    country_name,
    column_name,
):
    """
    Convert API response to clean DataFrame.
    """
    if not api_data or len(api_data) < 2:
        return pd.DataFrame()

    records = api_data[1]

    df = pd.DataFrame(records)

    df = df[["date", "value"]]

    df = df.rename(
        columns={
            "date": "year",
            "value": column_name,
        }
    )

    df["country"] = country_name

    df = df.dropna(subset=[column_name])

    df["year"] = df["year"].astype(int)

    return df

def merge_indicators(dataframes):
    """
    Merge indicator DataFrames.
    """
    return reduce(
        lambda left, right: pd.merge(
            left,
            right,
            on=["country", "year"],
            how="inner",
        ),
        dataframes,
    )

def save_to_csv(df, filepath=DATA_FILE):
    """
    Save DataFrame to CSV.
    """
    df.to_csv(filepath, index=False)

def main():
    all_country_frames = []

    indicators = {
        "GDP": GDP_INDICATOR,
        "Internet": INTERNET_INDICATOR,
        "Population": POPULATION_INDICATOR,
    }

    for country_code, country_name in COUNTRIES.items():

        indicator_frames = []

        for column_name, indicator_code in indicators.items():

            api_data = fetch_indicator(
                country_code,
                indicator_code,
            )

            df = clean_indicator_data(
                api_data,
                country_name,
                column_name,
            )

            indicator_frames.append(df)

        merged = merge_indicators(indicator_frames)

        all_country_frames.append(merged)

    final_df = pd.concat(
        all_country_frames,
        ignore_index=True,
    )

    save_to_csv(final_df)

    print(f"Saved {len(final_df)} rows to {DATA_FILE}")


if __name__ == "__main__":
    main()  # pragma: no cover