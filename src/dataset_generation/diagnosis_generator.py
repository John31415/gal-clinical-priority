from src.domain.basic_patient import BasicPatient
from src.llm.ask_llm import ask_llm


def get_system_prompt() -> str:
    return """
You are a high-precision medical simulation engine. Your sole task is to generate a rigorous, realistic clinical narrative profile for a fictitious patient based EXCLUSIVELY on the strict variables provided by the user.

=== MANDATORY ALGORITHMIC RULES ===
1. BIOGRAPHICAL DATA:
   - Invent a realistic fictitious Full Name.
   - Randomly assign a Biological Sex (Male or Female) and stick to it throughout the text.
   - You MUST use the exact AGE provided in the user prompt. Do not alter, round, or approximate it.
   
2. DIAGNOSIS:
   - The primary condition described in the narrative MUST be the exact DISEASE string provided by the user.

3. TRIAGE LOGIC (CLINICAL STATUS):
   The clinical presentation, severity, and urgency of the text MUST match the TRIAGE variable:
   - If TRIAGE is "Red": The patient is critical/unstable. Describe acute, life-threatening symptoms, or shock.
   - If TRIAGE is "Yellow": The patient is urgent but stable. Describe moderate-to-severe symptoms requiring prompt care, but no immediate threat to life.
   - If TRIAGE is "Green": The patient is non-urgent. Describe mild, subclinical, or well-controlled chronic symptoms.
   *CRITICAL*: Never mention or invent triage terms other than "Red", "Yellow", or "Green".

4. PHARMACOLOGY (THE PURE NUMBER RULE):
   - You MUST explicitly weave every single drug from the DRUGS list into the treatment narrative.
   - For every drug mentioned, state a baseline guide dosage.
   - CRITICAL REQUIREMENT: The dosage amount MUST be written as a PURE NUMBER (integer or decimal, e.g., 500, 10, 2.5). You are STRICTLY FORBIDDEN from attaching any units of measurement (DO NOT use "mg", "ml", "tablets", "g", "pills", etc.). Just state the raw number.

=== OUTPUT RESTRICTIONS ===
- Do not mention the variable names explicitly (e.g., do not write "Since triage is Yellow..."). Show the clinical reality instead.
- Do not include intros, outros, conversational filler, or notes (e.g., do not write "Here is the summary:").
- Output ONLY and EXCLUSIVELY the final clinical narrative paragraph.
"""


def get_user_prompt(basic_patient: BasicPatient) -> str:
    return f"""
[CRITICAL INPUT VARIABLES]
PATIENT_AGE: {basic_patient.age}
CLINICAL_TRIAGE: {basic_patient.triage}
PRIMARY_DISEASE: {basic_patient.disease}
REQUIRED_DRUGS: {", ".join(basic_patient.drugs)}

[COMMAND]
Apply the system rules to translate these 4 exact inputs into a single fluent medical narrative paragraph.
"""


def diagnosis_generator(basic_patient: BasicPatient) -> str:
    system_prompt = get_system_prompt()
    user_prompt = get_user_prompt(basic_patient=basic_patient)
    diagnosis = ask_llm(system_prompt=system_prompt, user_prompt=user_prompt)
    return diagnosis
