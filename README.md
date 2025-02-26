## **📖 RAG-Grammar-Enhancer**
### **An AI-powered tool for grammar correction and fluency enhancement using Retrieval-Augmented Generation (RAG).**  

🚀 **RAG-Grammar-Enhancer** combines **FAISS retrieval** and **LLM-powered text generation** to **improve English grammar, fluency, and slang-to-formal translations.**  

---

## **✨ Features**
- ✅ **Grammar Error Detection & Correction**  
- ✅ **Slang & Abbreviation Translation to Formal English**  
- ✅ **Context-Aware Sentence Restructuring**  
- ✅ **Retrieval-Augmented Generation (RAG) with FAISS for Knowledge-Based Corrections**  

---

## **📥 Installation**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/SCCSMARTCODE/RAG-Grammar-Enhancer.git
cd RAG-Grammar-Enhancer
```

### **2️⃣ Install Dependencies**
Ensure you have Python 3.8+ installed, then install required libraries:  
```bash
pip install -r requirements.txt
```

---

## **🚀 Usage**
Run the **inference script (`main.py`)** to input text and receive corrected output.  
```bash
python main.py
```

📌 **Example Interaction:**  
```plaintext
Welcome to the RAG-Grammar-Enhancer Tool!
Please enter your text: I goes to the store everyday.
Corrected Text: I go to the store every day.
```

---

## **📝 Mocked Example Interactions**
Below are **5 sample interactions** with the model.

### **🔹 Example 1: Basic Grammar Fix**
**User Input:**  
```plaintext
She go to school every day.
```
**Model Response:**  
```plaintext
Corrected Sentence: She goes to school every day.
Explanation: "Go" should be "goes" to match the singular subject "She".
Correction Type: Subject-Verb Agreement
```

---

### **🔹 Example 2: Slang to Formal English**
**User Input:**  
```plaintext
Lemme know when u free.
```
**Model Response:**  
```plaintext
Corrected Sentence: Let me know when you are free.
Explanation: "Lemme" is slang for "Let me", and "u" should be replaced with "you" for formal English.
Correction Type: Slang & Abbreviation
```

---

### **🔹 Example 3: Sentence Structure Error**
**User Input:**  
```plaintext
The email haven't been sent yet, I'll do it now.
```
**Model Response:**  
```plaintext
Corrected Sentence: The email hasn’t been sent yet; I’ll do it now.
Explanation: "Haven’t" should be "hasn’t" because "email" is singular.
Correction Type: Sentence Structure
```

---

### **🔹 Example 4: Abbreviation Expansion**
**User Input:**  
```plaintext
I'll be there ASAP, pls wait.
```
**Model Response:**  
```plaintext
Corrected Sentence: I’ll be there as soon as possible, please wait.
Explanation: "ASAP" should be expanded to "as soon as possible", and "pls" should be "please".
Correction Type: Abbreviation Errors
```

---

### **🔹 Example 5: Informal Register to Professional**
**User Input:**  
```plaintext
Yo, how's it hangin'? I need to know the time of the meeting.
```
**Model Response:**  
```plaintext
Corrected Sentence: Hello, how are you? I need to know the time of the meeting.
Explanation: "Yo, how's it hangin'?" is informal slang. A professional alternative is "Hello, how are you?".
Correction Type: Inappropriate Register
```

---

## **📌 Notes**
- The tool **retrieves knowledge from FAISS** to improve correction accuracy.  
- The model **follows structured prompts to enhance clarity & fluency.**  
- The project **no longer includes an API**—only direct inference via `main.py`.  

---

## **📜 License**
This project is **open-source** under the **[MIT License](LICENSE)**.  
