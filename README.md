# KDSH 2026: Neural-Validated RAG Pipeline

A high-precision **Retrieval-Augmented Generation (RAG)** system built for the **Kharagpur Data Science Hackathon 2026**. It features a custom **PyTorch Consistency Model** to validate claims against a **Pathway**-indexed knowledge base.

## The Collaborators
1. **ARIT PATRA**@(https://github.com/OMORJEEVAN/)
2. **ANISH SAHA**@(https://github.com/hex32-iitkgp)

## 🛠 The Pipeline

1. **Ingestion:** Raw text is split into **400-word chunks** and stored using a `Pathway` schema.
2. **Vectorization:** Text is converted into **384-dimensional embeddings** via `all-MiniLM-L6-v2`.
3. **Neural Reasoning:** A claim is passed through a custom **MLP (Consistency Model)** to generate a confidence score .
4. **Retrieval:** Top-5 relevant passages are extracted from the vector store using **Cosine Similarity**.
5. **Final Verdict:** The system outputs a binary label (**Consistent/Contradicted**) paired with retrieved evidence rationale.

## 🧠 Neural Architecture: `ConsistencyModel`

The system uses a custom **Multi-Layer Perceptron (MLP)** for claim validation:

* **Input (384):** Aligned with Sentence-Transformer output.
* **Hidden (128):** ReLU-activated for non-linear feature mapping.
* **Regularization:** Dropout (0.3) for robust generalization.
* **Output (1):** Scalar value used for thresholding decisions.

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3 (Modern, Flexbox, Animations), JavaScript (Vanilla, Async/Await).
* **Backend:** Python (Flask/FastAPI) *[Note: Confirm your specific backend framework here].
* **Data Layer:** [Pathway](https://pathway.com/) (Schema-based streaming tables).
* **Embeddings:** `Sentence-Transformers`.
* **Inference:** `PyTorch` & `Scikit-Learn`.


## 🚀 Installation & Setup

### Prerequisites

* Python 3.12.1
* Web-Browser("Preferably Chrome")

### Steps

1. *Clone the Repository*
bash
git clone https://github.com/OMORJEEVAN/KDSH_PROJECT_2026_final.git
cd KDSH_PROJECT_2026_final



2. *Install Backend Dependencies*
bash
pip install -r requirements.txt



3. *Run the Application*
bash
python app.py



4. *Access the Interface*
Open your browser and navigate to http://localhost:5000 OR http://127.0.0.1:5000/ (or the port specified in your terminal).

## 📖 Usage Guide

1. *Upload Backstory: Click the **Database Icon* to upload your character definitions (.csv).
2. *Upload Story: Click the **Document Icon* to upload the chapter or story text (.txt).
3. *Analyze:Click **Send*.
4. *Review Results or download the results.csv file.*
    * *Green Cards* indicate behavior is consistent with the backstory.
    * *Red Cards* indicate behavior is inconsistent with the backstory.
    * Click *👁 Show Evidence* to read the specific lines that triggered the judgment.



## 📂 Project Structure

KDSH_PROJECT_2026_final/
│
├── pipeline/
├── data/
├── model/
│         "<These contain the model training NLP program and trained model.>"
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   └── index.html
│
├── uploads/
│   ├── story.txt
│   └── train.csv
│ 
├── app.py
├── readme.md
├── requirements.txt
├── response.json
├── csvtojson.py
└── run_inference.py

---

*KDSH 2026 | Team Project by *
