import streamlit as st
import pandas as pd
import plotly.express as px

from utils.preprocessing import prepare_medals_datasets
from utils.filters import global_filters, apply_global_filters

# -----------------------------------------------------
# Page configuration
# -----------------------------------------------------
st.set_page_config(page_title="Sports & Events Analysis", layout="wide")
st.title("🏟️ Sports & Events Analysis")
st.markdown("### Explore event timelines, medal distribution by sport, and venue usage intensity.")

# -----------------------------------------------------
# Load core datasets
# -----------------------------------------------------
@st.cache_data
def load_additional_data():
    import os
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

    events = pd.read_csv(f"{DATA_DIR}/events.csv")
    schedule = pd.read_csv(f"{DATA_DIR}/schedules.csv")
    venues = pd.read_csv(f"{DATA_DIR}/venues.csv")
    return events, schedule, venues

df_medals_total, df_medallists, df_medals = prepare_medals_datasets()
events, schedule, venues = load_additional_data()

# -----------------------------------------------------
# Apply GLOBAL filters from sidebar
# -----------------------------------------------------
filters = global_filters(df_medallists)
df_filtered_medals = apply_global_filters(df_medallists, filters)

# -----------------------------------------------------
# Prepare EVENT-related filtered data
# -----------------------------------------------------
# Merge schedule with event table to get sport
schedule_merged = schedule.merge(events[['event', 'sport']], on='event', how='left')

# Filter by selected sports (global filter)
if filters["sport_col"] and filters["selected_sports"]:
    schedule_filtered = schedule_merged[schedule_merged["sport"].isin(filters["selected_sports"])]
else:
    schedule_filtered = schedule_merged.copy()

st.markdown("---")
tab1, tab2, tab3 = st.tabs([
    "🗓️ Event Calendar (Gantt)",
    "🥇 Medals by Sport (Treemap)",
    "🏟️ Venue Usage Intensity"
])

# =====================================================
# 1️⃣ EVENT CALENDAR (GANTT CHART)
# =====================================================
with tab1:
    st.header("🗓️ Event Calendar Timeline")
    st.markdown("Events are colored by **sport**. Filter sports using the global sidebar.")

    available_sports = sorted(schedule_filtered["sport"].dropna().unique())
    if available_sports:
        selected_sport = st.selectbox("Select a sport:", available_sports)
        df_gantt = schedule_filtered[schedule_filtered["sport"] == selected_sport].copy()

        df_gantt = df_gantt.dropna(subset=["start_date", "end_date"])
        df_gantt["start_date"] = pd.to_datetime(df_gantt["start_date"])
        df_gantt["end_date"] = pd.to_datetime(df_gantt["end_date"])

        if not df_gantt.empty:
            df_gantt = df_gantt.sort_values("start_date")

            fig = px.timeline(
                df_gantt,
                x_start="start_date",
                x_end="end_date",
                y="event",
                color="sport",
                title=f"Event Timeline for {selected_sport}",
                color_discrete_sequence=px.colors.qualitative.Bold,
            )

            fig.update_yaxes(autorange="reversed")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Event Details")
            show_cols = ["event", "sport", "start_date", "end_date", "venue"]
            st.dataframe(df_gantt[show_cols].sort_values("start_date"))
        else:
            st.info("No valid schedule entries for this sport.")
    else:
        st.warning("No sports available for the current global filters.")


# =====================================================
# 2️⃣ MEDALS BY SPORT (TREEMAP)
# =====================================================
with tab2:
    st.header("🥇 Medal Distribution by Sport and Country")

    # Merge medals with event info to get sport
    medal_events = df_filtered_medals.merge(events[['event', 'sport']], on='event', how='left')

    if "sport" not in medal_events.columns:
        st.error("Missing sport information. Cannot build treemap.")
    else:
        df_treemap = medal_events.groupby(["sport", "country"]).size().reset_index(name="Total Medals")

        if df_treemap.empty:
            st.info("No medal data available for selected filters.")
        else:
            fig = px.treemap(
                df_treemap,
                path=[px.Constant("Medals"), "sport", "country"],
                values="Total Medals",
                color="Total Medals",
                color_continuous_scale="Turbo",
                title="Hierarchical Medal Distribution",
            )
            st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 3️⃣ VENUE USAGE INTENSITY (BAR CHART)
# =====================================================
with tab3:
    st.header("🏟️ Venue Usage Intensity (Total Event Duration)")

    df_duration = schedule_filtered.copy()

    try:
        df_duration["start_date"] = pd.to_datetime(df_duration["start_date"])
        df_duration["end_date"] = pd.to_datetime(df_duration["end_date"])
    except:
        st.error("Date parsing failed for schedules.csv.")
        st.stop()

    df_duration["duration_days"] = (df_duration["end_date"] - df_duration["start_date"]).dt.total_seconds() / (24 * 3600)

    venue_intensity = df_duration.groupby("venue")["duration_days"].sum().reset_index()
    venue_intensity["duration_days"] = venue_intensity["duration_days"].round(2)
    venue_intensity = venue_intensity.sort_values("duration_days", ascending=False)

    if venue_intensity.empty:
        st.info("No event duration data available.")
    else:
        fig = px.bar(
            venue_intensity,
            x="duration_days",
            y="venue",
            orientation="h",
            color="duration_days",
            color_continuous_scale="Sunset",
            title="Total Event Duration per Venue"
        )
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
