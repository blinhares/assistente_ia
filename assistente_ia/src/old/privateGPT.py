#!/usr/bin/env python3
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler#deprecated
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
import argparse
import time
from src.config import (
    MODEL, 
    EMBEDDINGS_MODEL_NAME, 
    PERSIST_DIRECTORY, 
    TARGET_SOURCE_CHUNKS,
    )



def main():
    # Parse the command line arguments
    args = parse_arguments()
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL_NAME)

    db = Chroma(
        persist_directory=PERSIST_DIRECTORY.as_posix(), 
        embedding_function=embeddings,
        )

    retriever = db.as_retriever(search_kwargs={"k": TARGET_SOURCE_CHUNKS})
    # activate/deactivate the streaming StdOut callback for LLMs
    callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]


    llm = Ollama(model=MODEL, callbacks=callbacks)

    qa = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=retriever, 
        return_source_documents= not args.hide_source,
        )
    
    # Interactive questions and answers
    while True:

        print('#'*50)
        query = input("Digite uma Solicitação -> ")
        if query == "exit":
            break
        if query.strip() == "":
            continue

        # Get the answer from the chain
        start = time.time()
        res = qa.invoke(query)
        answer, docs = res['result'], [] if args.hide_source else res['source_documents']
        end = time.time()
        print()
        #TODO: eu quem comentou isso abaixo
        # Print the result
        # print("\n\n>>>>>> Question:")
        # print(query)
        # print(answer)

        # Print the relevant sources used for the answer
        # for document in docs:
        #     print("\n>>> " + document.metadata["source"] + ":")
        #     print(document.page_content)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='privateGPT: Ask questions to your documents without an internet connection, '
                                                 'using the power of LLMs.')
    parser.add_argument("--hide-source", "-S", action='store_true',
                        help='Use this flag to disable printing of source documents used for answers.')

    parser.add_argument("--mute-stream", "-M",
                        action='store_true',
                        help='Use this flag to disable the streaming StdOut callback for LLMs.')

    return parser.parse_args()


if __name__ == "__main__":
    main()
