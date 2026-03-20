

class RAG:

    def __init__(self):
        self.loader = None # loader of documents
        self.docs = None # documents
        self.splits = None # splitted documents
        self.vector_db = None # vector database
        self.llm = None #  
        self.prompt = None # 
        self.chain = None #
        self.rag_chain = None #


    def load_docs(self, folder, extension):
        raise Exception('Failed to call a function in an abstract class!')


    def get_documents_count(self):
        return 0 if self.docs is None else len(self.docs)


    def split(self, chunk_size, chunk_overlap):
        raise Exception('Failed to call a function in an abstract class!')

    
    def create_vectordb(self, model, output_path, save=True):
        raise Exception('Failed to call a function in an abstract class!')


    def load_llm(self, model):
        raise Exception('Failed to call a function in an abstract class!')


    def load_prompt(self):
        raise Exception('Failed to call a function in an abstract class!')


    def create_rag_chain(self):
        raise Exception('Failed to call a function in an abstract class!')


    def ask(self, question):
        raise Exception('Failed to call a function in an abstract class!')

