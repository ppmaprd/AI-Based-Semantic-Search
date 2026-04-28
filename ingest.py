import json
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# -------------------------------
# CONFIG
# -------------------------------
MODEL_NAME = "all-MiniLM-L6-v2"
INPUT_FILE = "policies.json"

# -------------------------------
# LOAD MODEL
# -------------------------------
print("🔄 Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

# -------------------------------
# LOAD JSON DATA
# -------------------------------
print("📂 Loading policies...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    policies = json.load(f)

# -------------------------------
# HELPER: CHUNK TEXT
# -------------------------------
def chunk_text(text, chunk_size=120, overlap=30):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks

# -------------------------------
# PREPARE DATA
# -------------------------------
texts = []
metadata = []

print("🧩 Processing policies into chunks...")

for policy in policies:
    policy_name = policy.get("policy_name", "Unknown Policy")
    sections = policy.get("sections", {})

    for section_name, content in sections.items():
        if not content:
            continue

        chunks = chunk_text(content)

        for chunk in chunks:
            texts.append(chunk)
            metadata.append({
    "policy_name": policy_name.lower(),
    "section": section_name.lower()
})

print(f"✅ Total chunks created: {len(texts)}")

# -------------------------------
# CREATE EMBEDDINGS
# -------------------------------
print("🧠 Generating embeddings...")
embeddings = model.encode(texts, show_progress_bar=True)

# -------------------------------
# CREATE FAISS INDEX
# -------------------------------
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

# -------------------------------
# SAVE FILES
# -------------------------------
print("💾 Saving vector database...")

faiss.write_index(index, "vectordb.index")

with open("texts.pkl", "wb") as f:
    pickle.dump(texts, f)

with open("meta.pkl", "wb") as f:
    pickle.dump(metadata, f)

print("🎉 Ingestion completed successfully!")
print(f"📦 Stored {len(texts)} chunks with metadata")