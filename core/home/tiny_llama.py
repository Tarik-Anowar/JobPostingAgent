from transformers import AutoModelForCausalLM, AutoTokenizer

# Define model name and target directory
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
local_dir = "./tinyllama_model"  # Change this to your preferred directory

# Download and save the tokenizer and model
print("Downloading and saving the tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(local_dir)

print("Downloading and saving the model...")
model = AutoModelForCausalLM.from_pretrained(model_name)
model.save_pretrained(local_dir)

print(f"Model saved in {local_dir}")
