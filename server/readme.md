python -m venv venv
./venv/Scripts/activate
python -m ensurepip --upgrade
pip install -r requirements.txt


**Database** 

**Create Migration :** python -m manage --app=manage:app db migrate

**Run Migration :** python manage.py --app=manage:app db upgrade

**Démarrer l'application :** python -m manage --app=manage:app run


**Cron**

**Relance email :** python -m manage --app=manage:app email:register:confirmation


**Commandes**

**Exemple :** 

docker compose exec wiki-server python manage.py --app=manage:app create_db

docker compose exec wiki-server alembic init alembic

docker compose exec wiki-server python manage.py --app=manage:app email:register:confirmation