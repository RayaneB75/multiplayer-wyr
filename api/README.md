# API utilisée pour l'application WYR


## Initialisation pour développement :

### Création de la base de données

```bash
docker run --name some-mysql \
    -p 3306:3306 \
    -e MYSQL_ROOT_PASSWORD=[] \
    -e MYSQL_DATABASE=[] \
    -e MYSQL_USER=[] \
    -e MYSQL_PASSWORD=[] \
    -d mysql:latest
```

### Lancement de l'application

Création virtual env :
```bash
python3 -m venv ./venv
source venv/bin/activate
```

Récupération des variables d'environnement (voir .env.sample) :

```bash
export DB_DATABASE=[]
export MYSQL_USER=[]
export MYSQL_PASSWORD=[]
export MYSQL_HOST=[@ip du container]
export MYSQL_PORT=[]
export FRONT_TOKEN=thisIsSecret
export DASH_TOKEN=thisIsSecret
```

Lancement de l'application :

```bash
cd src/
pip install -r requirements.txt
python3 wsgi.py
```

NB : On peut aussi lancer l'application avec des paramètres prédéfinis :
- `python3 wsgi.py --init`
- `python3 wsgi.py --create-db` (création des tables)
- `python3 wsgi.py --clear-db` (vidage des tables)
- `python3 wsgi.py --reset-db` (suppression et recréation des tables)
