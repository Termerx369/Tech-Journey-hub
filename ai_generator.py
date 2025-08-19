import os
from config import MODEL_NAME
from transformers import pipeline, set_seed

class AIGenerator:
    def __init__(self):
        self.generator = pipeline('text-generation', model=MODEL_NAME)
        set_seed(42)  # For reproducible results

    def generate_text(self, prompt, length=100):
        return self.generator(
            prompt,
            max_length=length,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9
        )[0]['generated_text']

def main():
    print("┌─────────────────────────────┐")
    print("│   TERMUX AI TEXT GENERATOR  │")
    print("└─────────────────────────────┘")
    
    ai = AIGenerator()
    
    while True:
        try:
            prompt = input("\nEnter your prompt (or 'quit' to exit): ")
            if prompt.lower() == 'quit':
                break
                
            length = int(input("Output length (50-200 words): "))
            length = max(50, min(200, length))  # Clamp between 50-200
            
            print("\nGenerating... (This may take a moment on mobile)")
            result = ai.generate_text(prompt, length)
            
            print("\n" + "="*40)
            print(result)
            print("="*40)
            
            # Save to examples folder
            os.makedirs("examples/outputs", exist_ok=True)
            with open(f"examples/outputs/{prompt[:10]}.txt", "w") as f:
                f.write(result)
                
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
