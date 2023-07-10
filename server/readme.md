python -m venv venv
./venv/Scripts/activate
python -m ensurepip --upgrade
pip install -r requirements.txt
python -m manage --app=manage:app run

docker compose exec wiki-server python manage.py --app=manage:app create_db