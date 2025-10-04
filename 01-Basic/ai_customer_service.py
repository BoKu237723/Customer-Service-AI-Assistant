import ollama
import json

def load_packages():
    try:
        with open('packages.json', 'r', encoding = 'utf-8') as f:
            data = json.load(f)
        return data['plans']
    except Exception as e:
        print(f"❌ Error loading packages: {e}")
        return []
    
def ai_prompt(packages):
    packages_text = json.dumps(packages, indent = 2)
    return f"""
You are a professional customer service AI for a web design company. 
Your job is to help clients choose the best website package based on their needs.

CURRENT PACKAGES AVAILABLE:
{packages_text}

GUIDELINES:
1. Always recommend based on the client's specific business needs
2. Mention exact prices and features from the package data
3. Be honest about limitations
4. Suggest the most cost-effective option that meets their requirements
5. If unsure, ask clarifying questions

IMPORTANT: Only recommend packages that exist in the data above. Never make up packages or prices.
"""

def get_ai_response(user_question, packages):
    system_prompt = ai_prompt(packages)
    try:
        response = ollama.chat(model = 'llama3.1:8b', messages = [
            {
                'role' : 'system',
                'content' : system_prompt
            },
            {
                'role' : 'user',
                'content' : user_question
            }
        ])
        return response['message'] ['content']
    except Exception as e:
        return f"❌ Error getting AI response: {e}"
    
def display_packages(packages):
    print("\n📦 AVAILABLE PACKAGES: ")
    print("-"*50)
    for i, package in enumerate(packages, 1):
        print(f"{i}. {package['name']} - {package['price']}")
        print(f"Pages: {[f for f in package['features'] if 'page' in f.lower() or 'Page' in f]}")
        print(f"Key Features: {', '.join(package['features'][:3])}")
        print()

def main():
    print("Welcome to the AI Customer Service for Web Design Packages!")
    print("=" *60)

    packages = load_packages()
    if not packages:
        print("No packages available. Exiting.")
        return
    print("Here are the available packages:")
    display_packages(packages)

    while True:
        print("\n" + "=" *60)
        print("How can I assist you today?")
        print("Type 'exit' to quit.")
        print("Type 'packages' to see the available packages again.")
        user_input = input("Your question: ")
        if user_input.lower() in ['exit']:
            print("Thank you for using the AI Customer Service. Goodbye!")
            break
        elif user_input.lower() in ['packages']:
            display_packages(packages)
            continue
        elif not user_input:
            continue

        print("Getting recommendation...")
        recommendation = get_ai_response(user_input, packages)
        print(recommendation)

        print("=" *60)

if __name__ == "__main__":
    main()