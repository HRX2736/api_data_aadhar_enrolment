import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===============================
# 1. DATA LOADING
# ===============================

files = [
    "api_data_aadhar_enrolment_0_500000.csv",
    "api_data_aadhar_enrolment_500000_1000000.csv",
    "api_data_aadhar_enrolment_1000000_1006029.csv"
]

dfs = []
for f in files:
    df = pd.read_csv(f, encoding_errors="ignore")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    dfs.append(df)

df = pd.concat(dfs, ignore_index=True)

# ===============================
# 2. BASIC CLEANING
# ===============================

df = df.dropna(subset=["date", "state", "district", "pincode"])

df["state"] = (
    df["state"]
    .str.lower()
    .str.strip()
    .str.replace("&", "and", regex=False)
)

state_merge = {
    "dadra and nagar haveli": "dadra and nagar haveli and daman and diu",
    "daman and diu": "dadra and nagar haveli and daman and diu"
}
df["state"] = df["state"].replace(state_merge)

df["total_enrolments"] = (
    df["age_0_5"] +
    df["age_5_17"] +
    df["age_18_greater"]
)

# ===============================
# 3. UNIVARIATE ANALYSIS
# ===============================

state_total = (
    df.groupby("state")["total_enrolments"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure()
state_total.plot(kind="bar")
plt.title("Top 10 States by Total Aadhaar Enrolments")
plt.ylabel("Total Enrolments")
plt.tight_layout()
plt.show()

# ===============================
# 4. BIVARIATE ANALYSIS
# ===============================
# Enrolment Momentum Index (trend slope)

state_time = (
    df.groupby(["state", "date"])["total_enrolments"]
    .sum()
    .reset_index()
)

momentum = {}

for state, g in state_time.groupby("state"):
    g = g.sort_values("date")
    if len(g) >= 3:
        x = np.arange(len(g))
        y = g["total_enrolments"].values
        slope = np.polyfit(x, y, 1)[0]
        momentum[state] = slope

momentum_df = (
    pd.Series(momentum)
    .sort_values(ascending=False)
    .head(8)
)

plt.figure()
momentum_df.plot(kind="bar")
plt.title("States with Highest Aadhaar Enrolment Momentum")
plt.ylabel("Trend Strength")
plt.tight_layout()
plt.show()

# ===============================
# 5. TRIVARIATE ANALYSIS
# ===============================
# State × Time × Age Composition

age_long = df.melt(
    id_vars=["date", "state"],
    value_vars=["age_0_5", "age_5_17", "age_18_greater"],
    var_name="age_group",
    value_name="enrolments"
)

top_states = state_total.index[:5]
age_filtered = age_long[age_long["state"].isin(top_states)]

age_trend = (
    age_filtered
    .groupby(["date", "age_group"])["enrolments"]
    .sum()
    .unstack()
)

plt.figure()
age_trend.plot()
plt.title("Age-wise Aadhaar Enrolment Trends (Top States)")
plt.ylabel("Enrolments")
plt.tight_layout()
plt.show()

# ===============================
# 6. INNOVATIVE SPATIAL INSIGHT
# ===============================
# Enrolment Intensity per PIN (district pressure proxy)

district_intensity = (
    df.groupby(["state", "district"])
    .agg(
        total_enrolments=("total_enrolments", "sum"),
        unique_pins=("pincode", "nunique")
    )
)

district_intensity["enrolments_per_pin"] = (
    district_intensity["total_enrolments"] /
    district_intensity["unique_pins"]
)

hotspots = (
    district_intensity
    .sort_values("enrolments_per_pin", ascending=False)
    .head(10)
)

print("\nTop Districts with High Enrolment Intensity:")
print(hotspots.reset_index())
# ================================
# Aadhaar Enrolment Stability Index
# ================================

# total daily enrolments per state
state_daily = (
    df.groupby(["state", "date"])[["age_0_5", "age_5_17", "age_18_greater"]]
    .sum()
)

state_daily["total_enrolments"] = state_daily.sum(axis=1)

# compute stability metrics
stability = (
    state_daily["total_enrolments"]
    .groupby("state")
    .agg(["mean", "std"])
)

stability["stability_index"] = stability["std"] / stability["mean"]
stability = stability.sort_values("stability_index", ascending=False)

# print top unstable states
print("\nStates with Highest Enrolment Volatility (Unstable):")
print(stability.head(10))

# plot
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
stability["stability_index"].head(10).plot(kind="bar")
plt.title("States with Highest Aadhaar Enrolment Volatility")
plt.ylabel("Stability Index (Std / Mean)")
plt.xlabel("State")
plt.tight_layout()
plt.show()
# after reading CSVs and cleaning
df = df[df["state"] != "100000"]
df = df[df["state"].apply(lambda x: not str(x).isdigit())]
