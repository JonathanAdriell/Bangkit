# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st 

st.set_option('deprecation.showPyplotGlobalUse', False)

# Load files
day_df = pd.read_csv("submission/dashboard/day.csv")
hour_df = pd.read_csv("submission/dashboard/hour.csv")

# Create groups
penyewaan_per_musim = day_df.groupby(['yr', 'season'])['cnt'].sum()
tren_penyewaan_sepeda = day_df.groupby(["yr", "mnth"])["cnt"].sum().reset_index()
penyewaan_per_jam = hour_df.groupby(['yr', 'hr'])['cnt'].agg(['mean', 'max', 'min']).reset_index()

# Polynomial regression of degree 2
coefficients = np.polyfit(tren_penyewaan_sepeda["mnth"], tren_penyewaan_sepeda["cnt"], 2)
polynomial = np.poly1d(coefficients)
poly_y = polynomial(tren_penyewaan_sepeda["mnth"])

# Make tren_penyewaan_sepeda more readable
month_dict = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}
year_dict = {
    0: "2011",
    1: "2012"
}

formatted_months = []
for index, row in tren_penyewaan_sepeda.iterrows():
    month = month_dict[row["mnth"]]
    year = year_dict[row["yr"]]
    formatted_months.append(f"{month}, {year}")

tren_penyewaan_sepeda["formatted_months"] = formatted_months

# Make penyewaan_per_musim more readable
penyewaan_per_musim = pd.DataFrame(penyewaan_per_musim).reset_index()
season_dict = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

formatted_seasons = []
for index, row in penyewaan_per_musim.iterrows():
    formatted_season = season_dict[row["season"]]
    formatted_seasons.append(formatted_season)

penyewaan_per_musim["formatted_seasons"] = formatted_seasons

# Create dashboard
st.header('Bike Sharing Dashboard')
st.write('The trend of bike rentals experienced an increase between 2011 and 2012.')

# Create line chart
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(tren_penyewaan_sepeda["formatted_months"], tren_penyewaan_sepeda["cnt"], marker='o', linewidth=2, color="lightblue", label="Data")
ax.plot(tren_penyewaan_sepeda["formatted_months"], poly_y, color="red", linestyle="--", label="Polynomial Fit (Degree 2)")
ax.set_title("Number of Bike Rentals per Month", fontsize=18)
ax.set_xticklabels(tren_penyewaan_sepeda["formatted_months"], rotation=45)
ax.legend()

st.pyplot(fig)

st.write('The highest daily bike rentals occurred during the fall season, both in 2011 and 2012. This was followed by summer, winter, and spring, in that order, in both years.')

# Filter based on year
year_2011 = penyewaan_per_musim[penyewaan_per_musim["yr"] == 0]
year_2012 = penyewaan_per_musim[penyewaan_per_musim["yr"] == 1]

# Get colors for year_2011 pie chart
year_2011_colors = ["lightgrey"] * len(year_2011)
max_index = year_2011["cnt"].idxmax()
year_2011_colors[max_index] = "orange"

# Get colors for year_2012 pie chart
year_2012_colors = ["lightgrey"] * len(year_2012)
max_index = year_2012["cnt"].idxmax() - 4
year_2012_colors[max_index] = "orange"

col1, col2 = st.columns(2)

# Display pie charts
with col1:
    plt.figure(figsize=(8, 6))
    plt.pie(year_2011["cnt"], labels=year_2011["formatted_seasons"], autopct="%1.1f%%", colors=year_2011_colors, wedgeprops=dict(edgecolor='black'))
    plt.title("Percentage of Bike Rentals per Season in 2011", pad=25)
    plt.axis("equal")
    st.pyplot()

with col2:
    plt.figure(figsize=(8, 6))
    plt.pie(year_2012["cnt"], labels=year_2012["formatted_seasons"], autopct="%1.1f%%", colors=year_2012_colors, wedgeprops=dict(edgecolor='black'))
    plt.title("Percentage of Bike Rentals per Season in 2012", pad=25)
    plt.axis("equal")
    st.pyplot()

st.write('The highest average number of bike rentals per hour occurred at 5:00 PM, both in 2011 and 2012.')

def show_barchart(df, year):
    penyewaan_year = df[df["yr"] == year]

    hours = penyewaan_year["hr"]
    average_penyewaan = penyewaan_year["mean"]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(hours, average_penyewaan, color="lightgrey")

    # Highlight the bar with the highest average
    highest_bar_index = average_penyewaan.idxmax()
    ax.bar(penyewaan_year.loc[highest_bar_index, "hr"], average_penyewaan.max(), color="orange")

    ax.set_title(f"Average Number of Bike Rentals per Hour in 201{year+1}")
    ax.legend()
    ax.grid(True)

    return fig

col1, col2 = st.columns(2)

# Display bar chart
with col1:
    st.pyplot(show_barchart(penyewaan_per_jam, 0))

with col2:
    st.pyplot(show_barchart(penyewaan_per_jam, 1))

st.write(
    """
    It can be concluded that the trend of bike rentals tends to peak in the middle of the year. The increase in bike rentals starts at the beginning of the year, then after reaching its peak, it will decrease again towards the end of the year.

    There is a pattern that daily bike rentals, in sequence from highest to lowest, occur in the fall, summer, winter, and spring seasons.

    Overall, the highest average number of bike rentals tends to occur at 5:00 PM.
    """
)
st.caption("Created by Jonathan Adriel")
