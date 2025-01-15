from fastapi import FastAPI
from pydantic import BaseModel

# 1) 로컬 모듈 임포트
from utils.data_preprocessing import load_and_preprocess_coffee_data
from utils.vector_store import create_vector_store_from_coffee_df
from utils.llama_loader import load_llama_llm
from utils.coffee_chain import create_coffee_retrieval_qa_chain

app = FastAPI()

class UserQuery(BaseModel):
    query: str

# 2) 서버 시작 시 실행할 초기화 로직
@app.on_event("startup")
def startup_event():
    global coffee_qa_chain
    
    # (a) 데이터 전처리
    coffee_df = load_and_preprocess_coffee_data("../../pipeline/data/processed/coffee_drop.csv")
    
    # (b) 벡터 스토어 생성
    vectorstore = create_vector_store_from_coffee_df(coffee_df)
    
    # (c) LLM 로드
    llm = load_llama_llm("meta-llama/Llama-2-7b-hf")  # 예시
    
    # (d) 체인 생성
    coffee_qa_chain = create_coffee_retrieval_qa_chain(llm, vectorstore)

# 3) 추천 API
@app.post("/recommend_coffee")
def recommend_coffee(user_query: UserQuery):
    """
    사용자 질문을 받아서, RetrievalQA 체인으로 답변을 생성하여 반환
    """
    question = user_query.query
    answer = coffee_qa_chain.run(question)
    return {"answer": answer}

#uvicorn main:app --reload
