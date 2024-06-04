from .ai_ollama_base import AIBase
import ollama # type: ignore
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
import time
from .config import (
    EMBEDDINGS_MODEL_NAME, 
    PERSIST_DIRECTORY, 
    TARGET_SOURCE_CHUNKS,
    )


class PersonalIA(AIBase):
    def __init__(self,  *args, **kwargs): # type: ignore
        super().__init__(*args, **kwargs) # type: ignore
        self.qa_assistant = self._inicializar_modelo()

    def _get_retriver(self):
        '''Retorna um Vetor Retraiver'''
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDINGS_MODEL_NAME)
        
        db = Chroma(
            persist_directory=PERSIST_DIRECTORY.as_posix(), 
            embedding_function=embeddings,
            )
        
        retriever = db.as_retriever(
            search_kwargs={"k": TARGET_SOURCE_CHUNKS})

        return retriever

    def _inicializar_modelo(self):
        # activate/deactivate the streaming StdOut callback for LLMs     
        callbacks = [StreamingStdOutCallbackHandler()]

        llm = Ollama(
            model=self._model_name, 
            callbacks=callbacks)
        
        qa = RetrievalQA.from_chain_type(
            llm=llm, 
            chain_type="stuff", 
            retriever=self._get_retriver(), 
            return_source_documents= True, 
            # return_source_documents= not args.hide_source,
            )
        
        return qa

    def start_chat(self):
        print(f'Starting {self._model_name}...')
            
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
            res = self.qa_assistant.invoke(query) # type: ignore

            print(f'\nEssa resposta levou : {time.time()-start} ms')

if __name__ == "__main__":

    assis = PersonalIA('robo')
    assis.start_chat()
         
    
