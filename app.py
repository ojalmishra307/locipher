import streamlit as st
import requests
import re
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
def is_valid_variant(variant):
    if len(variant) < 4:
        return False
    if not re.search(r'\d', variant) and not re.search(r'[A-Z][a-z]', variant):
        return False
    return True

def fetch_variant_data(variant):
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "clinvar", "term": variant, "retmax": 1, "retmode": "json"}
    response = requests.get(search_url, params=params)
    data = response.json()
    ids = data["esearchresult"]["idlist"]
    if not ids or data["esearchresult"]["count"] == "0":
        return None
    variant_id = ids[0]
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params2 = {"db": "clinvar", "id": variant_id, "retmode": "json"}
    response2 = requests.get(fetch_url, params=params2)
    summary = response2.json()
    try:
        result = summary["result"][variant_id]
        gene = result.get("gene_sort", "Unknown")
        significance = result.get("clinical_significance", {}).get("description", "Unknown")
        if gene == "Unknown" and significance == "Unknown":
            return None
        return {
            "variant_name": result.get("title", "Unknown"),
            "clinical_significance": significance,
            "review_status": result.get("clinical_significance", {}).get("review_status", "Unknown"),
            "conditions": [trait.get("trait_name", "") for trait in result.get("trait_set", [])],
            "gene": gene,
            "variant_type": result.get("obj_type", "Unknown"),
            "last_evaluated": result.get("clinical_significance", {}).get("last_evaluated", "Unknown"),
            "accession": result.get("accession", "Unknown")
        }
    except:
        return None

def explain_variant(variant_data, variant_name):
    prompt = f"""You are a warm, expert genetic counselor explaining a patient's genetic test result. The patient has no biology background and is anxious about their results.

IMPORTANT: If the gene and clinical significance are both Unknown, respond only with: "This variant could not be found in our database. Please check the format and try again." Do not make up information.

Here is the clinical data about their variant:
- Variant: {variant_name}
- Gene affected: {variant_data.get('gene', 'Unknown')}
- Clinical significance: {variant_data.get('clinical_significance', 'Unknown')}
- Associated conditions: {', '.join(variant_data.get('conditions', [])) or 'None listed'}
- Review status: {variant_data.get('review_status', 'Unknown')}
- Last evaluated: {variant_data.get('last_evaluated', 'Unknown')}

Write a response with these exact sections:

**What is this gene?**
Explain what this gene normally does in the body in 2-3 simple sentences. Use an everyday analogy.

**What does this mutation mean?**
Explain what specifically went wrong in simple terms. No jargon.

**How concerned should I be?**
Based on the clinical significance, give an honest but calm assessment. Use LOW / MODERATE / HIGH concern rating with a one line explanation.

**What could this mean for my health?**
List 2-3 practical health implications based on the associated conditions. Be specific but not scary.

**Questions to ask your doctor:**
List exactly 4 specific, smart questions this patient should bring to their next appointment.

Be warm, human, and specific. Work with what's provided."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )
    return response.choices[0].message.content

st.set_page_config(page_title="locipher", layout="centered")

st.markdown("""
    <style>
    ... all your existing CSS ...
    
    [data-baseweb="input"] {
        border-radius: 100px !important;
        border: 1.5px solid rgba(96,71,52,0.2) !important;
        box-shadow: none !important;
    }
    [data-baseweb="base-input"] {
        background-color: #604734 !important;
        border-radius: 100px !important;
    }
    .stButton > button {
        color: #fcf7d9 !important;
        background-color: #604734 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("# locipher")
st.markdown("### Decipher your *genes.*")
st.markdown("Paste any variant from your genetic report and get a clear, human explanation.")

st.markdown("""
    <div style="display:flex; justify-content:center; gap:60px; padding:24px; background:#ffffff; border-radius:16px; border:1px solid rgba(96,71,52,0.08); margin:16px 0 24px 0;">
        <div style="text-align:center;">
            <div style="font-size:24px; font-weight:700; color:#604734;">1M+</div>
            <div style="font-size:12px; color:#8a6a58;">Variants in ClinVar</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:24px; font-weight:700; color:#604734;">AI</div>
            <div style="font-size:12px; color:#8a6a58;">Powered Explanations</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:24px; font-weight:700; color:#604734;">Instant</div>
            <div style="font-size:12px; color:#8a6a58;">First Patient-Facing Tool</div>
        </div>
    </div>
""", unsafe_allow_html=True)

variant_input = st.text_input("Enter your genetic variant", placeholder="e.g. BRCA1 c.5266dupC, TP53 R175H, CFTR F508del")
decode_btn = st.button("Decode My Variant")

if decode_btn:
    if variant_input:
        if not is_valid_variant(variant_input):
            st.error("Please enter a valid genetic variant. Example formats: BRCA1 c.5266dupC, TP53 R175H, CFTR F508del")
        else:
            with st.spinner("Searching ClinVar database..."):
                raw_data = fetch_variant_data(variant_input)
            if raw_data:
                with st.spinner("Generating your explanation..."):
                    explanation = explain_variant(raw_data, variant_input)
                st.markdown("---")
                st.markdown("### Your Results")
                st.markdown(explanation)
                st.markdown("---")
            else:
                st.error("Variant not found. Try format: BRCA1 c.5266dupC")
    else:
        st.warning("Please enter a variant first.")

st.markdown("""
    <div style="text-align:center; color:#b8a09a; font-size:12px; padding:40px 0 20px 0;">
        Locipher is for educational purposes only. Always consult a qualified doctor or genetic counselor.<br><br>
        Built by Ojal · Powered by ClinVar + Groq AI
    </div>
""", unsafe_allow_html=True)