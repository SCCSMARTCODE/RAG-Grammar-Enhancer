import json
import os
from dotenv import load_dotenv
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

JSON_FORMAT_DATA_PATH = "../data/json_format"
N_LISTS = 100  # Number of Voronoi cells (for large datasets, increase this)

load_dotenv()

def get_sentences():
    sentence_list = []

    for file in os.listdir(JSON_FORMAT_DATA_PATH):
        full_path = os.path.join(JSON_FORMAT_DATA_PATH, file)

        with open(full_path, "r", encoding="utf-8") as f:
            json_type_data = json.load(f)

            if isinstance(json_type_data, list):
                for datapoint in json_type_data:
                    text = ""

                    if "Error Type" in datapoint and "Ungrammatical Statement" in datapoint and "Standard English" in datapoint:
                        text = (
                            f"Error Type: {datapoint['Error Type']}. "
                            f"Incorrect: {datapoint['Ungrammatical Statement']} "
                            f"Correct: {datapoint['Standard English']}."
                        )

                    elif "idioms" in datapoint and "meaning" in datapoint:
                        text = f"Idiom: {datapoint['idioms']}. Meaning: {datapoint['meaning']}."

                    if text:
                        sentence_list.append(text.strip())

            elif isinstance(json_type_data, dict):
                for key, value in json_type_data.items():
                    text = f"Slang: {key}. Meaning: {value}."
                    sentence_list.append(text.strip())

    return sentence_list


def retrieve_best_match(user_input, top_k=1):
    stored_index = faiss.read_index("./models/knowledge_base.faiss")

    with open("./models/sentence_mappings.txt", "r", encoding="utf-8") as f:
        stored_sentences = f.readlines()

    myModel = SentenceTransformer("all-MiniLM-L6-v2")

    query_embedding = myModel.encode([user_input])

    if not stored_index.is_trained:
        raise ValueError("FAISS index is not trained!")

    D, I = stored_index.search(np.array(query_embedding), k=top_k)

    return [stored_sentences[i].strip() for i in I[0] if i != -1]


def correct_grammar(input_text):
    import requests

    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
    HEADERS = {"Authorization": f"Bearer {os.getenv("LMM_API_KEY", " ")}"}

    prompt = generate_prompt(input_text)

    payload = {
        "inputs": prompt,
        "parameters": {
            "return_full_text": False,
            "temperature": 0.85
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()[0].get("generated_text", input_text)

def generate_prompt(input_text):
    retrieved_data = "\n".join(retrieve_best_match(input_text, 5))
    prompt = f"""
            [System Instruction Begin]
            You are an AI assistant specializing in **correcting grammar, fluency, and slang-to-formal translations**.

            ### Task:
            1. **Identify the issue in the given input** (grammar mistake, slang, abbreviation, sentence structure, etc.).
            2. **Correct the sentence in formal English** while preserving the original meaning.
            3. **Use the reference data below only if relevant**—it is for guidance, not a strict rule.
            4. **If the reference data is not useful, ignore it and provide your own correction.**

            ### Input Sentence:
            "{input_text}"

            ### Reference Data (Optional):
            "{retrieved_data}"

            ### Expected Response Format:
            - **Corrected Sentence:** [Your correction here]
            - **Explanation:** [Brief reason for the correction]
            - **Correction Type:** (Grammar, Slang, Abbreviation, etc.)

            [System Instruction End]
        """
    return prompt



if __name__ == "__main__":
    model = SentenceTransformer("all-MiniLM-L6-v2")

    strings = get_sentences()

    embeddings = model.encode(strings)

    # Get embedding dimensions
    dimension = embeddings.shape[1]

    # Create an IVF index (IVF + L2 distance metric)
    quantizer = faiss.IndexFlatL2(dimension)
    index = faiss.IndexIVFFlat(quantizer, dimension, N_LISTS, faiss.METRIC_L2)

    index.train(np.array(embeddings))
    index.add(np.array(embeddings))

    # Save FAISS index to file
    faiss.write_index(index, "knowledge_base.faiss")
    print("FAISS index saved successfully!")

    # Save sentences for later retrieval mapping
    with open("sentence_mappings.txt", "w", encoding="utf-8") as f:
        for sentence in strings:
            f.write(sentence + "\n")