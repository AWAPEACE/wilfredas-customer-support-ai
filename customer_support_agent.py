import os

def load_knowledge_base():
    try:
        with open("knowledge_base.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Knowledge base not found."

def main():
    print("Wilfreda's Collection Customer Support AI Agent")
    print("=" * 50)

    knowledge_base = load_knowledge_base()

    print("Knowledge base loaded successfully.")
    print(f"Knowledge base length: {len(knowledge_base)} characters")

if __name__ == "__main__":
    main()
