import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModel
from consistency_model import ConsistencyModel
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

tokenizer = AutoTokenizer.from_pretrained(
    "sentence-transformers/all-MiniLM-L6-v2"
)
encoder = AutoModel.from_pretrained(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def embed(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )
    with torch.no_grad():
        outputs = encoder(**inputs)

    token_embeddings = outputs.last_hidden_state
    attention_mask = inputs["attention_mask"].unsqueeze(-1)

    masked = token_embeddings * attention_mask
    summed = masked.sum(dim=1)
    counts = attention_mask.sum(dim=1)

    emb = summed / counts
    return F.normalize(emb, dim=1)

df = pd.read_csv("data/train.csv")

X, y = [], []

for _, row in df.iterrows():
    combined = (
        f"Character: {row['char']}. "
        f"{row['caption']} {row['content']}"
    )
    X.append(embed(combined))
    y.append(1 if row["label"] == "consistent" else 0)

X = torch.cat(X)
y = torch.tensor(y).float().unsqueeze(1)

num_pos = y.sum()
num_neg = len(y) - num_pos

pos_weight = torch.tensor([num_neg / num_pos])

model = ConsistencyModel()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = torch.nn.BCEWithLogitsLoss(pos_weight=pos_weight)

dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=16, shuffle=True)

for epoch in range(100):
    total_loss = 0

    for xb, yb in loader:
        optimizer.zero_grad()
        logits = model(xb)
        loss = loss_fn(logits, yb)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1} | Loss: {total_loss / len(loader):.4f}")

torch.save(model.state_dict(), "model/saved_model/model.pt")
print(" Model trained and saved.")