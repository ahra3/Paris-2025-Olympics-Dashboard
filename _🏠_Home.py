import streamlit as st
import pandas as pd
import plotly.express as px
import os

from utils.preprocessing import (
    prepare_medals_datasets,
    normalize_name,
    add_continent_column
)
from utils.filters import global_filters, apply_global_filters


# -----------------------------------------------------
# PAGE SETUP
# -----------------------------------------------------
st.set_page_config(
    page_title="🏠 Overview | LA28 Olympic Challenge",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏅Paris 2024 Olympics Dashboard")
st.markdown("### Explore the world of sports at a glance, uncover how nations, athletes, and medals come together in one dynamic dashboard!!")


# -----------------------------------------------------
# LOAD DATASETS
# -----------------------------------------------------
df_medals_total, df_medallists, df_medals = prepare_medals_datasets()

# ADD NORMALIZED NAME COLUMN BEFORE FILTERING (IMPORTANT FIX)
df_medallists["name_norm"] = df_medallists["name"].apply(normalize_name)

@st.cache_data
def load_extra_data():
    DATA = os.path.join(os.path.dirname(__file__), "data")
    athletes = pd.read_csv(f"{DATA}/athletes.csv")
    teams = pd.read_csv(f"{DATA}/teams.csv")
    events = pd.read_csv(f"{DATA}/events.csv")
    nocs = pd.read_csv(f"{DATA}/nocs.csv")
    return athletes, teams, events, nocs

athletes, teams, events, nocs = load_extra_data()

# ADD CONTINENT COLUMN TO ATHLETES TO ENABLE CONTINENT FILTERING
athletes = add_continent_column(athletes, "country_code")


# -----------------------------------------------------
# GLOBAL FILTERS (with continent)
# -----------------------------------------------------
filters = global_filters(df_medallists)

# Filter medallists
df_filtered_medallists = apply_global_filters(df_medallists, filters)

# Ensure name_norm exists after filtering
df_filtered_medallists["name_norm"] = df_filtered_medallists["name"].apply(normalize_name)


# -----------------------------------------------------
# FILTER MEDALS TOTAL
# -----------------------------------------------------
df_medals_total_filtered = df_medals_total.copy()

# Continent filter
if filters["continent"]:
    df_medals_total_filtered = df_medals_total_filtered[
        df_medals_total_filtered["continent"].isin(filters["continent"])
    ]

# Country filter
if filters["selected_countries"]:
    df_medals_total_filtered = df_medals_total_filtered[
        df_medals_total_filtered["country_code"].isin(filters["selected_countries"])
    ]


# -----------------------------------------------------
# FILTER ATHLETES (continent now works)
# -----------------------------------------------------
athletes_filtered = athletes.copy()

# Continent filter
if filters["continent"]:
    athletes_filtered = athletes_filtered[
        athletes_filtered["continent"].isin(filters["continent"])
    ]

# Country filter
if filters["selected_countries"]:
    athletes_filtered = athletes_filtered[
        athletes_filtered["country_code"].isin(filters["selected_countries"])
    ]

# Gender filter
if filters["selected_genders"]:
    athletes_filtered = athletes_filtered[
        athletes_filtered["gender"].isin(filters["selected_genders"])
    ]


# -----------------------------------------------------
# KPI SECTION — ALL FILTERS APPLIED
# -----------------------------------------------------
st.subheader("📊 Overall Statistics")

total_athletes = athletes_filtered["name"].nunique()
total_countries = df_medals_total_filtered["country_code"].nunique()
total_sports = events["sport"].nunique()
total_medals = df_medals_total_filtered["Total"].sum()
total_events = events["event"].nunique()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Athletes", f"{total_athletes:,}")
c2.metric("Countries", f"{total_countries:,}")
c3.metric("Sports", f"{total_sports:,}")
c4.metric("Total Medals", f"{total_medals:,}")
c5.metric("Events", f"{total_events:,}")

st.markdown("---")


# -----------------------------------------------------
# ATHLETE PROFILE
# -----------------------------------------------------
st.header("🔍 Athlete Profile")
st.markdown("Select an athlete to view medal history and profile information.")

valid_names = [
    n for n in athletes_filtered["name"].unique()
    if isinstance(n, str) and not n.strip().isdigit()
]

selected_athlete = st.selectbox("Choose an athlete:", [""] + sorted(valid_names))

if selected_athlete:
    athlete_row = athletes_filtered[
        athletes_filtered["name"] == selected_athlete
    ].iloc[0]

    norm_selected = normalize_name(selected_athlete)

    athlete_medals = df_filtered_medallists[
        df_filtered_medallists["name_norm"] == norm_selected
    ]

    left, right = st.columns([3, 2])

    with left:
        st.subheader(f"🏅 {selected_athlete} ({athlete_row['country']})")
        st.markdown(f"**Gender:** {athlete_row.get('gender', 'N/A')}")

    with right:
        st.subheader("Medal Summary")

        if athlete_medals.empty:
            st.info("This athlete has no medals.")
        else:
            counts = athlete_medals["medal_type"].value_counts()
            c1, c2, c3 = st.columns(3)
            c1.metric("Gold", counts.get("Gold", 0))
            c2.metric("Silver", counts.get("Silver", 0))
            c3.metric("Bronze", counts.get("Bronze", 0))

else:
    st.info("Select an athlete or adjust filters.")

st.markdown("---")


# -----------------------------------------------------
# PIE CHART (FILTERED)
# -----------------------------------------------------
st.header("🥇 Global Medal Distribution (Filtered)")

medal_sum = df_medals_total_filtered[["Gold", "Silver", "Bronze"]].sum()

df_pie = pd.DataFrame({
    "Medal": ["Gold", "Silver", "Bronze"],
    "Count": medal_sum.values
})

df_pie = df_pie[df_pie["Medal"].isin(filters["selected_medal_types"])]

if df_pie["Count"].sum() > 0:
    fig = px.pie(
        df_pie,
        names="Medal",
        values="Count",
        color="Medal",
        color_discrete_map={
            "Gold": "#FFD700",
            "Silver": "#C0C0C0",
            "Bronze": "#CD7F32"
        }
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No medal data for selected filters.")

st.markdown("---")


# -----------------------------------------------------
# TOP 10 COUNTRIES (FILTERED)
# -----------------------------------------------------
st.header("🥇 Top 10 Countries by Medals")

top10 = df_medals_total_filtered.groupby("country_code")["Total"].sum().reset_index()

top10 = top10.merge(
    nocs[["code", "country"]],
    left_on="country_code",
    right_on="code",
    how="left"
)

top10 = top10.sort_values("Total", ascending=False).head(10)

if not top10.empty:
    fig = px.bar(
        top10,
        y="country",
        x="Total",
        orientation="h",
        color="Total",
        color_continuous_scale="Plasma",
        title="Top 10 Countries by Total Medals"
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("No medal data for selected filters.")
