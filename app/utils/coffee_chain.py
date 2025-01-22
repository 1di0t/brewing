from langchain.chains import RetrievalQA
from langchain.vectorstores.base import VectorStore
from langchain.llms.base import BaseLLM
from langchain.prompts import PromptTemplate

def create_coffee_retrieval_qa_chain(llm: BaseLLM, vectorstore: VectorStore):
    """
    chain generation for coffee recommendation
    based on the LLM and vectorstore
    """
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    prompt_template = """한국어로 답변해주세요.

        질문: {question}

        관련 정보:
        {context}

        한국어로 답변:"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain_type_kwargs = {"prompt": PROMPT} 
    
    coffee_qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        chain_type_kwargs=chain_type_kwargs,
        retriever=retriever
    )
    return coffee_qa_chain
