import ollama
import json

class PackageAdvisor:
    def __init__(self):
        self.packages = []
        self.other_services = []
        self.unavailable_services = []

    def load_data(self):
        try:
            with open('01-frontend-services.json','r', encoding='utf-8') as f:
                frontend_data = json.load(f)
                self.packages = frontend_data.get('plans',[])
            with open('02-other-services.json','r',encoding='utf-8') as f:
                other_services = json.load(f)
                self.other_services = other_services.get('other_services',[])
            with open('03-unavailable-services.json','r',encoding='utf-8') as f:
                unavailable_services = json.load(f)
                self.unavailable_services.get('unavailable_services',[])
            print(f"Loaded {len(self.packages)} packages, {len(self.other_services)} services, {len(self.unavailable_services)} unavailable services.")
            return True
        except Exception as e:
            print(f"Error in Loading data: {e}")

    def load_ai_prompt(self):
        try:
            with open('ai_prompt.txt','r',encoding='utf-8') as f:
                prompt_template = f.read()

            package_text = json.dumps(self.packages, indent=2, ensure_ascii=False)
            return prompt_template.replace('{packages_text}',package_text)
        except Exception as e:
            print(f"Error loading AI prompt: {e}")
            return None
        
    def get_ai_recommendation(self,user_question):
        system_prompt = self.load_ai_prompt()

        if not system_prompt:
            return f"Loading AI prompt is not available."
        
        try:
            response = ollama.chat(model='llama3.1:8b',messages=[
                {
                    'role' : 'system',
                    'content' : system_prompt
                },
                {
                    'role' : 'user',

                    'content' : user_question
                }
            ])
            return response['message','content']
        except Exception as e:
            print(f"Error in gettting AI recommendation: {e}")
            return[]
    
    def display_summary(self):
        print("PACKAGE SUMMARY")
        print("=" * 30)
        for package in self.packages:
            print(f"{package['name']} - {package['price']}")
        print("="*30)

    def display_packages(self):
        print("AVAILABLE PACKAGES")
        print("="*30)

        for i, package in enumerate(self.packages, 1):
            print(f"{i}. {package['name']} - {package['price']}")
            print(f"      Type : {package['type']}")
            pages = [f for f in package['features'] if 'page' in f.lower()]
            if pages:
                print(f"   Pages: {', '.join(pages)}")
            
            key_features = package['features']
            print(f"   Key Features: {', '.join(key_features)}")
            print(f"   Support: {package.get('support','N/A')}")
            print(f"   Updates: {package.get('updates','N/A')}")

        if package.get('note'):
            print(f"   Note: {package['note']}")

        print("=" *30)

    def display_other_services(self):
        if not self.other_services:
            return
        print("\nOTHER SERVICES")
        print("=" * 30)
        
        for i, service in enumerate(self.other_services, 1):
            print(f"{i}. Service:     {service['service']}")
            print(f"     Description: {service['description']}")
            features = service['features']
            print(f"     Features:    {'\n '.join(features)}")
            print(f"     Notes:       {service['notes']}")
        print("="*30)

    def display_unavailable_services(self):
        if not self.unavailable_services:
            return
        
        print("UNAVAILABLE SERVICES")
        print("=" * 30)

        for service in self.unavailable_services:
            print(f"\n {service['service']}")
            print(f"Reason : {service['description']}")
            print("-" * 30)
        
    def show_help(self):
        print("\n💡 AVAILABLE COMMANDS:")
        print("=" * 40)
        print("• 'packages' - Show all package details")
        print("• 'summary'  - Show package summary")
        print("• 'services' - Show other services")
        print("• 'unavailable' - Show unavailable services")
        print("• 'help'     - Show this help message")
        print("• 'exit'     - Exit the program")
        print("=" * 40)
        print("💬 Or describe your business needs for AI recommendations!")

    def run(self):
        print("AI CUSTOMER PACKAGE ADVISOR")
        print("=" * 30)

        if not self.load_data():
            print("Failed to load data. Check your files.")
            return
        
        print(f"Welcome!")
        self.show_help()

        while True:
            try:
                print("\n" + "=" * 30)
                user_input = input("Describe your needs: ").strip()

                if not user_input:
                    continue

                user_input_lower = user_input.lower()

                if user_input_lower == "exit":
                    print("Bye!")
                    break
                elif user_input_lower == "packages":
                    self.display_packages
                    continue
                elif user_input_lower == "summary":
                    self.display_summary
                    continue
                elif user_input_lower == "services":
                    self.display_other_services
                    continue
                elif user_input_lower == "unavailable":
                    self.display_unavailable_services
                    continue
                elif user_input_lower == "help":
                    self.show_help()
                    continue

                print("Analyzing your request...")
                print("\nAI RECOMMENDATION:")
                print("-" * 30)
                recommendation = self.get_ai_recommendation(user_input)
                print(recommendation)
                print("=" * 30)

            except Exception as e:
                return f"Error in running service: {e}"

def main():
    advisor = PackageAdvisor()
    advisor.run()

if __name__ == "__main__":
    main()