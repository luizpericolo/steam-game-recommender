build:
	@git clone https://github.com/smiley/steamapi.git _steam_api
	@pip install -r requirements.txt
	@cd _steam_api/ && python setup.py install
