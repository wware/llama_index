# How To Chat With A Github Repository Using Llama-index

https://medium.com/thoughts-on-machine-learning/how-to-chat-with-a-github-repository-using-llama-index-20dea106ae7d

This looks relatively simple.

```shell
pip install llama_index openai
```

```python
import os
from tokens import githubToken, apikey
import openai
from llama_index import VectorStoreIndex
from llama_index import StorageContext, load_index_from_storage
from llama_index.readers import GithubRepositoryReader

openai.api_key = apikey
os.environ["GITHUB_TOKEN"] = githubToken

folder_path = "./storage"
folder_exists = os.path.exists(folder_path) and os.path.isdir(folder_path)

if folder_exists:
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)
else:
    reader = GithubRepositoryReader("jerryjliu", "llama_index", ignore_directories=[".github", ".vscode", "benchmarks", "docs", "examples", "experimental", "scripts", "tests"])
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

    prompt = f"Respond to this question: {question} given the conversation history: {conversation} \n"
    response = query_engine.query(prompt)
    conversation[question] = response
    print(response)
```
