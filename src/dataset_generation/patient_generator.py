from src.llm.ask_llm import ask_llm
from src.domain.basic_patient import BasicPatient


def get_system_prompt() -> str:
    return """
You are a precise clinical data extraction engine. Your job is to analyze a patient's medical narrative and translate it into a structured JSON object. 

=== CLINICAL EVALUATION CRITERIA ===
You must evaluate the narrative and assign three clinical metrics as float numbers between 1.0 and 10.0 (where 1.0 is the worst/lowest and 10.0 is the best/highest):

1. `health_level`: Overall systemic stability of the patient.
   - 1.0 - 3.0: Critical condition, shock, high risk of mortality (typically correlates with Red triage).
   - 3.1 - 7.0: Moderate severity, symptomatic but stable, requires prompt care (Yellow triage).
   - 7.1 - 10.0: Mild, subclinical, or fully controlled symptoms (Green triage).

2. `deterioration_rate`: The speed or likelihood of the patient's condition worsening if left untreated.
   - 1.0 - 3.0: Low risk, stable chronic condition, or very slow progression.
   - 3.1 - 7.0: Moderate risk, requires active monitoring to prevent escalation.
   - 7.1 - 10.0: High risk, immediate physiological collapse or rapid deterioration imminent.

3. `improvement_rate`: The expected speed or capability of recovery given the current therapeutic intervention.
   - Rate this from 1.0 (minimal/slowest recovery expected) to 10.0 (rapid, highly effective recovery expected) based on the matching of the treatment to the severity of the disease.

=== DRUG EXTRACTION RULES ===
- Scan the text for every mentioned medication/drug.
- For each drug, extract its name and the accompanying raw dosage number.
- Represent the dosage as a float. If no number is mentioned for a drug, default its value to 0.0.

=== OUTPUT FORMAT ===
You MUST return ONLY a valid JSON object matching the schema below. Do not wrap the JSON in markdown code blocks (do not use ```json). Do not include any introductory text, notes, warnings, or explanations. Your entire response must start with '{' and end with '}'.

[EXPECTED JSON SCHEMA]
{
  "health_level": <float between 1.0 and 10.0>,
  "deterioration_rate": <float between 1.0 and 10.0>,
  "improvement_rate": <float between 1.0 and 10.0>,
  "drugs": [
    ["<drug_name_1>", <dosage_float_1>],
    ["<drug_name_2>", <dosage_float_2>]
  ]
}
"""


def get_user_prompt(diagnosis: str) -> str:
    return f"""
[CLINICAL NARRATIVE TO ANALYZE]
{diagnosis}

[COMMAND]
Analyze the narrative text above and extract the JSON object according to the system rules. Do not print anything else.
"""


def json_patient_generator(diagnosis: str) -> str:
    system_prompt = get_system_prompt()
    user_prompt = get_user_prompt(diagnosis)
    patient_json = ask_llm(system_prompt=system_prompt, user_prompt=user_prompt)
    return patient_json
