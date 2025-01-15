from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import pandas as pd

def create_vector_store_from_coffee_df(coffee_df: pd.DataFrame):
    """
    1) 데이터셋으로부터 텍스트를 생성 (origin + desc_1 + desc_3 + roast + agtron)
    2) 임베딩 생성 → FAISS 벡터스토어 구축
    """
    # 임베딩 모델 (예: sentence-transformers/all-MiniLM-L6-v2)
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    texts = []
    metadatas = []
    for _, row in coffee_df.iterrows():
        # 검색 대상 텍스트
        text_content = (
            f"Origin: {row['origin']}\n"
            f"Roast: {row['roast']}\n"
            f"Agtron: {row['agtron']}\n"
            f"Description1: {row['desc_1']}\n"
            f"Description3: {row['desc_3']}"
        )
        texts.append(text_content)
        
        # 메타데이터
        metadatas.append({
            "origin": row["origin"],
            "roast": row["roast"],
            "agtron": row["agtron"],
            "desc_1": row["desc_1"],
            "desc_3": row["desc_3"]
        })
    
    # FAISS 벡터 스토어 생성
    vectorstore = FAISS.from_texts(texts, embedding_model, metadatas=metadatas)
    return vectorstore
