import os
import requests
import pandas as pd
from requests.exceptions import RequestException
from functools import reduce

# World Bank indicator URLs
URL_GDP = (
    "https://api.worldbank.org/v2/country/{country}/"
    "indicator/NY.GDP.PCAP.CD"
    "?format=json&per_page=100"
)

URL_INTERNET = (
    "https://api.worldbank.org/v2/country/{country}/"
    "indicator/IT.NET.USER.ZS"
    "?format=json&per_page=100"
)

URL_POPULATION = (
    "https://api.worldbank.org/v2/country/{country}/"
    "indicator/SP.POP.TOTL"
    "?format=json&per_page=100"
)

DATA_FILE = "nordic_indicators.csv"

COUNTRIES = {
    "FIN": "Finland",
    "SWE": "Sweden",
    "NOR": "Norway",
    "DNK": "Denmark",
    "ISL": "Iceland",
}


def fetch_indicator(country_code, url_template, column_name):
    """
    Fetch a World Bank indicator and return a cleaned DataFrame.
    """
    response = requests.get(
        url_template.format(country=country_code),
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list) or len(data) < 2:
        return pd.DataFrame()

    df = pd.DataFrame(data[1])

    if not {"date", "value"}.issubset(df.columns):
        return pd.DataFrame()

    df = df[["date", "value"]].copy()

    df["date"] = pd.to_numeric(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    df = df.dropna()

    return df.rename(columns={"value": column_name})


try:

    if os.path.exists(DATA_FILE):
        print(f"Loading '{DATA_FILE}'...")
        final_df = pd.read_csv(DATA_FILE)

    else:
        print("Downloading data from World Bank API...")

        all_data = []

        for country_code, country_name in COUNTRIES.items():

            print(f"Fetching {country_name}...")

            indicators = [
                (
                    fetch_indicator(
                        country_code,
                        URL_GDP,
                        "gdp_per_capita_usd"
                    )
                ),
                (
                    fetch_indicator(
                        country_code,
                        URL_INTERNET,
                        "internet_users_pct"
                    )
                ),
                (
                    fetch_indicator(
                        country_code,
                        URL_POPULATION,
                        "population"
                    )
                ),
            ]

            # Keep non-empty DataFrames
            indicators = [df for df in indicators if not df.empty]

            if not indicators:
                print(f"Skipping {country_name}: no data found.")
                continue

            # Merge all indicators on year
            country_df = reduce(
                lambda left, right: pd.merge(
                    left,
                    right,
                    on="date",
                    how="outer"
                ),
                indicators
            )

            country_df["country_code"] = country_code
            country_df["country"] = country_name

            all_data.append(country_df)

        if not all_data:
            raise ValueError("No data downloaded.")

        final_df = pd.concat(
            all_data,
            ignore_index=True
        )

        final_df = final_df.sort_values(
            by=["country", "date"]
        )

        final_df.to_csv(
            DATA_FILE,
            index=False
        )

        print(f"Data saved to '{DATA_FILE}'")

    print("\nDataset info:")
    print(final_df.info())

    print("\nSample data:")
    print(final_df.head(10))

except RequestException as error:
    print(f"Network error: {error}")

except Exception as error:
    print(f"Unexpected error: {error}")