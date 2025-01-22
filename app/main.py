from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv
from utils.data_processing import load_and_preprocess_coffee_data
from utils.vector_store import create_vector_store_from_coffee_df
from utils.llama_loader import load_llama_llm
from utils.coffee_chain import create_coffee_retrieval_qa_chain
from utils.text import extract_origin_text, translate_with_nllb


import os

load_dotenv()

huggingface_token = os.getenv("HUGGINGFACE_API_KEY")

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

class UserQuery(BaseModel):
    query: str

# initialize global variables when the server starts
@app.on_event("startup")
def startup_event():
    global coffee_qa_chain
    global translator

    # data preprocessing
    coffee_df = load_and_preprocess_coffee_data("../../pipeline/data/processed/coffee_drop.csv")
    
    # vector store generation
    vectorstore = create_vector_store_from_coffee_df(coffee_df)

    # load LLM
    llm = load_llama_llm("meta-llama/Llama-3.2-1B",token=huggingface_token) 
    
    # chain generation
    coffee_qa_chain = create_coffee_retrieval_qa_chain(llm, vectorstore)



# 3) 추천 API
@app.post("/recommend_coffee")
async def recommend_coffee(user_query: UserQuery):
    """
    recieve user query and return the answer
    """
    print(f"user_query: {user_query}")
    question = user_query.query
    answer = coffee_qa_chain.invoke({"query":question})
    print(f"answer\n======================================\n: {answer}")
    
    # Translate the answer to Korean
    #answer['result'] = translate_with_nllb(text=answer['result'], src_lang="eng", tgt_lang="ko")
    
    # Extract only answer in the 'result' field
    answer['result'] = extract_origin_text(answer['result'])
    #answer['result'] = answer['result'].replace('\n\n', ' ')
    return {"answer": answer}

#uvicorn main:app --reload
