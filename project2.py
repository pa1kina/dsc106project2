import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("dataset_2026-04-21T17_11_26.528833749Z_DEFAULT_INTEGRATION_IMF.STA_CO2E_2.0.1.csv")

years = [str(y) for y in range(1995, 2022)]

indicator_total = "CO2 emissions embodied in production, Metric ton of CO₂ equivalent"

prod = df[df["INDICATOR"] == indicator_total].copy()
prod = prod[["COUNTRY", "INDICATOR"] + years]

for y in years:
    prod[y] = pd.to_numeric(prod[y], errors="coerce")

valid_years = [y for y in years if prod[y].notna().sum() > 50]

bad_labels = [
    "Not Specified (including Confidential)",
    "World",
    "Advanced Economies",
    "Emerging Market and Developing Economies"
]
prod = prod[~prod["COUNTRY"].isin(bad_labels)].copy()

country_totals = prod.groupby("COUNTRY")[valid_years].sum()

def format_num(x):
    return f"{int(x):,}"


global_total = country_totals.sum()

plt.figure(figsize=(11, 6))
plt.plot([int(y) for y in valid_years], global_total.values, marker="o", linewidth=2.5)

plt.title("Global CO₂ Emissions Have Increased Steadily Over Time", fontsize=20, pad=14)
plt.xlabel("Year", fontsize=13)
plt.ylabel("Total CO₂ Emissions (MtCO₂e)", fontsize=13)
plt.grid(True, alpha=0.25)

plt.annotate(
    format_num(global_total.iloc[0]),
    (int(valid_years[0]), global_total.iloc[0]),
    xytext=(0, 10),   # 👈 straight above
    textcoords="offset points",
    ha="center",
    va="bottom",
    fontsize=10,
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8)
)

plt.annotate(
    format_num(global_total.iloc[-1]),
    (int(valid_years[-1]), global_total.iloc[-1]),
    xytext=(0, 10),   # 👈 straight above
    textcoords="offset points",
    ha="center",
    va="bottom",
    fontsize=10,
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8)
)

plt.tight_layout()
plt.show()

top_countries = country_totals.sum(axis=1).sort_values(ascending=False)

top_countries = [c for c in top_countries.index if "Not Specified" not in c][:5]

top_data = country_totals.loc[top_countries]

plt.figure(figsize=(11, 6))
for country in top_data.index:
    plt.plot(
        [int(y) for y in valid_years],
        top_data.loc[country],
        marker="o",
        linewidth=2.2,
        label=country
    )

plt.title("The Largest Emitters Continue to Increase CO₂ Output", fontsize=20, pad=14)
plt.xlabel("Year", fontsize=13)
plt.ylabel("CO₂ Emissions (MtCO₂e)", fontsize=13)
plt.grid(True, alpha=0.25)
plt.legend(frameon=True, fontsize=11)

plt.tight_layout()
plt.show()

recent_years = [y for y in valid_years if int(y) >= 2010]
global_recent = country_totals[recent_years].sum()

plt.figure(figsize=(11, 6))
plt.plot([int(y) for y in recent_years], global_recent.values, marker="o", linewidth=2.5)

plt.title("Global CO₂ Emissions Have Recently Leveled Off", fontsize=20, pad=14)
plt.xlabel("Year", fontsize=13)
plt.ylabel("Total CO₂ Emissions (MtCO₂e)", fontsize=13)
plt.grid(True, alpha=0.25)

ymin = global_recent.min() - 150
ymax = global_recent.max() + 120
plt.ylim(ymin, ymax)

plt.annotate(
    "Little net change\nfor several years",
    (2014, global_recent.loc["2014"]),
    xytext=(20, 20),
    textcoords="offset points",
    fontsize=10,
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.85)
)

plt.tight_layout()
plt.show()


country_recent = country_totals[recent_years]

declining = country_recent[
    country_recent[recent_years[-1]] < country_recent[recent_years[0]]
]

top_declining = (
    (declining[recent_years[0]] - declining[recent_years[-1]])
    .sort_values(ascending=False)
    .head(5)
    .index
)

declining_data = country_recent.loc[top_declining]

plt.figure(figsize=(11, 6))
for country in declining_data.index:
    plt.plot(
        [int(y) for y in recent_years],
        declining_data.loc[country],
        marker="o",
        linewidth=2.2,
        label=country
    )

plt.title("Some Countries Have Successfully Reduced CO₂ Emissions", fontsize=20, pad=14)
plt.xlabel("Year", fontsize=13)
plt.ylabel("CO₂ Emissions (MtCO₂e)", fontsize=13)
plt.grid(True, alpha=0.25)
plt.legend(frameon=True, fontsize=11)

plt.tight_layout()
plt.show()