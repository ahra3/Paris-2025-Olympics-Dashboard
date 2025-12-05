import streamlit as st
import pandas as pd
import plotly.express as px

from utils.preprocessing import prepare_medals_datasets
from utils.filters import global_filters, apply_global_filters


# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="Global Analysis - Paris 2024",
    page_icon="🗺️",
    layout="wide",
)

GOLD_COLOR = "#FFD700"
SILVER_COLOR = "#C0C0C0"
BRONZE_COLOR = "#CD7F32"

MEDAL_COLOR_MAP = {
    "Gold": GOLD_COLOR,
    "Silver": SILVER_COLOR,
    "Bronze": BRONZE_COLOR,
}

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------
@st.cache_data
def load_data():
    return prepare_medals_datasets()

df_medals_total, df_medallists, df_medals = load_data()

st.title("🗺️ Global Analysis Dashboard")
st.markdown("Explore all global medal insights using the sidebar filters and the tabs below.")

# -----------------------------------------------------
# FILTER DATA
# -----------------------------------------------------
filters = global_filters(df_medallists)
df_filtered = apply_global_filters(df_medallists, filters)

if df_filtered.empty:
    st.warning("No data matches your filters.")
    st.stop()


# -----------------------------------------------------
# HELPER AGGREGATION FUNCTIONS
# -----------------------------------------------------
def aggregate_country_medals(df):
    grp = df.groupby(
        ["country_code", "country_long", "medal_type"]
    ).size().reset_index(name="count")

    pivot = grp.pivot_table(
        index=["country_code", "country_long"],
        columns="medal_type",
        values="count",
        fill_value=0
    ).reset_index()

    for m in ["Gold", "Silver", "Bronze"]:
        if m not in pivot.columns:
            pivot[m] = 0

    pivot["Total"] = pivot["Gold"] + pivot["Silver"] + pivot["Bronze"]
    return pivot.sort_values("Total", ascending=False)


def aggregate_continent_medals(df):
    grp = df.groupby(["continent", "medal_type"]).size().reset_index(name="count")
    return grp[grp["medal_type"].isin(["Gold", "Silver", "Bronze"])]


def aggregate_sunburst(df):
    if "discipline" not in df.columns:
        df["discipline"] = "Unknown"
    return df.groupby(
        ["continent", "country", "discipline"]
    ).size().reset_index(name="count")


df_country_medals = aggregate_country_medals(df_filtered)
df_continent_medals = aggregate_continent_medals(df_filtered)
df_sunburst = aggregate_sunburst(df_filtered)


# -----------------------------------------------------
# TABS LAYOUT
# -----------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌍 World Medal Map",
    "🌞 Medal Hierarchy (Sunburst)",
    "📊 Continent Comparison",
    "🏆 Top 20 Countries",
    "👥 Medals by Gender",
    "🏅 Top 10 Sports",
])


# -----------------------------------------------------
# TAB 1 — Choropleth Map
# -----------------------------------------------------
with tab1:
    st.subheader("🌍 World Medal Map")

    fig_map = px.choropleth(
        df_country_medals,
        locations="country_code",
        color="Total",
        hover_name="country_long",
        color_continuous_scale="YlOrBr",
    )
    st.plotly_chart(fig_map, use_container_width=True)


# -----------------------------------------------------
# TAB 2 — Sunburst
# -----------------------------------------------------
with tab2:
    st.subheader("🌞 Medal Hierarchy by Continent → Country → Sport")

    fig_sun = px.sunburst(
        df_sunburst,
        path=["continent", "country", "discipline"],
        values="count",
        color="continent",
    )
    st.plotly_chart(fig_sun, use_container_width=True)


# -----------------------------------------------------
# TAB 3 — Continent vs Medal Type
# -----------------------------------------------------
with tab3:
    st.subheader("📊 Medals by Continent and Medal Type")

    fig_cont = px.bar(
        df_continent_medals,
        x="continent",
        y="count",
        color="medal_type",
        barmode="group",
        color_discrete_map=MEDAL_COLOR_MAP,
    )
    st.plotly_chart(fig_cont, use_container_width=True)


# -----------------------------------------------------
# TAB 4 — Top 20 Countries
# -----------------------------------------------------
with tab4:
    st.subheader("🏆 Top 20 Countries by Total Medals")

    df_top20 = df_country_medals.head(20)
    df_top20_melt = df_top20.melt(
        id_vars=["country_long"],
        value_vars=["Gold", "Silver", "Bronze"],
        var_name="medal_type",
        value_name="count",
    )

    fig_top20 = px.bar(
        df_top20_melt,
        x="country_long",
        y="count",
        color="medal_type",
        barmode="group",
        color_discrete_map=MEDAL_COLOR_MAP,
    )
    fig_top20.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_top20, use_container_width=True)


# -----------------------------------------------------
# TAB 5 — Medals by Gender
# -----------------------------------------------------
with tab5:
    st.subheader("👥 Medal Distribution by Gender")

    df_gender = (
        df_filtered.groupby(["gender", "medal_type"])
        .size().reset_index(name="count")
    )
    df_gender = df_gender[df_gender["medal_type"].isin(["Gold", "Silver", "Bronze"])]

    fig_gender = px.bar(
        df_gender,
        x="gender",
        y="count",
        color="medal_type",
        barmode="group",
        color_discrete_map=MEDAL_COLOR_MAP,
    )
    st.plotly_chart(fig_gender, use_container_width=True)


# -----------------------------------------------------
# TAB 6 — Top 10 Sports by Medal Count
# -----------------------------------------------------
with tab6:
    st.subheader("🏅 Top 10 Sports by Medal Count")

    if "discipline" not in df_filtered.columns:
        st.info("Sport data unavailable.")
    else:
        df_sport = (
            df_filtered.groupby(["discipline", "medal_type"])
            .size().reset_index(name="count")
        )

        df_sport = df_sport[df_sport["medal_type"].isin(["Gold", "Silver", "Bronze"])]

        totals = df_sport.groupby("discipline")["count"].sum().reset_index()
        top10 = totals.sort_values("count", ascending=False).head(10)["discipline"]

        df_sport_top10 = df_sport[df_sport["discipline"].isin(top10)]

        fig_sport = px.bar(
            df_sport_top10,
            x="discipline",
            y="count",
            color="medal_type",
            barmode="group",
            color_discrete_map=MEDAL_COLOR_MAP,
        )
        fig_sport.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_sport, use_container_width=True)
