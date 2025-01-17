import re

def extract_helpful_answer(response_text: str) -> str:
    pattern = r"Helpful Answer:\s*(.*)"
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        answer_only = match.group(1).strip()
    else:
        answer_only = "답변을 찾을 수 없습니다."
    return answer_only

