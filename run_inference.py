import os
import pandas as pd
from pipeline.pathway_store import build_novel_store
from pipeline.reasoning import evaluate_claim, load_model
import csv
import json

def run_inference():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    if (os.path.isfile("response.json")):
        os.remove("response.json")
    if (os.path.isfile("results.csv")):
        os.remove("results.csv")
    if (os.path.isfile("test.csv")):
        os.remove("test.csv")
    NOVEL_PATH ="data/In search of the castaways.txt"
    CSV_PATH =  "data/train.csv"
    MODEL_PATH = "model/saved_model/model.pt"
    OUTPUT_PATH = "test.csv"
    OUTPUT_PATH2 = "results.csv"

    print(" Building novel store...")
    store = build_novel_store(NOVEL_PATH)

    print(" Loading trained model...")
    model = load_model(MODEL_PATH)

    df = pd.read_csv(CSV_PATH)

    results = []
    results2=[]

    print(f" Running inference on {len(df)} rows...\n")

    for _, row in df.iterrows():
        claim_text = (
            f"Character: {row['char']}. "
            f"{row['caption']} {row['content']}"
        )

        label, rationale = evaluate_claim(claim_text, store, model)

        results.append({
            "character": row["char"],
            "claim": row["caption"],
            "judgment": "Consistent" if label else "Inconsistent",
            "confidence": rationale["confidence"],
            "evidence": " || ".join(rationale["evidence_passages"][:2])
        })
        results2.append({
            "story_id":row["id"],
            "prediction":"1" if label else "0",
            "rationale":" || ".join(rationale["evidence_passages"][:2])
        })

    #  SAVE TO test.csv (NO LABEL)
    output_df = pd.DataFrame(results)
    output_df.to_csv(OUTPUT_PATH, index=False)

    output_df2=pd.DataFrame(results2)
    output_df2.to_csv(OUTPUT_PATH2,index=False)
    csv_file = "test.csv"
    json_file = "abc.json"

    print(f" Inference complete.")
    print(f" Results saved to: {OUTPUT_PATH2}")

    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("CSV converted to JSON successfully")
    os.rename("abc.json", "response.json")
    return 
