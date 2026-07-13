import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------
# Load data
# --------------------------------------------------
df = pd.read_csv("nordic_indicators.csv")

# Use a clean plotting style
plt.style.use("ggplot")

# --------------------------------------------------
# 1. GDP per capita time series
# --------------------------------------------------
plt.figure(figsize=(10, 6))

# Plot one line per country
for country, group in df.groupby("country"):
    group = group.sort_values("year")
    plt.plot(
        group["year"],
        group["GDP"],
        marker="o",
        linewidth=2,
        label=country
    )

plt.title("GDP per Capita in Nordic Countries")
plt.xlabel("Year")
plt.ylabel("GDP per Capita (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("01_gdp_timeseries.png", dpi=300)
plt.show()

# --------------------------------------------------
# 2. Internet usage time series
# --------------------------------------------------
plt.figure(figsize=(10, 6))

for country, group in df.groupby("country"):
    group = group.sort_values("year")
    plt.plot(
        group["year"],
        group["Internet"],
        marker="o",
        linewidth=2,
        label=country
    )

plt.title("Internet Usage in Nordic Countries")
plt.xlabel("Year")
plt.ylabel("Internet Users (% of Population)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("02_internet_timeseries.png", dpi=300)
plt.show()

# --------------------------------------------------
# 3. Population development
# --------------------------------------------------
plt.figure(figsize=(10, 6))

for country, group in df.groupby("country"):
    group = group.sort_values("year")
    plt.plot(
        group["year"],
        group["Population"],
        marker="o",
        linewidth=2,
        label=country
    )

plt.title("Population Development")
plt.xlabel("Year")
plt.ylabel("Population")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("03_population_trend.png", dpi=300)
plt.show()

# --------------------------------------------------
# 4. Correlation: Internet usage vs GDP
# Bubble size represents population
# --------------------------------------------------
plt.figure(figsize=(10, 6))

scatter = plt.scatter(
    df["Internet"],
    df["GDP"],
    s=df["Population"] / 50000,
    c=df["GDP"],
    cmap="viridis",
    alpha=0.75
)

plt.colorbar(label="GDP per Capita")
plt.title("Internet Usage vs GDP per Capita")
plt.xlabel("Internet Users (%)")
plt.ylabel("GDP per Capita (USD)")
plt.grid(True)
plt.tight_layout()
plt.savefig("04_correlation_scatter.png", dpi=300)
plt.show()

# --------------------------------------------------
# 5. Latest-year country comparison
# --------------------------------------------------
latest_year_data = (
    df.sort_values("year")
      .groupby("country")
      .tail(1)
)

plt.figure(figsize=(10, 6))

bars = plt.bar(
    latest_year_data["country"],
    latest_year_data["GDP"],
    color="steelblue"
)

# Show GDP values above bars
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:,.0f}",
        ha="center",
        va="bottom"
    )

plt.title("Latest GDP per Capita by Country")
plt.xlabel("Country")
plt.ylabel("GDP per Capita (USD)")
plt.tight_layout()
plt.savefig("05_latest_comparison.png", dpi=300)
plt.show()

# --------------------------------------------------
# 6. GDP heatmap
# --------------------------------------------------
gdp_matrix = df.pivot_table(
    values="GDP",
    index="country",
    columns="year"
)

plt.figure(figsize=(12, 6))

heatmap = plt.imshow(
    gdp_matrix,
    aspect="auto",
    cmap="YlGnBu"
)

plt.colorbar(label="GDP per Capita (USD)")

plt.yticks(
    np.arange(len(gdp_matrix.index)),
    gdp_matrix.index
)

plt.xticks(
    np.arange(len(gdp_matrix.columns)),
    gdp_matrix.columns,
    rotation=45
)

plt.title("GDP Heatmap by Country and Year")
plt.xlabel("Year")
plt.ylabel("Country")

plt.tight_layout()
plt.savefig("06_gdp_heatmap.png", dpi=300)
plt.show()

print("All six visualizations created successfully.")