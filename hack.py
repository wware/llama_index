import json
import os
import openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader,\
    StorageContext, load_index_from_storage
    
# from llama_index import VectorStoreIndex

# from llama_index import StorageContext, load_index_from_storage

# from llama_index.readers.github.repository.base import GithubRepositoryReader

# Requires: pip install llama-index-readers-github
from llama_index.readers.github import GithubRepositoryReader, GithubClient

creds = json.load(open("credentials.json"))
apikey = creds["openai-key"]
githubToken = creds["github-token"]

openai.api_key = apikey
os.environ["GITHUB_TOKEN"] = githubToken

folder_path = "./storage"
folder_exists = os.path.exists(folder_path) and os.path.isdir(folder_path)

if folder_exists:
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)
else:
    reader = GithubRepositoryReader(
        "wware",
        "python-hacks"
        # ignore_directories=[
        #     ".github",
        #     ".vscode",
        #     "benchmarks",
        #     "docs",
        #     "examples",
        #     "experimental",
        #     "scripts",
        #     "tests"
        # ]
    )
    branch_documents = reader.load_data(branch="main")
    index = VectorStoreIndex.from_documents(branch_documents)
    index.storage_context.persist()

query_engine = index.as_query_engine()

while True:
    conversation = {}
    question = input("\n Write your question or enter 'quit' to quit. \n\n")
    conversation[question] = ""

    if question == 'quit':
        break

    prompt = f"Respond to this question: <<<{question}>>> given the conversation history: <<<{conversation}>>> \n"
    response = query_engine.query(prompt)
    conversation[question] = response
    print(response)
