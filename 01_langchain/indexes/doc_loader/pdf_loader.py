# pip install pymupdf faiss-gpu faiss-cpu
# streamlit run ~/pdf_loader.pdf
import os

import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI, AzureOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

def main():
    load_dotenv()

    EMBED_API_MODEL = os.getenv("EMBED_API_MODEL")
    API_TYPE = os.getenv("API_TYPE")
    API_BASE = os.getenv("API_BASE")
    API_KEY = os.getenv("API_KEY")
    GPT_API_MODEL = os.getenv("GPT_API_MODEL")
    GPT_API_VERSION = os.getenv("GPT_API_VERSION")
    embedding = OpenAIEmbeddings(
        deployment=EMBED_API_MODEL,
        openai_api_type=API_TYPE,
        openai_api_base=API_BASE,
        openai_api_key=API_KEY,
        chunk_size=1)

    st.set_page_config(page_title="PDF 问答")
    st.header("PDF 问答 💬")

    pdf = st.file_uploader("上传 PDF", type="pdf")
    if pdf is not None:
        pdf_reader = PdfReader(pdf)

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        index = FAISS.from_texts(chunks, embedding)
        print('索引：', index)

        question = st.text_input("对你的 PDF 进行提问:")
        print('提问：', question)

        if question:
            docs = index.similarity_search(question)

            llm = AzureOpenAI(deployment_name=GPT_API_MODEL, openai_api_version=GPT_API_VERSION, temperature=0)
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=question)
                print(cb)

            st.write(response)


if __name__ == '__main__':
    main()
