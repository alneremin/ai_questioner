
import pysqlite3
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

from questioner.rag.rag import RAG

class OllamaRAG(RAG):

    def __init__(self):
        super().__init__()


    def load_docs(self, folder, extension):
        self.loader = DirectoryLoader(folder, glob=f"*.{extension}")
        self.docs = self.loader.load()


    def split(self, chunk_size, chunk_overlap):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.splits = text_splitter.split_documents(self.docs)

    
    def create_vector_db(self, model, output_path, save=True):
        ollama_embeddings = OllamaEmbeddings(model=model)
        self.vector_db = Chroma.from_documents(
            documents=self.splits, 
            embedding=ollama_embeddings, 
            persist_directory=output_path
        )
        if save:
            self.vector_db.persist()


    def load_llm(self, model):
        self.llm = Ollama(model=model)


    def load_prompt(self, prompt):
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", (prompt)),
                ("human", "{input}"),
            ]
        )


    def create_rag_chain(self):
        self.chain = create_stuff_documents_chain(self.llm, self.prompt)
        retriever = self.vector_db.as_retriever()
        self.rag_chain = create_retrieval_chain(retriever, self.chain)


    def ask(self, question):
        return self.rag_chain.invoke({"input": question})['answer']
