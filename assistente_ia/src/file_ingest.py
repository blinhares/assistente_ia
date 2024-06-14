#!/usr/bin/env python3
import os
import glob
from typing import Any, List
from multiprocessing import Pool
from tqdm import tqdm

from langchain_community.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)

from langchain_community.document_loaders import UnstructuredExcelLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

from pathlib import Path
# Load environment variables
from assistente_ia.src.config import (
    EMBEDDINGS_MODEL_NAME, 
    PERSIST_DIRECTORY, 
    SOURCE_DIRECTORY, 
    # CHROMA_SETTINGS
    )

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Custom document loaders
class MyElmLoader(UnstructuredEmailLoader):
    """Wrapper to fallback to text/plain when default does not work"""
    def load(self) -> List[Document]:
        """Wrapper adding fallback for elm without html"""
        try:
            try:
                doc = UnstructuredEmailLoader.load(self)
            except ValueError as e:
                if 'text/html content not found in email' in str(e):
                    # Try plain text
                    self.unstructured_kwargs["content_source"]="text/plain"
                    doc = UnstructuredEmailLoader.load(self)
                else:
                    raise
        except Exception as e:
            # Add file_path to exception message
            raise type(e)(f"{self.file_path}: {e}") from e

        return doc

# Map file extensions to document loaders and their arguments
LOADER_MAPPING = { # type: ignore
    ".csv": (CSVLoader, {}),
    # ".docx": (Docx2txtLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".eml": (MyElmLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PyMuPDFLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
    ".log": (TextLoader, {"encoding": "utf8"}),
    # Add more mappings for other file extensions and loaders as needed
    ".xlsx":(UnstructuredExcelLoader,{})
}

class IngestData:
    def __init__(self) -> None:
        pass

    def _if_directory_not_exist_then_create(self, directory:str)->bool:
        if Path(directory).is_dir():
            return True
        print(f'O diretório {directory} sera criado!')
        os.mkdir(directory)
        return False

    def _load_single_document(self, file_path: str) -> List[Document]:
        ext = "." + file_path.rsplit(".", 1)[-1]
        try:
            if ext in LOADER_MAPPING:
                loader_class, loader_args = LOADER_MAPPING[ext]
                loader = loader_class(file_path, **loader_args) # type: ignore
                return loader.load()
        except ValueError :
            print(f"Problema ao ler : '{file_path}'")
            return [Document('')]
        return [Document('')]
        
    def _load_documents(
            self,
            source_dir_or_file: str, 
            ignored_files: List[str] = []
            ) -> List[Document]:
        """
        Loads all documents from the source documents directory, ignoring specified files
        """
        all_files:list[Any] = []
        #verificar se source_dir é diretório
        if Path(source_dir_or_file).is_dir():
            for ext in LOADER_MAPPING:
                all_files.extend(
                    glob.glob(
                        os.path.join(source_dir_or_file, f"**/*{ext}"), 
                        recursive=True)
                )
        else:
            if (f".{source_dir_or_file.split('.')[-1]}" 
                in list(LOADER_MAPPING.keys())): # type: ignore
                all_files.extend([source_dir_or_file])

        filtered_files = [file_path for file_path in all_files if file_path not in ignored_files]

        with Pool(processes=os.cpu_count()) as pool:
            results:list[Any] = []
            with tqdm(
                total=len(filtered_files), 
                desc='Loading new documents', 
                ncols=80) as pbar:
                for _ , docs in enumerate(
                    pool.imap_unordered(
                        self._load_single_document, 
                        filtered_files)
                        ):
                    results.extend(docs)
                    pbar.update()

        return results

    def _process_documents(
            self,
            ignored_files: List[str] = []) -> List[Document]:
        """
        Load documents and split in chunks
        """
        print(f"Carregando Documentos de : {SOURCE_DIRECTORY}")
        documents = self._load_documents(SOURCE_DIRECTORY, ignored_files)
        if not documents:
            print("No new documents to load")
            exit(0)
        print(f"Loaded {len(documents)} new documents from {SOURCE_DIRECTORY}")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, 
            chunk_overlap=CHUNK_OVERLAP)
        texts = text_splitter.split_documents(documents)
        print(f"Split into {len(texts)} chunks of text (max. {CHUNK_SIZE} tokens each)")
        
        return texts

    def _get_db(self):
        # Create embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDINGS_MODEL_NAME)
        
        return Chroma(
            persist_directory=PERSIST_DIRECTORY.as_posix(),
            embedding_function=embeddings,
            # client_settings=CHROMA_SETTINGS,
            )
    
    def start_ingestion(self):
        if self._if_directory_not_exist_then_create(SOURCE_DIRECTORY):
            # Update and store locally vectorstore
            print(f"Adicionando ao Banco de Vetores em: {PERSIST_DIRECTORY}")
            db = self._get_db()
            
            collection = db.get()

            ignored_files = [metadata['source'] for metadata in collection['metadatas']]

            texts = self._process_documents(
                ignored_files
                )
            
            print("Criando embeddings. Talvez leve alguns minutos...")
            embeddings_limit =30_000
            texts = texts[:embeddings_limit]

            with tqdm(
                total=len(texts), 
                desc='Embedding Documentos..', 
                ncols=80) as progress_bar:
                    for text in texts:
                        db.add_documents([text])
                        progress_bar.update()
        
    
    def _remove_db_data(self):
        db = self._get_db()
        db.delete(
            db.get()['ids']
        )

if __name__ == "__main__":
    # main()
    a = IngestData()
    a.start_ingestion()
    # a._remove_db_data()
    
    
