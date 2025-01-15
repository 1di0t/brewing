from langchain.chains import RetrievalQA
from langchain.vectorstores.base import VectorStore
from langchain.llms.base import BaseLLM

def create_coffee_retrieval_qa_chain(llm: BaseLLM, vectorstore: VectorStore):
    """
    1) 사용자의 질문을 임베딩 후, FAISS 스토어 검색
    2) LLM이 검색된 문서(커피 정보)를 바탕으로 답변 생성
    """
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    coffee_qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )
    return coffee_qa_chain
