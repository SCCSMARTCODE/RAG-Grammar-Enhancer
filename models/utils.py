import json
import os

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

JSON_FORMAT_DATA_PATH = "../data/json_format"
N_LISTS = 100  # Number of Voronoi cells (for large datasets, increase this)



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
    stored_index = faiss.read_index("knowledge_base.faiss")

    with open("sentence_mappings.txt", "r", encoding="utf-8") as f:
        stored_sentences = f.readlines()

    myModel = SentenceTransformer("all-MiniLM-L6-v2")

    query_embedding = myModel.encode([user_input])

    if not stored_index.is_trained:
        raise ValueError("FAISS index is not trained!")

    D, I = stored_index.search(np.array(query_embedding), k=top_k)

    return [stored_sentences[i].strip() for i in I[0] if i != -1]


def correct_grammar(input_text):
    return input_text



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