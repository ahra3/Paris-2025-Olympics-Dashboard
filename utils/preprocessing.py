import os
import pandas as pd
import pycountry
import pycountry_convert as pc
import unicodedata
import re

# ---------------------------------------
# Paths
# ---------------------------------------
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# ---------------------------------------
# Continent mapping
# ---------------------------------------
SPECIAL_NOC_CONTINENTS = {
    "AIN": "Other",
    "EOR": "Other",
    "TPE": "Asia",
    "GBR": "Europe",
    "ROC": "Europe",
}

def get_continent_from_noc(noc):
    """Convert NOC → continent."""
    try:
        if noc in SPECIAL_NOC_CONTINENTS:
            return SPECIAL_NOC_CONTINENTS[noc]

        country = pycountry.countries.get(alpha_3=noc)
        if country is None:
            return "Other"

        alpha2 = country.alpha_2
        cont = pc.country_alpha2_to_continent_code(alpha2)

        mapping = {
            "AF": "Africa",
            "NA": "Americas",
            "SA": "Americas",
            "EU": "Europe",
            "AS": "Asia",
            "OC": "Oceania",
            "AN": "Antarctica",
        }
        return mapping.get(cont, "Other")
    except:
        return "Other"

def add_continent_column(df, col="country_code"):
    df = df.copy()
    df["continent"] = df[col].apply(get_continent_from_noc)
    return df

# ---------------------------------------
# Clean Medal Type
# ---------------------------------------
def clean_medal_type(df, col="medal_type"):
    df = df.copy()
    mapping = {
        "Gold Medal": "Gold", "GOLD": "Gold", "Gold": "Gold",
        "Silver Medal": "Silver", "SILVER": "Silver", "Silver": "Silver",
        "Bronze Medal": "Bronze", "BRONZE": "Bronze", "Bronze": "Bronze",
    }
    if col in df.columns:
        df[col] = df[col].map(mapping).fillna(df[col])
    return df

# ---------------------------------------
# Main Preprocessing Function
# ---------------------------------------
def prepare_medals_datasets():
    """Loads and preprocesses medals_total, medallists, medals."""

    medals_total = pd.read_csv(os.path.join(DATA_DIR, "medals_total.csv"))
    medallists = pd.read_csv(os.path.join(DATA_DIR, "medallists.csv"))
    medals = pd.read_csv(os.path.join(DATA_DIR, "medals.csv"))

    # Clean totals
    medals_total = medals_total.rename(columns={
        "Gold Medal": "Gold",
        "Silver Medal": "Silver",
        "Bronze Medal": "Bronze"
    })
    medals_total = add_continent_column(medals_total)

    

    # Clean medallists
    medallists = clean_medal_type(medallists)
    medallists = add_continent_column(medallists)

    # Clean medals
    medals = clean_medal_type(medals)
    medals = add_continent_column(medals)

    return medals_total, medallists, medals





def normalize_name(name):
    if not isinstance(name, str):
        return ""
    # Remove accents
    name = ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    )
    # Lowercase
    name = name.lower()
    # Remove punctuation
    name = re.sub(r"[^a-zA-Z\s]", "", name)
    # Split and sort words (fixes reversed names)
    parts = name.split()
    parts.sort()
    return " ".join(parts)
