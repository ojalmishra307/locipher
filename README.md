# Locipher
### Decipher your genes.

Locipher is a free, patient-facing AI tool that explains genetic test results in words that actually make sense. When patients receive reports containing variants like `BRCA1 c.5266dupC`, they're often left confused and anxious. Locipher bridges the gap between complex genomic data and human understanding.

🔗 **Live at:** [locipher.streamlit.app](https://locipher.streamlit.app)

---

## The Problem

Every year, millions of patients receive genetic test reports filled with clinical terminology they don't understand. Genetic counselors are expensive and scarce. Patients are left searching the internet for answers confused, overwhelmed, and without guidance.

## The Solution

Locipher takes any genetic variant, pulls real clinical data from the ClinVar database, and uses AI to generate a warm, jargon-free explanation that any patient can understand, instantly and for free.

---

## What You Get

For any genetic variant, Locipher provides:

- ꩜ **Gene explanation** — what the gene normally does, in plain English
- ꩜ **Mutation breakdown** — what specifically went wrong
- ꩜ **Concern rating** — LOW / MODERATE / HIGH with clear reasoning
- ꩜ **Health implications** — what this means practically for your life
- ꩜ **Doctor questions** — 4 smart questions to bring to your next appointment

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Genomics Data | NCBI ClinVar API |
| AI Engine | Groq LLaMA 3.3 70B |
| Deployment | Streamlit Cloud |

---

## How to Run Locally

```bash
# Clone the repository
git clone https://github.com/ojalmishra307/locipher.git
cd locipher

# Install dependencies
pip install -r requirements.txt

# Create a .env file with your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# Run the app
streamlit run app.py
```

---

## Example Variants to Try

- `BRCA1 c.5266dupC` — Breast/ovarian cancer risk
- `TP53 R175H` — Tumor suppressor mutation
- `CFTR F508del` — Cystic fibrosis
- `APOE e4` — Alzheimer's risk factor

---

## Disclaimer

Locipher is for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified genetic counselor or physician regarding your results.

---

## Built By

**Ojal Mishra**

*Bridging the gap between genomic science and patient understanding.*