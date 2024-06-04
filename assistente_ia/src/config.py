from chromadb.config import Settings
import logging
from pathlib import Path

### LOG ###

ROOT_DIR = Path(__file__).parent
LOG_FILE_DIR = ROOT_DIR / 'logteste.log'

# formato da msg de log deve ser add como atributo format em basicConfig
LOG_FORMAT = '[%(asctime)s] - %(levelname)s:%(name)s:%(message)s' 

# Mudando a configuração em caso de produção ou projeto
PRODUCAO = True # se false imprime os logs na tela.
if PRODUCAO:
    basic_config = {
        # 'filename':LOG_FILE_DIR,
        'level' : logging.INFO,#nao mostra arquivos de debug
        'format' : LOG_FORMAT
        }
else:
    basic_config = {
        'level' : logging.DEBUG,
        'format' : LOG_FORMAT
        }
#set log config
logging.basicConfig(**basic_config) # type: ignore

def logger_maker(name:str):
    '''Criar logger'''
    return logging.getLogger(name)
    

## DIRETORIO DE ARQUIVOS ##
SOURCE_DIRECTORY = 'source_documents'
# SOURCE_DIRECTORY = '/home/bruno/Downloads/'
# SOURCE_DIRECTORY = '/home/bruno/Documentos/Python/assistente_ia/source_documents/SJ MARACANAU solicitação de investimento.xlsx'

## DIRETORIO DE ARQUIVOS PERSISTENTES ##
PERSIST_DIRECTORY = Path(__file__).parent / 'db'

# Define the Chroma settings
CHROMA_SETTINGS = Settings(
        persist_directory=PERSIST_DIRECTORY.as_posix(),
        anonymized_telemetry=False
)

# For embeddings model, the example uses a sentence-transformers model
# https://www.sbert.net/docs/pretrained_models.html 
# "The all-mpnet-base-v2 model provides the best quality, while all-MiniLM-L6-v2 is 5 times faster and still offers good quality."
# EMBEDDINGS_MODEL_NAME = os.environ.get("EMBEDDINGS_MODEL_NAME", "all-MiniLM-L6-v2")
# EMBEDDINGS_MODEL_NAME = "all-mpnet-base-v2"
EMBEDDINGS_MODEL_NAME = "all-MiniLM-L6-v2"

###DEFININDO MODEL DO OLLAMA ###
## CERTIFICAR DE QUE FOI BAIXADO 
MODEL = "phi3"
# MODEL = os.environ.get("MODEL", "mistral-poke")
# MODEL = os.environ.get("MODEL", "mistral")#original

TARGET_SOURCE_CHUNKS = int(4)
