import ollama
import json
from typing import Optional

class PackageAdvisor:
    def __init__(self):
        self.packages = []
        self.other_services = []
        self.unavailable_services = []
        
    def load_data(self) -> bool:
        """Load all package and service data from JSON files"""
        try:
            # Load frontend packages
            with open('01-frontend-services.json', 'r', encoding='utf-8') as f:
                frontend_data = json.load(f)
                self.packages = frontend_data.get('plans', [])
            
            # Load other services
            with open('02-other-services.json', 'r', encoding='utf-8') as f:
                other_data = json.load(f)
                self.other_services = other_data.get('other_services', [])
            
            # Load unavailable services
            with open('03-unavailable-services.json', 'r', encoding='utf-8') as f:
                unavailable_data = json.load(f)
                self.unavailable_services = unavailable_data.get('unavailable_services', [])
            
            print(f"✓ Loaded {len(self.packages)} packages, {len(self.other_services)} other services")
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Error: Required data file not found - {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON format - {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error loading data: {e}")
            return False
    
    def load_ai_prompt(self) -> Optional[str]:
        """Load and prepare the AI prompt template"""
        try:
            with open('ai_prompt.txt', 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            
            # Replace placeholder with actual packages data
            packages_text = json.dumps(self.packages, indent=2, ensure_ascii=False)
            return prompt_template.replace('{packages_text}', packages_text)
            
        except FileNotFoundError:
            print("❌ Error: ai_prompt.txt file not found")
            return None
        except Exception as e:
            print(f"❌ Error loading AI prompt: {e}")
            return None
    
    def get_ai_recommendation(self, user_question: str) -> str:
        """Get AI recommendation based on user input"""
        system_prompt = self.load_ai_prompt()
        if not system_prompt:
            return "❌ AI service is currently unavailable. Please contact support directly."
        
        try:
            response = ollama.chat(model='llama3.1:8b', messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_question
                }
            ])
            return response['message']['content']
            
        except Exception as e:
            return f"❌ Error getting AI response: {e}"
    
    def display_summary(self):
        """Display package summary"""
        print("\n📦 PACKAGE SUMMARY")
        print("=" * 50)
        for package in self.packages:
            print(f"• {package['name']}: {package['price']}")
        print("=" * 50)
    
    def display_packages(self):
        """Display all packages with details"""
        print("\n🎯 AVAILABLE PACKAGES")
        print("=" * 70)
        
        for i, package in enumerate(self.packages, 1):
            print(f"\n{i}. {package['name']} - {package['price']}")
            print(f"   Type: {package['type']}")
            
            # Extract page information
            pages = [f for f in package['features'] if 'page' in f.lower()]
            if pages:
                print(f"   Pages: {', '.join(pages)}")
            
            # Display key features (first 3)
            key_features = package['features'][:3]
            print(f"   Key Features: {', '.join(key_features)}")
            
            print(f"   Support: {package.get('support', 'N/A')}")
            print(f"   Updates: {package.get('updates', 'N/A')}")
            
            if package.get('note'):
                print(f"   Note: {package['note']}")
            
            print("-" * 70)
    
    def display_other_services(self):
        """Display other available services"""
        if not self.other_services:
            return
            
        print("\n🛠️ OTHER SERVICES")
        print("=" * 60)
        
        for service in self.other_services:
            print(f"\n• {service['service']}")
            print(f"  Description: {service['description']}")
            print(f"  Features: {', '.join(service['features'])}")
            if service.get('notes'):
                print(f"  Notes: {service['notes']}")
            print("-" * 60)
    
    def display_unavailable_services(self):
        """Display services not currently offered"""
        if not self.unavailable_services:
            return
            
        print("\n🚫 SERVICES NOT AVAILABLE")
        print("=" * 60)
        
        for service in self.unavailable_services:
            print(f"\n• {service['service']}")
            print(f"  Reason: {service['description']}")
            print("-" * 60)
    
    def search_packages_by_keywords(self, user_input: str):
        """Search packages based on keywords in user input"""
        keywords = [word.lower() for word in user_input.split() if len(word) > 2]
        if not keywords:
            return
        
        print(f"\n🔍 Packages matching your needs:")
        found_matches = False
        
        for package in self.packages:
            # Search in features
            matched_features = [
                f for f in package['features'] 
                if any(keyword in f.lower() for keyword in keywords)
            ]
            
            # Search in package name and type
            package_text = f"{package['name']} {package['type']}".lower()
            package_match = any(keyword in package_text for keyword in keywords)
            
            if matched_features or package_match:
                found_matches = True
                print(f"\n• {package['name']}")
                if matched_features:
                    print(f"  Matching features: {', '.join(matched_features[:3])}")
        
        if not found_matches:
            print("No direct matches found. Here's our AI recommendation:")
    
    def show_help(self):
        """Display help information"""
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
        """Main program loop"""
        print("🤖 AI CUSTOMER PACKAGE ADVISOR")
        print("=" * 50)
        
        # Load data
        if not self.load_data():
            print("Failed to load required data. Please check your files.")
            return
        
        print(f"\nWelcome! I'll help you find the perfect package for your needs.")
        self.show_help()
        
        while True:
            try:
                print("\n" + "=" * 50)
                user_input = input("\nDescribe your business needs or enter command: ").strip()
                
                if not user_input:
                    continue
                
                user_input_lower = user_input.lower()
                
                # Handle commands
                if user_input_lower == 'exit':
                    print("\n👋 Thank you for using our service! Goodbye!")
                    break
                elif user_input_lower == 'packages':
                    self.display_packages()
                    continue
                elif user_input_lower == 'summary':
                    self.display_summary()
                    continue
                elif user_input_lower == 'services':
                    self.display_other_services()
                    continue
                elif user_input_lower == 'unavailable':
                    self.display_unavailable_services()
                    continue
                elif user_input_lower == 'help':
                    self.show_help()
                    continue
                
                # Process user query
                print(f"\n📝 Analyzing your request: '{user_input}'")
                
                # Show keyword matches
                self.search_packages_by_keywords(user_input)
                
                # Get AI recommendation
                print("\n🤖 AI RECOMMENDATION:")
                print("-" * 40)
                recommendation = self.get_ai_recommendation(user_input)
                print(recommendation)
                print("-" * 40)
                
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                print("Please try again or contact support.")


def main():
    """Main entry point"""
    advisor = PackageAdvisor()
    advisor.run()


if __name__ == "__main__":
    main()