python -m venv venv
./venv/Scripts/activate
python -m ensurepip --upgrade
pip install -r requirements.txt

Démarrer l'application : python -m manage --app=manage:app run

Relance email : python -m manage --app=manage:app email:register:comfirmation

Commande directement dans le conteneur:
Exemple : 
docker compose exec wiki-server python manage.py --app=manage:app create_db