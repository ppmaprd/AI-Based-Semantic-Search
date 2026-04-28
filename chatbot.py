import faiss
import pickle
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from datetime import datetime
import json

# -------------------------------
# INIT
# -------------------------------
client = OpenAI(api_key="api_key")

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("vectordb.index")

with open("texts.pkl", "rb") as f:
    texts = pickle.load(f)

with open("meta.pkl", "rb") as f:
    metadata = pickle.load(f)

# -------------------------------
# HELPERS
# -------------------------------
def normalize(text):
    return text.lower().strip()

# -------------------------------
# POLICY / SECTION DETECTION
# -------------------------------
POLICIES = [normalize(p) for p in [
    "Risk Assessment Policy","Access Control Policy","Incident Management Policy",
    "Data Classification Policy","Vendor Risk Management Policy","Password Management Policy",
    "Backup and Recovery Policy","Secure Development Policy","Logging and Monitoring Policy",
    "Business Continuity Policy","Network Security Policy","Endpoint Security Policy",
    "Change Management Policy","Asset Management Policy","Encryption Policy",
    "Mobile Device Policy","Physical Security Policy","Email Security Policy"
]]

SECTION_MAP = {
    "purpose": "purpose",
    "scope": "scope",
    "roles": "roles",
    "responsibilities": "roles",
    "inputs": "inputs",
    "outputs": "outputs",
    "compliance": "compliance",
    "review": "review",
    "records": "records"
}

def detect_policy(query):
    q = normalize(query)
    for p in POLICIES:
        if p in q:
            return p
    return None

def detect_section(query):
    q = normalize(query)
    for k, v in SECTION_MAP.items():
        if k in q:
            return v
    return None

# -------------------------------
# MAIN FUNCTION
# -------------------------------
def chatbot_response(query):

    query_norm = normalize(query)

    policy = detect_policy(query_norm)
    section = detect_section(query_norm)

    # -------------------------------
    # RETRIEVE (FAISS)
    # -------------------------------
    query_vec = model.encode([query])
    distances, indices = index.search(query_vec, 10)

    retrieved = []

    # -------------------------------
    # STEP 1: FLEXIBLE FILTER
    # -------------------------------
    for i in indices[0]:
        meta = metadata[i]

        meta_policy = normalize(meta["policy_name"])
        meta_section = normalize(meta["section"])

        if policy and policy not in meta_policy:
            continue

        if section:
            if section not in meta_section and meta_section not in section:
                continue

        retrieved.append({
            "text": texts[i],
            "policy": meta["policy_name"],
            "section": meta["section"]
        })

    # -------------------------------
    # STEP 2: RELAX SECTION FILTER
    # -------------------------------
    if not retrieved and policy:
        for i in indices[0]:
            meta = metadata[i]
            meta_policy = normalize(meta["policy_name"])

            if policy in meta_policy:
                retrieved.append({
                    "text": texts[i],
                    "policy": meta["policy_name"],
                    "section": meta["section"]
                })

    # -------------------------------
    # STEP 3: FULL FALLBACK
    # -------------------------------
    if not retrieved:
        for i in indices[0][:5]:
            meta = metadata[i]
            retrieved.append({
                "text": texts[i],
                "policy": meta["policy_name"],
                "section": meta["section"]
            })

    # -------------------------------
    # FINAL CHECK
    # -------------------------------
    if not retrieved:
        return "⚠️ No relevant information found in the available security policies."

    # -------------------------------
    # STEP 4: SECTION BOOSTING (CRITICAL FIX)
    # -------------------------------
    if section:
        section_matches = [
            r for r in retrieved if section in normalize(r["section"])
        ]
        other_matches = [
            r for r in retrieved if section not in normalize(r["section"])
        ]
        retrieved = section_matches + other_matches

    # -------------------------------
    # BUILD CONTEXT
    # -------------------------------
    context = "\n\n".join([r["text"] for r in retrieved[:6]])

    # -------------------------------
    # CORRECT SECTION LABEL
    # -------------------------------
    section_label = section if section else retrieved[0]["section"]

    # -------------------------------
    # PROMPT (SMART RAG)
    # -------------------------------
    prompt = f"""
You are an Information Security Compliance Assistant.

RULES:
- Use the context to answer the question
- Prefer the requested section if available
- If exact match is not found, give closest relevant answer
- Do NOT say "No relevant information found" unless context is completely unrelated

Context:
{context}

Question:
{query}

Format strictly as:

[Policy]: {retrieved[0]["policy"]}
[Section]: {section_label}
[Answer]:
[Source]: Based on provided policy content
"""

    # -------------------------------
    # GENERATE
    # -------------------------------
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    answer = response.choices[0].message.content

    # -------------------------------
    # AUDIT LOG
    # -------------------------------
    log = {
        "timestamp": str(datetime.now()),
        "query": query,
        "detected_policy": policy,
        "detected_section": section,
        "retrieved_chunks": retrieved[:5],
        "response": answer
    }

    with open("audit_log.json", "a") as f:
        f.write(json.dumps(log) + "\\n")

    return answer