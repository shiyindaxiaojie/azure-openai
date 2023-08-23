# !pip install pymilvus
import json
import os

from dotenv import load_dotenv
from langchain.document_loaders import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Milvus


def main():
    load_dotenv()

    EMBED_API_MODEL = os.getenv("EMBED_API_MODEL")
    API_TYPE = os.getenv("API_TYPE")
    API_BASE = os.getenv("API_BASE")
    API_KEY = os.getenv("API_KEY")
    MILVUS_HOST = os.getenv("MILVUS_HOST")
    MILVUS_PORT = os.getenv("MILVUS_PORT")
    embedding = OpenAIEmbeddings(
        deployment=EMBED_API_MODEL,
        openai_api_type=API_TYPE,
        openai_api_base=API_BASE,
        openai_api_key=API_KEY,
        chunk_size=1)

    file_path = "../../data/sample.csv"
    loader = CSVLoader(file_path=file_path, encoding="utf-8")
    docs = loader.load()

    vector_store = Milvus.from_documents(
        docs,
        embedding=embedding,
        connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT}
    )

    query = "呵呵呵我我我"
    docs = vector_store.similarity_search_with_score(query, k=2)
    if docs:
        for doc in docs:
            vector = doc[0]
            score = doc[1]
            if score > 0.3:  # 设置相似度阈值
                return

            data = json.loads(vector.json())
            page_content = data['page_content']
            print(page_content, ", 相似度：", score)


if __name__ == '__main__':
    main()
