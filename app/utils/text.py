import re

def extract_origin_text(data: str) -> str:
    """
    Extract the portion of the text starting from '\n\nOrigin:' and ending at the last '\n\n'.
    
    Args:
        data (dict): A dictionary containing the 'result' key with the text to process.

    Returns:
        str: The extracted portion of the text, or an empty string if not found.
    """
    result_text = data

    # Regular expression to capture the block starting from '\n\nOrigin:' and ending before the last '\n\n'
    match = re.search(r"(\n\nOrigin:.*?\n\n)", result_text, re.DOTALL)

    if match:
        return match.group(1).strip()
    return ""

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def translate_with_nllb(text: str, src_lang: str, tgt_lang: str) -> str:
    model_name = "facebook/nllb-200-distilled-600M"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # generate input 
    input_text = f">>{tgt_lang}<< {text}"
    print(input_text)
    inputs = tokenizer(input_text, return_tensors="pt",padding=True)

    # translate
    translated = model.generate(**inputs)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text


