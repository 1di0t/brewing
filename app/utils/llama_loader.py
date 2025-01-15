from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.llms import HuggingFacePipeline

def load_llama_llm(model_name_or_path="meta-llama/Llama-2-7b-hf", use_auth_token=None):
    """
    - LLaMA2 모델 로드 (GPU 환경 권장)
    - use_auth_token: Hugging Face access token (gated repo 접근 시 필요)
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_auth_token=use_auth_token)
    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        device_map="auto",        # GPU 여러 개나 CPU 환경 등에 맞게 설정
        torch_dtype="auto",       # 가능하다면 bfloat16, float16 등 설정
        use_auth_token=use_auth_token
    )
    generation_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=512,
        temperature=0.7
    )
    llm = HuggingFacePipeline(pipeline=generation_pipeline)
    return llm
