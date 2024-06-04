from src.ai_personal import PersonalIA
from src.file_ingest import IngestData
#TODO : Implementar Chat History, E outras coisinhas mais

if __name__ == '__main__':
    while True:
        print('''
Escolha uma opção:

1 - Processar Dados;
2 - Iniciar Chat;''')
        escolha = input('->')
        if  escolha == '1':
            data_ingestion = IngestData()
            data_ingestion.start_ingestion()
        if escolha == '2':
            assis = PersonalIA('minha_ia','Um assistente digital que fala portugues do brasil')
            assis.start_chat()
    
    