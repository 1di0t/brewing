import os
os.environ["HF_HOME"] = "E:\self\huggingface_cache"

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline


def load_llama_llm(model_name_or_path="meta-llama/Llama-2-7b-hf", token=None):
    """
    - Llama2 model load (GPU environment recommended)
    - token: Hugging Face access token 
    """
    
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, token=token,)
    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        device_map="auto",        
        torch_dtype="auto",       
        token=token
        
    )
    generation_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=1024,
        truncation=True,
        temperature=0.7
    )
    llm = HuggingFacePipeline(pipeline=generation_pipeline)
    return llm
