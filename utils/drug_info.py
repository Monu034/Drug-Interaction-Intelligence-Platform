# Database of drug metadata for side-by-side cards
DRUG_METADATA = {
    "ASPIRIN": {
        "class": "NSAID / Antiplatelet",
        "uses": "Pain relief, fever reduction, stroke prevention.",
        "brand": "Bayer, Ecotrin"
    },
    "WARFARIN": {
        "class": "Anticoagulant",
        "uses": "Prevention of blood clots in heart, lung, or legs.",
        "brand": "Coumadin, Jantoven"
    },
    "METFORMIN": {
        "class": "Biguanide",
        "uses": "Type 2 Diabetes management.",
        "brand": "Glucophage"
    },
    "SIMVASTATIN": {
        "class": "HMG-CoA Reductase Inhibitor",
        "uses": "Lowering cholesterol and triglycerides.",
        "brand": "Zocor"
    },
    "AMIODARONE": {
        "class": "Antiarrhythmic",
        "uses": "Heart rhythm disorders (AFib, VTach).",
        "brand": "Pacerone"
    },
    "DULOXETINE": {
        "class": "SNRI",
        "uses": "Depression, anxiety, diabetic neuropathy.",
        "brand": "Cymbalta"
    },
    "IBUPROFEN": {
        "class": "NSAID",
        "uses": "Inflammation, pain, fever.",
        "brand": "Advil, Motrin"
    },
    "LITHIUM": {
        "class": "Mood Stabilizer",
        "uses": "Bipolar disorder, manic episodes.",
        "brand": "Lithobid"
    },
    "OMEPRAZOLE": {
        "class": "Proton Pump Inhibitor",
        "uses": "GERD, heartburn, stomach ulcers.",
        "brand": "Prilosec"
    },
    "CLOPIDOGREL": {
        "class": "Antiplatelet",
        "uses": "Prevention of heart attack or stroke after recent events.",
        "brand": "Plavix"
    }
}

def get_drug_details(drug_name):
    name = drug_name.strip().upper()
    return DRUG_METADATA.get(name, {
        "class": "Pharmaceutical Agent",
        "uses": "Clinical application as per physician's guidance.",
        "brand": "Generic Available"
    })
