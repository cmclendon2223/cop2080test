import requests
import pandas as pd
import streamlit as st

st.title("Pokemon app")
names_input = input("Enter pokemon names, use commas: ") or "Charizard"

@st.cache_data 
def get_stats(name):
  r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower().strip()}")
  if r.status_code == 200:
    data = r.json()
    #print(data) # This print was for debugging and can be removed
    stats = {}
    for stat in data["stats"]:
        stat_name = stat["stat"]["name"]
        base_value = stat["base_stat"]
        stats[stat_name] = base_value
    return stats
  else:
    print(f"Error: Could not retrieve stats for '{name}'. Status code: {r.status_code}")
    return None

# Removed: print(get_stats(names_input)) 

names = [n.strip() for n in names_input.split(",") if n.strip()]
rows = {}
if st.button("Compare"):
    names = [n.strip() for n in names_input.split(",") if n.strip()]
    rows = {}
    for name in names:
        stats = get_stats(name)
        if stats:
            rows[name.title()] = stats
        else:
            st.warning(f"'{name}' not found — skipping.")
for name in names:
    if rows:
        df = pd.DataFrame(rows).T
        df.columns = [c.replace("-", " ").title() for c in df.columns]

    stats = get_stats(name)
    if stats:
        rows[name.title()] = stats # capitalize 1st letter
        print(f"rows: {rows}")
if rows:
    df = pd.DataFrame(rows).transpose()
    df.columns = [c.replace("-", " ").title() for c in df.columns]
    st.bar_chart(df)
    st.dataframe(df)



