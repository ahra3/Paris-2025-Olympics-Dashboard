import streamlit as st
import pandas as pd

def global_filters(df_base: pd.DataFrame):
    """
    Global sidebar filters:
    - Continent
    - Country
    - Sport / Discipline
    - Medal type
    - Gender (if exists)
    """

    with st.sidebar:
        st.header("🌍 Global Filters")

        # -------- 1. Continent Filter --------
        if "continent" in df_base.columns:
            continents = sorted(df_base["continent"].dropna().unique())
            selected_continents = st.multiselect(
                "Continent:", continents, default=continents
            )
        else:
            selected_continents = None

        # -------- 2. Country Filter --------
        if "country_code" in df_base.columns:
            country_col = "country_code"
        elif "country" in df_base.columns:
            country_col = "country"
        else:
            country_col = df_base.columns[0]  # fallback

        countries = sorted(df_base[country_col].dropna().unique())
        selected_countries = st.multiselect(
            "Country (NOC):",
            options=countries,
            default=countries
        )

        # -------- 3. Sport / Discipline Filter --------
        if "discipline" in df_base.columns:
            sport_col = "discipline"
        elif "sport" in df_base.columns:
            sport_col = "sport"
        else:
            sport_col = None

        if sport_col:
            sports = sorted(df_base[sport_col].dropna().unique())
            selected_sports = st.multiselect(
                "Sport / Discipline:", sports, default=sports
            )
        else:
            selected_sports = None

        # -------- 4. Medal Types --------
        medal_types = ["Gold", "Silver", "Bronze"]
        selected_medal_types = [
            m for m in medal_types if st.checkbox(m, value=True, key=f"medal_{m}")
        ]

        # -------- 5. Gender Filter --------
        if "gender" in df_base.columns:
            genders = sorted(df_base["gender"].dropna().unique())
            selected_genders = st.multiselect(
                "Gender:",
                options=genders,
                default=genders
            )
        else:
            selected_genders = None

    return {
        "continent": selected_continents,
        "country_col": country_col,
        "selected_countries": selected_countries,
        "sport_col": sport_col,
        "selected_sports": selected_sports,
        "selected_medal_types": selected_medal_types,
        "selected_genders": selected_genders,
    }


def apply_global_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    df_f = df.copy()

    # Continent
    if "continent" in df_f.columns and filters["continent"]:
        df_f = df_f[df_f["continent"].isin(filters["continent"])]

    # Country
    if filters["selected_countries"]:
        df_f = df_f[df_f[filters["country_col"]].isin(filters["selected_countries"])]

    # Sport / Discipline
    if filters["sport_col"] and filters["selected_sports"]:
        df_f = df_f[df_f[filters["sport_col"]].isin(filters["selected_sports"])]

    # Medal Type
    if "medal_type" in df_f.columns and filters["selected_medal_types"]:
        df_f = df_f[df_f["medal_type"].isin(filters["selected_medal_types"])]

    # Gender
    if "gender" in df_f.columns and filters["selected_genders"]:
        df_f = df_f[df_f["gender"].isin(filters["selected_genders"])]

    return df_f
