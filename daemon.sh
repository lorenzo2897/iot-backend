sudo -u lorenzo screen -S flask -d -m bash -c "export FLASK_APP=backend.py; python -m flask run --host=0.0.0.0 --port=50500"
