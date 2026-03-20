
import sys
import yaml
from questioner.google import GoogleSheetAPI
from questioner.rag import OllamaRAG
import warnings
from langchain_core._api.deprecation import LangChainDeprecationWarning

# Suppress LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

def main(argv):

    print(f"Arguments: {argv}")

    config = None
    with open(argv[1], 'r') as file:
        config = yaml.safe_load(file)

    google_conf = config['google_sheet_service']
    gsheet_api = GoogleSheetAPI(google_conf['path_to_creds'], google_conf['scopes'])
    gsheet_api.init_spreadsheets(google_conf['service_name'], google_conf['service_version'])
    gsheet_api \
    .set_current_spreadsheet(google_conf['spreadsheet_id']) \
    .set_current_sheet(google_conf['sheet'])

    rag_conf = config['llm']
    rag = OllamaRAG()
    rag.load_docs(rag_conf['path_to_docs'], rag_conf['docs_extension'])
    print(f"Documents (N={rag.get_documents_count()}) are loaded.")
    rag.split(rag_conf['shunk_size'], rag_conf['shunk_overlap'])
    print(f"Documents are splitted into chunks with size equal to {rag_conf['shunk_size']}")

    rag.create_vector_db(rag_conf['embeddings_model'], rag_conf['path_to_vector_db'])
    print(f"Vector DB is created in folder '{rag_conf['path_to_vector_db']}'!")

    rag.load_llm(rag_conf['llm'])
    print("Model is loaded!")
    prompt = ""
    with open(rag_conf['system_prompt_path'], 'r') as file:
        prompt = file.read()
    rag.load_prompt(prompt)
    rag.create_rag_chain()
    print("RAG chain is created, ready to answer!")

    current_row_index = 1
    while True:
        question = input("Ask a question [and press Enter]:")
        print(f"Your question: {question}")
        if question.strip() == "":
            continue
        print("I am thinking...")
        answer = rag.ask(question)
        print(f"My answer: {answer}")
        gsheet_api.write_to_cell(f'A{current_row_index}:B{current_row_index}', [str(question), str(answer)])

        current_row_index += 1


if __name__ == '__main__':
    main(argv=sys.argv)
