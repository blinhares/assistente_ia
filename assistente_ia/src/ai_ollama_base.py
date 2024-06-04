import ollama # type: ignore
from .config import logger_maker

logger = logger_maker(__name__)

class AIBase:
    """Cria um assistente de IA usando Ollama MOdels"""
    def __init__(self, 
                 assistant_name:str = '',
                 model_system:str='', 
                 ollama_model:str = 'phi3'
                 ):
        """Inicializa o Modelo, baseado no model indicado.

        Args:
            assistant_name (str, optional): Nome do seu assistente. Ex.: 'Marcos', 'Carla'.
            O padrao é em branco.
            model_system (str, optional): Define o system do seu modelo. A identidade de sua IA.
            Ex.:'VOce é o Marinheiro Popai. E fala gaguejando.'
            Esse dado pode ser tao extenso quanto deseja e pode adicionar caracteristicas ao modelo.
            . Defaults to ''.
            ollama_model (str, optional): O model do Ollama que nossa ia Se baseara. 
            No nosso caso sera 'phi3'. FIque a vontade para usar qualquer uma dessas: https://ollama.com/library
        """
        self._assistant_name:str = assistant_name
        self._model_ollama:str = ollama_model
        self._model_name:str = ''
        self._model_system_description:str = model_system
        self._start()
        
    def _start(self):
        #nomeando o modelo
        self.give_model_a_name(
            self._model_ollama, 
            self._assistant_name )
        #caso nao exista criar um
        if not self._model_exists():
            self._model_create()

    def give_model_a_name(self,ollama_model:str, assistant_name:str ):
        """
    Este método gera um nome para o modelo Ollama com base no nome do assistente e no modelo Ollama selecionado.
    Se nenhum nome de assistente for fornecido, ele padrão para um nome de modelo personalizado usando o nome do modelo Ollama.

    Parâmetros:
    - self (PersonalAI): A instância da classe PersonalAI.

    Retorna:
    - None: Este método não retorna nenhum valor. Ele atualiza o atributo '_model_name' da instância.
    """
        if not assistant_name:
            self._model_name:str = f'{ollama_model}_personal'.lower()
        else:
            self._model_name:str = f'{ollama_model}_{assistant_name}'.lower()

    @property
    def model_name(self):
        return self._model_name
    
    def _model_exists(self)-> bool:
        logger.info(f'Verificando se {self._model_name} existe')
        try:
            ollama.show(self._model_name)
            logger.info(f'{self._model_name} Existe')
            return True
        except:
            logger.info(f'{self._model_name} Não Existe')
            return False
        
    def _model_make_modelfile(self)->str:
        """Criar arquivo Model File para Criacao do Modelo
        """
        logger.info(f'Criando Model File para {self._model_name} ... ')
        modelfile = f'''
FROM {self._model_ollama}
'''
        if self._model_system_description == '':
            return modelfile
        modelfile += f'''SYSTEM """{self._model_system_description}"""'''
        return modelfile
        
        
    def _model_create(self):
        logger.info(f'Criando modelo {self._model_name}...')
        ollama.create( # type: ignore
            model=self._model_name,
            modelfile=self._model_make_modelfile()
        )
        logger.info(f'Modelo {self._model_name} criado!')

    def _model_autoremove(self):
        """Auto remove o Modelo"""
        logger.warning(f'Removendo modelo {self._model_name}...')
        ollama.delete( # type: ignore
            model=self._model_name,
        )
        logger.warning(f'Modelo {self._model_name} removido!')

    def model_rebuild(self):
        """Reconstroi o Modelo para aplicar possiveis alterações."""
        logger.info(f'Reconstruindo o Modelo {self._model_name}...')
        self._model_autoremove()
        self._model_create()


    

if __name__ == "__main__":

    def perguntar_algo(model_name:str, pergunta:str):
        stream = ollama.chat(
        model=model_name,
        messages=[
            {'role': 'user', 'content': pergunta}],
        stream=True,
        )

        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True) # type: ignore

    system = '''Voce é uma IA'''
    assis = AIBase('robo',system)
    # assis.model_rebuild()

    while True:
        print('-'*80)
        perguntar_algo(assis.model_name, input('Pergunta -> '))


    

    
  