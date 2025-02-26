from models.utils import correct_grammar

def main():
    print("Welcome to the RAG-Grammar-Enhancer Tool!")
    user_input = input("Please enter your text: ")

    corrected_output = correct_grammar(user_input)
    print("Corrected Text:", corrected_output)


if __name__ == "__main__":
    main()