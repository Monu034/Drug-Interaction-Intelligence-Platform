import pandas as pd


# LOAD DATA
df1 = pd.read_csv("DS1.csv")
df3 = pd.read_csv("DS3.csv")


# CLEAN DS1

df1 = df1.rename(columns={
    "Drug 1": "drug_a",
    "Drug 2": "drug_b",
    "Interaction Description": "description"
})

def infer_severity(text):
    text = str(text).lower()
    if "severe" in text or "toxicity" in text or "contraindicated" in text:
        return "Severe"
    elif "increase" in text or "risk" in text:
        return "Moderate"
    elif "decrease" in text:
        return "Mild"
    else:
        return "Mild"

df1["severity"] = df1["description"].apply(infer_severity)
df1 = df1[["drug_a", "drug_b", "severity", "description"]]


# CLEAN DS3 (AUTO DETECT COLUMNS)

df3.columns = [col.lower() for col in df3.columns]

# Try to detect columns automatically
drug_a_col = None
drug_b_col = None
desc_col = None
sev_col = None

for col in df3.columns:
    if "drug" in col and drug_a_col is None:
        drug_a_col = col
    elif "drug" in col and drug_b_col is None:
        drug_b_col = col
    elif "desc" in col or "interaction" in col:
        desc_col = col
    elif "severity" in col:
        sev_col = col

# Fallbacks (in case names are weird)
if not drug_a_col or not drug_b_col:
    cols = df3.columns.tolist()
    drug_a_col, drug_b_col = cols[0], cols[1]

if not desc_col:
    desc_col = df3.columns[-1]

# Rename properly
df3 = df3.rename(columns={
    drug_a_col: "drug_a",
    drug_b_col: "drug_b",
    desc_col: "description"
})

# Handle severity — standardise labels if column exists
severity_map = {
    "major": "Severe",
    "moderate": "Moderate",
    "minor": "Mild",
    "mild": "Mild",
    "severe": "Severe",
    "contraindicated": "Contraindicated",
}

if sev_col:
    df3 = df3.rename(columns={sev_col: "severity"})
    df3["severity"] = (
        df3["severity"]
        .astype(str)
        .str.lower()
        .str.strip()
        .map(severity_map)
        .fillna("Mild")
    )
else:
    df3["severity"] = df3["description"].apply(infer_severity)

df3 = df3[["drug_a", "drug_b", "severity", "description"]]


# MERGE

df_final = pd.concat([df1, df3], ignore_index=True)


# CLEAN FINAL

df_final["drug_a"] = df_final["drug_a"].astype(str).str.lower().str.strip()
df_final["drug_b"] = df_final["drug_b"].astype(str).str.lower().str.strip()

df_final = df_final.dropna()
df_final = df_final.drop_duplicates(subset=["drug_a", "drug_b"])

# Ensure all severity values are in the allowed set (catch anything missed)
allowed = {"Severe", "Moderate", "Mild", "Contraindicated"}
df_final["severity"] = df_final["severity"].where(
    df_final["severity"].isin(allowed), other="Mild"
)


# SAVE

df_final.to_csv("final_dataset.csv", index=False)

# CHECK

print("✅ DONE — final_dataset.csv created\n")
print(df_final.head())
print("\n📊 Severity Distribution:\n")
print(df_final["severity"].value_counts())
print("\n📐 Shape:", df_final.shape)