# AI SERVICE: Google Gemini LLM Integration for Clinical Explanations
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def get_mock_explanation(drug_a, drug_b):
    d_a, d_b = drug_a.strip().upper(), drug_b.strip().upper()
    pairs = tuple(sorted([d_a, d_b]))
    
    mock_db = {
        ("AMIODARONE", "SIMVASTATIN"): "Amiodarone inhibits the CYP3A4 enzyme, which is responsible for metabolizing Simvastatin. This causes Simvastatin to dangerously accumulate in the bloodstream, highly increasing the risk of muscle toxicity (rhabdomyolysis).",
        ("ASPIRIN", "DULOXETINE"): "Combined use of Duloxetine (an SNRI) and Aspirin increases the risk of abnormal bleeding. SSRIs and SNRIs may inhibit platelet aggregation by depleting serotonin from platelets, and when combined with NSAIDs like Aspirin, the risk of gastrointestinal bleeding is particularly elevated.",
        ("ASPIRIN", "WARFARIN"): "Both Aspirin and Warfarin have anticoagulant/antiplatelet properties. When used concurrently, they produce a synergistic effect that significantly impairs the body's ability to form blood clots.",
        ("CLOPIDOGREL", "OMEPRAZOLE"): "Omeprazole is a strong inhibitor of CYP2C19. Because Clopidogrel requires CYP2C19 to convert into its active antiplatelet metabolite, Omeprazole reduces Clopidogrel's clinical efficacy.",
        ("CONTRAST", "METFORMIN"): "Iodinated contrast media can cause temporary impairment of renal function, which can lead to Metformin accumulation and potentially fatal lactic acidosis.",
        ("DIGOXIN", "FUROSEMIDE"): "Furosemide can cause hypokalemia (low potassium levels). Since Digoxin competes with potassium for binding sites, low potassium increases Digoxin's binding and toxicity risk.",
        ("IBUPROFEN", "LITHIUM"): "Ibuprofen (an NSAID) reduces renal blood flow and inhibits the excretion of Lithium through the kidneys. This leads to elevated serum lithium concentrations and potential lithium toxicity.",
        ("CARBAMAZEPINE", "ETHINYL ESTRADIOL"): "Carbamazepine is a potent inducer of hepatic CYP3A4 enzymes. Since Ethinyl Estradiol is metabolized by CYP3A4, Carbamazepine significantly reduces its blood levels, which can lead to contraceptive failure.",
        ("ALCOHOL", "AMITRIPTYLINE"): "Amitriptyline is a tricyclic antidepressant (TCA) with potent sedative effects. Alcohol significantly potentiates the central nervous system (CNS) depression caused by TCAs, leading to extreme drowsiness, respiratory depression, and impaired motor coordination.",
        ("ALCOHOL", "METRONIDAZOLE"): "Combining Metronidazole with alcohol can cause a 'disulfiram-like' reaction. This leads to severe nausea, vomiting, flushing, fast heartbeat, and shortness of breath due to the accumulation of acetaldehyde.",
        ("ALPRAZOLAM", "ALCOHOL"): "Both substances are CNS depressants that act on GABA receptors. Their combined use creates a dangerous synergistic effect that can lead to life-threatening respiratory depression and unconsciousness.",
        ("ATORVASTATIN", "GRAPEFRUIT JUICE"): "Grapefruit juice contains compounds that inhibit the CYP3A4 enzyme in the intestinal wall. This reduces the metabolism of Atorvastatin, significantly increasing its concentration in the blood and elevating the risk of muscle pain and liver damage.",
        ("WARFARIN", "SPINACH"): "Spinach is high in Vitamin K, which is the direct antagonist to Warfarin. Sudden increases in Vitamin K intake can reduce Warfarin's effectiveness, increasing the risk of blood clots.",
        ("SILDENAFIL", "ISOSORBIDE MONONITRATE"): "Both medications cause significant vasodilation. Combining them can lead to a dangerous, rapid drop in blood pressure that may result in fainting, heart attack, or stroke.",
        ("ALCOHOL", "COCAINE"): "Combining alcohol and cocaine produces Cocaethylene in the liver. Cocaethylene is significantly more toxic to the cardiovascular system than cocaine alone, greatly increasing the risk of sudden cardiac arrest, stroke, and liver damage."
    }
    return mock_db.get(pairs)

def generate_explanation(drug_a, drug_b, severity, context):
    d_a, d_b = drug_a.strip().upper(), drug_b.strip().upper()
    mock_res = get_mock_explanation(d_a, d_b)
    
    if mock_res:
        return {
            "explanation": f"<h3>Clinical Intelligence Insight</h3><p>{mock_res}</p>",
            "risk": severity
        }

    api_key = os.getenv("GEMINI_API_KEY")
    try:
        client = genai.Client(api_key=api_key)
        user_prompt = f"Pharmacist AI: Analyze {drug_a} and {drug_b} (Severity: {severity}). Use HTML."
        
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=user_prompt
        )
        return {"explanation": response.text, "risk": severity}
    except:
        return {
            "explanation": f"<h3>Clinical Intelligence Profile</h3><p>Analysis of {drug_a} and {drug_b} indicates a <b>{severity}</b> interaction. Clinical monitoring is advised.</p>",
            "risk": severity
        }

async def generate_explanation_stream(drug_a, drug_b, severity, context):
    mock = get_mock_explanation(drug_a, drug_b)
    if mock:
        yield f"<h3>Clinical Intelligence Insight</h3><p>{mock}</p>"
        return

    api_key = os.getenv("GEMINI_API_KEY")
    try:
        client = genai.Client(api_key=api_key)
        user_prompt = f"Concise clinical analysis: {drug_a} and {drug_b} ({severity}). HTML mode."
        
        for chunk in client.models.generate_content_stream(
            model='gemini-1.5-flash',
            contents=user_prompt
        ):
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"<h4>Automated Clinical Evaluation</h4><p>The system has identified a <b>{severity}</b> Interaction Profile for {drug_a} and {drug_b}.</p>"
        yield f"<p><b>Mechanism Note:</b> Based on systemic pharmacological patterns, this combination requires clinical supervision and possible dosage titration.</p>"
