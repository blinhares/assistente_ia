kill_all:
	@pgrep ollama | xargs sudo kill 
build:
	@pgrep ollama | xargs sudo kill ; sleep 5 ; ollama rm mistral-poke ;  ollama create mistral-poke -f ./assistente_ia/Modelfile
run:
	@python assistente_ia/privateGPT.py -M
build-igest-run:
	@pgrep ollama | xargs sudo kill ; sleep 5 ; ollama rm mistral-poke ;  ollama create phi3-poke -f ./assistente_ia/Modelfile ; sleep 2 ; python assistente_ia/ingest.py -M ; sleep 2 ;python assistente_ia/privateGPT.py -M

