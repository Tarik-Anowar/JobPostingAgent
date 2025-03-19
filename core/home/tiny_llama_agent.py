from langchain_huggingface import HuggingFacePipeline  # Updated import
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch

# Define the local model directory
local_dir = "./tinyllama_model"

# Load tokenizer and model from local storage
print("Loading the tokenizer and model from local directory...")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(local_dir)

# Load model and move it to CUDA (GPU)
model = AutoModelForCausalLM.from_pretrained(
    local_dir, 
    torch_dtype=torch.float16,  # Use float16 for better GPU performance
    device_map="cuda"  # Automatically assigns model to available GPU
)

# Create a text generation pipeline using CUDA
text_generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=256,
    do_sample=True,
    temperature=0.7,
    top_k=50,
)

# Use HuggingFacePipeline in LangChain
llm = HuggingFacePipeline(pipeline=text_generator)

# Test the model
prompt = "Explain the importance of artificial intelligence."
response = llm.invoke(prompt)  # Updated method
print(response)
