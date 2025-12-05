from utils.preprocessing import prepare_medals_datasets, normalize_name
from utils.filters import global_filters, apply_global_filters
import pandas as pd
import os

DATA = os.path.join(os.path.dirname(__file__), "data")

athletes = pd.read_csv(f"{DATA}/athletes.csv")

print("Does Remco exist in athletes.csv?")
print(athletes[athletes["name"].str.contains("Remco", case=False, na=False)])

print("\n👉 NORMALIZED name:")
print(normalize_name("EVENEPOEL Remco"))
