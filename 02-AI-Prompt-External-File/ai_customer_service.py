import ollama
import json

def load_packages():
    try:
        with open('packages.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['plans']
    except Exception as e:
        print(f"Error in loading packages: {e}")
        return[]
    
def load_ai_prompt(packages):
    try:
        with open('ai_prompt.txt','r',encoding='utf-8') as f:
            prompt_template = f.read()
            packages_text = json.dumps(packages, indent=2)
        return prompt_template.replace('{packages_text}', packages_text)
    except Exception as e:
        print("Error in loading ai prompt: {e}")
        return None
    
def get_ai_recommendation(user_question, package):
    system_prompt = load_ai_prompt(package)
    if not system_prompt:
        return f"AI Prompt not available."
    
    try:
        response = ollama.chat(model='llama3.1:8b', messages=[
            {
                "role" : "system",
                "content" : system_prompt
            },
            {
                "role" : "user",
                "content" : user_question
            }
        ])
        return response['message']['content']
    except Exception as e:
        return f"Error in getting AI response: {e}"

def display_summary(packages):
    print("PACKAGE SUMMARY: ")
    for p in packages:
        print(f"{p['name']}: {p['price']}")
    
def display_packages(packages):
    print("AVAILABLE PACKAGES:")
    print("=" *60)
    for i, package in enumerate(packages, 1):
        print(f"{i}. {package['name']} - {package['price']}")
        print(f"Type : {package['type']}")
        pages = [f for f in package['features'] if 'page' in f.lower()]
        print(f"Pages: {pages}")
        print(f"Key Features: {', '.join(package['features'])}")
        print(f"Support: {package.get('support','N/A')}")
        print(f"Updates: {package.get('updates','N/A')}")
        print(f"Notes: {package.get('note','')}")
        print("-"*60)

def main():
    print("AI CUSTOMER PACKAGE ADVISOR")
    print("=" *60)
    packages = load_packages()

    if not packages:
        print("Packages are not loaded!")
        return None
    
    print(f"Loaded {len(packages)} packages from packages.json")
    display_packages(packages)

    while True:
        print("\n"+"=" *60)
        print("How can I assist you today?")
        print("Commands: 'exit', 'packages','summary','help")
        print("=" * 60)

        user_input = input("\n Describe your business needs: ")
        if not user_input:
            continue

        if user_input.lower() == 'exit':
            print("Good Bye!")
            break
        elif user_input.lower() == 'packages':
            display_packages(packages)
            continue
        elif user_input.lower() == 'summary':
            display_summary(packages)
            continue
        elif user_input.lower() == 'help':
            print("Commands: 'exit', 'packages','summary','help")
            continue

        keywords = [word.lower() for word in user_input.split()]
        print("Packages matching your keywords: ")
        for package in packages:
            matched_features = [f for f in package['features'] if any (k in f.lower() for k in keywords)]
            if matched_features:
                print(f"{package['name']} -> {matched_features}\n")
            
        print("AI Recommendation: ")
        print("-"*40)
        recommendation = get_ai_recommendation(user_input, packages)
        print(recommendation)
        print("\n")

if __name__ == "__main__":
    main()