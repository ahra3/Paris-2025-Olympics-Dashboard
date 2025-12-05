import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import os

# ------------------------------------
# Page Setup
# ------------------------------------
st.set_page_config(layout="wide", page_title="Athlete Performance")

st.markdown("""
<style>
.block-container { padding-left: 2rem; padding-right: 2rem; max-width: 100%; }
.section-header { background-color: #4CAF50; color: white; padding: 10px;
                  border-radius: 5px; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

def get_flag_emoji(code):
    flags = {
        'USA':'🇺🇸','CHN':'🇨🇳','JPN':'🇯🇵','GBR':'🇬🇧','AUS':'🇦🇺','GER':'🇩🇪','FRA':'🇫🇷','ITA':'🇮🇹',
        'BRA':'🇧🇷','CAN':'🇨🇦','RUS':'🇷🇺','KOR':'🇰🇷','NED':'🇳🇱','SWE':'🇸🇪','NOR':'🇳🇴'
    }
    return flags.get(code, "🏳️")


def load_image():
    return "👤"

# ------------------------------------
# Load Data (Correct Paths)
# ------------------------------------
ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, "data")

athletes_df = pd.read_csv(os.path.join(DATA_DIR, "athletes.csv"))
coaches_df = pd.read_csv(os.path.join(DATA_DIR, "coaches.csv"))
teams_df = pd.read_csv(os.path.join(DATA_DIR, "teams.csv"))
medals_df = pd.read_csv(os.path.join(DATA_DIR, "medals.csv"))
nocs_df = pd.read_csv(os.path.join(DATA_DIR, "nocs.csv"))
medals_total_df = pd.read_csv(os.path.join(DATA_DIR, "medals_total.csv"))

# ------------------------------------
# Continent Mapping
# ------------------------------------
continent_map = {
    'USA':'North America','CAN':'North America','MEX':'North America',
    'BRA':'South America','ARG':'South America','COL':'South America',
    'GBR':'Europe','GER':'Europe','FRA':'Europe','ITA':'Europe','ESP':'Europe',
    'NED':'Europe','SWE':'Europe','NOR':'Europe','RUS':'Europe',
    'CHN':'Asia','JPN':'Asia','KOR':'Asia','IND':'Asia','THA':'Asia',
    'AUS':'Oceania','NZL':'Oceania',
    'EGY':'Africa','KEN':'Africa','RSA':'Africa'
}

athletes_df["continent"] = athletes_df["country_code"].map(continent_map).fillna("Other")
medals_total_df["continent"] = medals_total_df["country_code"].map(continent_map).fillna("Other")

# ------------------------------------
# Clean Athletes Age
# ------------------------------------
athletes_df["birth_date"] = pd.to_datetime(athletes_df["birth_date"], errors="coerce")
today = datetime.date.today()

athletes_df["age"] = athletes_df["birth_date"].apply(
    lambda x: today.year - x.year - ((today.month, today.day) < (x.month, x.day))
    if pd.notna(x) else None
)
athletes_df = athletes_df.dropna(subset=["age"])

# ------------------------------------
# Medal Count per Athlete
# ------------------------------------
medal_counts = medals_df.groupby("name").size().reset_index(name="total_medals")

# ------------------------------------
# UI Layout
# ------------------------------------
st.title("🏅 Athlete Performance Dashboard")
st.markdown("---")

# ======================================================
# 1️⃣ Athlete Profile Card
# ======================================================
st.markdown('<div class="section-header"><h2>🎖 Athlete Profile</h2></div>', unsafe_allow_html=True)

# Remove invalid numeric names like "671"
athlete_list = [
    name for name in athletes_df["name"].dropna().unique()
    if isinstance(name, str) and not name.isdigit()
]

athlete_list = sorted(athlete_list)

selected_athlete = st.selectbox("🔍 Select an Athlete:", [""] + athlete_list)

if selected_athlete:
    row = athletes_df[athletes_df["name"] == selected_athlete].iloc[0]

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"<h1 style='text-align:center;font-size:120px'>{load_image()}</h1>", unsafe_allow_html=True)

    with col2:
        st.subheader(row["name"])
        flag = get_flag_emoji(row["country_code"])
        st.markdown(f"**Country:** {row['country']} ({row['country_code']}) {flag}")
        st.markdown(f"**Height / Weight:** {row.get('height', 'N/A')} cm / {row.get('weight','N/A')} kg")
        st.markdown(f"**Coach:** {row.get('coach','N/A')}")
        st.markdown(f"**Discipline:** {row.get('discipline','N/A')}")

st.markdown("---")

# ======================================================
# 2️⃣ Age Distribution
# ======================================================
st.markdown('<div class="section-header"><h2>📊 Age Distribution</h2></div>', unsafe_allow_html=True)

group_choice = st.selectbox("Group Age By:", ["Gender", "Discipline", "Country"])

df_plot = athletes_df.copy()
if group_choice == "Gender":
    group_col = "gender"
elif group_choice == "Discipline":
    group_col = "discipline"
elif group_choice == "Country":
    group_col = "country"

fig = px.violin(df_plot, x=group_col, y="age", box=True, points="all")
st.plotly_chart(fig, use_container_width=True)

summary = df_plot.groupby(group_col)["age"].agg(["count", "mean", "median"]).round(1)
st.dataframe(summary, use_container_width=True)

st.markdown("---")

# ======================================================
# 3️⃣ Gender Distribution
# ======================================================
st.markdown('<div class="section-header"><h2>🧍 Gender Distribution</h2></div>', unsafe_allow_html=True)

scope = st.selectbox("Filter:", ["Worldwide", "By Continent", "By Country"])

df_gender = athletes_df.copy()
title_suffix = ""

if scope == "By Continent":
    c = st.selectbox("Select Continent:", sorted(df_gender["continent"].unique()))
    df_gender = df_gender[df_gender["continent"] == c]
    title_suffix = f" in {c}"

elif scope == "By Country":
    c = st.selectbox("Select Country:", sorted(df_gender["country"].unique()))
    df_gender = df_gender[df_gender["country"] == c]
    title_suffix = f" in {c}"

gender_counts = df_gender["gender"].value_counts().reset_index()
gender_counts.columns = ["gender", "count"]

pie = px.pie(gender_counts, names="gender", values="count", title="Gender Distribution" + title_suffix)
bar = px.bar(gender_counts, x="gender", y="count")

col1, col2 = st.columns(2)
col1.plotly_chart(pie, use_container_width=True)
col2.plotly_chart(bar, use_container_width=True)

st.dataframe(gender_counts)

st.markdown("---")

# ======================================================
# 4️⃣ Top Athletes by Medals
# ======================================================
st.markdown('<div class="section-header"><h2>🥇 Top Athletes by Medal Count</h2></div>', unsafe_allow_html=True)

n = st.slider("How many athletes?", 5, 20, 10)
top_athletes = medal_counts.nlargest(n, "total_medals")

fig_top = px.bar(top_athletes, x="name", y="total_medals", color="total_medals")
st.plotly_chart(fig_top, use_container_width=True)
st.dataframe(top_athletes)

st.markdown("---")

# ======================================================
# 5️⃣ Top Countries by Continent
# ======================================================
st.markdown('<div class="section-header"><h2>🌍 Top Performing Countries</h2></div>', unsafe_allow_html=True)

continent = st.selectbox("Select Continent:", sorted(medals_total_df["continent"].unique()))
ranking = st.radio("Rank by:", ["Total", "Gold", "Silver", "Bronze"])

ranking_col = ranking
df_cont = medals_total_df[medals_total_df["continent"] == continent]
df_sorted = df_cont.nlargest(10, ranking)

fig = px.bar(df_sorted, x="country", y=ranking_col, title=f"Top Countries in {continent}")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ======================================================
# 6️⃣ Medal World Map by Type
# ======================================================
st.markdown('<div class="section-header"><h2>🗺️ Global Medal Distribution</h2></div>', unsafe_allow_html=True)

# User selects Gold / Silver / Bronze (UI)
medal_type = st.selectbox("Medal Type:", ["Gold", "Silver", "Bronze"])

# Map UI label → actual column name in CSV
real_col_map = {
    "Gold": "Gold Medal",
    "Silver": "Silver Medal",
    "Bronze": "Bronze Medal",
}

color_col = real_col_map[medal_type]  # <-- FIX HERE

fig_map = px.choropleth(
    medals_total_df,
    locations="country_code",
    locationmode="ISO-3",
    color=color_col,   # <-- MUST use real CSV column
    title=f"{medal_type} Medal Distribution",
    color_continuous_scale="YlOrBr",
)

st.plotly_chart(fig_map, use_container_width=True)


