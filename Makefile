clean-env:
	rm -rf env

env: requirements.txt
	virtualenv -p python3 env
	env/bin/python -m pip install -r requirements.txt
	env/bin/python -m pip install -e

