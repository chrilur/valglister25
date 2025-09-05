import streamlit as st
import pandas as pd
from io import BytesIO

lister = pd.read_csv("valgdata/lister_og_kandidater_stortingsvalget_2025.csv", sep=";", index_col=0)

df = pd.DataFrame(lister)
df["Partinavn"] = df["Partinavn"].replace("Arbeidarpartiet", "Arbeiderpartiet")
df["Partinavn"] = df["Partinavn"].replace("Høgre", "Høyre")
df["Partinavn"] = df["Partinavn"].replace("Framstegspartiet", "Fremskrittspartiet")
df["Partinavn"] = df["Partinavn"].replace("Kristeleg Folkeparti", "Kristelig Folkeparti")
df["Partinavn"] = df["Partinavn"].replace("Miljøpartiet Dei Grøne, ", "Miljøpartiet De Grønne")
df["Partinavn"] = df["Partinavn"].replace("Raudt", "Rødt")

st.title("Valglister 2025")

# Velg valgdistrikt fra dropdown
distrikt = ["Alle"] + sorted(df["Valgdistrikt"].unique().tolist())
valgt_distrikt = st.selectbox("Valgdistrikt", distrikt)

# Velg parti fra dropdown
parti = ["Alle"] + sorted(df["Partinavn"].unique().tolist())
valgt_parti = st.selectbox("Parti", parti)

# Fritekst-søk
fritekst = st.text_input("Frisøk")

# Filtrering
filtrert_df = df.copy()
if valgt_distrikt != "Alle":
    filtrert_df = filtrert_df[filtrert_df["Valgdistrikt"] == valgt_distrikt]

if valgt_parti != "Alle":
    filtrert_df = filtrert_df[filtrert_df["Partinavn"] == valgt_parti]

if fritekst:
    filtrert_df = filtrert_df[
        filtrert_df.apply(lambda row: fritekst.lower() in row.to_string().lower(), axis=1)
    ]

st.dataframe(filtrert_df)

# ---- Eksport til Excel ----
def to_excel(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Valglister")
    return output.getvalue()

if not filtrert_df.empty:
    excel_data = to_excel(filtrert_df)
    st.download_button(
        label="📥 Last ned som Excel",
        data=excel_data,
        file_name="valglister_filtrert.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.write("Godt valg! Hilsen Samarbeidsdesken")