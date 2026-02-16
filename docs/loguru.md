**Documentation complète : Loguru (v0.7.3 – février 2026)**  
Tout ce dont tu as besoin pour intégrer Loguru dans un vrai projet professionnel (FastAPI, Django, script, microservice, etc.).

### 1. Pourquoi Loguru ?
- Un seul logger global (plus de `getLogger(__name__)` partout)
- Configuration ultra-simple (`logger.add()` fait tout : handler + formatter + filter)
- 10× plus rapide que le `logging` standard
- Couleurs dans la console, rotation automatique, JSON natif, backtrace + variables, multiprocessing safe, etc.
- Parfait pour la prod (observability, Loki/Grafana, ELK, etc.)

### 2. Installation
```bash
pip install loguru
# ou avec poetry / uv / etc.
```

### 3. Configuration recommandée pour un vrai projet (à mettre au tout début)

```python
from loguru import logger
import sys
import os
from pathlib import Path

# 1. Supprime le handler par défaut (sinon tu auras des doublons)
logger.remove()

# 2. Handler console (beau + lisible)
logger.add(
    sys.stderr,
    level="INFO",                    # ou os.getenv("LOG_LEVEL", "INFO")
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - {message}",
    colorize=True,
    backtrace=True,
    diagnose=False,                  # ← IMPORTANT en prod (ne pas afficher les variables)
    enqueue=True,                    # safe pour les threads / workers
)

# 3. Handler fichier rotatif + JSON (idéal pour la prod)
log_path = Path("logs") / "app_{time:YYYY-MM-DD}.log"
logger.add(
    str(log_path),
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {name}:{function}:{line} | {message}",
    rotation="500 MB",               # ou "00:00" (minuit), "1 week", etc.
    retention="30 days",             # supprime les vieux fichiers
    compression="zip",               # ou "gz"
    serialize=True,                  # ← JSON structuré (parfait pour Loki/ELK)
    enqueue=True,
    encoding="utf8",
)
```

### 4. Les méthodes principales

| Méthode                  | Usage typique                                      | Exemple |
|--------------------------|----------------------------------------------------|---------|
| `logger.debug/info/...`  | Log normal                                         | `logger.info("Utilisateur {user} connecté", user="john")` |
| `logger.opt(...).info()` | Options temporaires (lazy, colors, exception…)    | voir ci-dessous |
| `logger.bind()`          | Contexte persistant (user_id, request_id…)        | `logger = logger.bind(user_id=123)` |
| `logger.contextualize()` | Contexte local au thread/task (contextvars)        | `with logger.contextualize(request_id=req_id):` |
| `logger.patch()`         | Modifier le record à la volée                      | ajout de timestamp UTC, etc. |
| `logger.catch()`         | Décorateur / context manager pour catcher les exceptions | `@logger.catch` |
| `logger.exception()`     | Log une exception + traceback (uniquement dans un `except`) | voir section 7 |
| `logger.remove(id)`      | Supprime un handler                                | `logger.remove(0)` (default) |
| `logger.configure()`     | Configuration complète en une fois                 | idéal pour les apps |

### 5. Structured logging (JSON) – le plus important en prod

```python
# Option 1 : serialize=True dans logger.add() → tout est déjà JSON

# Option 2 : custom serializer (si tu veux un format précis)
def json_serializer(record):
    return {
        "timestamp": record["time"].timestamp(),
        "level": record["level"].name,
        "message": record["message"],
        "module": record["name"],
        "function": record["function"],
        "line": record["line"],
        "extra": record["extra"],        # tout ce que tu as bindé
        "exception": record["exception"]
    }

logger.add("app.jsonl", serialize=json_serializer, enqueue=True)
```

### 6. Fonctionnalités avancées très utiles

**Lazy evaluation** (évite de calculer des choses chères si le niveau n’est pas actif)
```python
logger.opt(lazy=True).debug("Données lourdes : {}", lambda: expensive_query())
```

**Backtrace + variables** (super puissant en dev)
```python
logger.add(..., backtrace=True, diagnose=True)   # seulement en dev !
```

**Niveaux personnalisés**
```python
logger.level("API_CALL", no=15, color="<blue>", icon="📡")
logger.log("API_CALL", "Appel vers Stripe")
```

**Multiprocessing / Workers (FastAPI uvicorn, Celery, etc.)**
```python
logger.add("file.log", enqueue=True)   # obligatoire
# Dans les workers : logger.complete() avant de quitter
```

### 7. Gestion des exceptions (et le fameux `NoneType: None`)

**Correct :**
```python
try:
    1 / 0
except Exception:
    logger.exception("Division par zéro !")   # ← traceback complet + beau
```

**Incorrect (ce qui provoque `NoneType: None`) :**
```python
logger.exception("Oups !")   # ← pas dans un except → sys.exc_info() = (None, None, None)
```

**Solution :** utilise `logger.error()` ou `logger.opt(exception=True)` si tu as déjà l’exception.

**Décorateur magique :**
```python
@logger.catch(reraise=True)   # ou reraise=False pour ne pas crasher
def risky_function():
    ...
```

### 8. Meilleures pratiques production 2026

1. Configure le logger **une seule fois** au démarrage de l’application (dans `main.py` ou `app/__init__.py`).
2. `diagnose=False` en production (sécurité).
3. `enqueue=True` dès que tu as plusieurs threads/workers.
4. `logger.remove()` avant d’ajouter tes handlers.
5. Pour les **libraries** : `logger.disable("ma_lib")` et laisse l’application décider.
6. Utilise `logger.bind(request_id=...)` partout (très utile avec middleware FastAPI).
7. Logs en JSON + rotation + retention → compatible Loki, ELK, Datadog, etc.

### 9. Exemple complet FastAPI (très courant en 2026)

```python
# main.py
from fastapi import FastAPI, Request
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="INFO", format=..., enqueue=True)
logger.add("logs/api_{time}.jsonl", serialize=True, rotation="100 MB", enqueue=True)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    with logger.contextualize(
        request_id=request.headers.get("X-Request-ID"),
        path=request.url.path,
        method=request.method,
    ):
        logger.info("Requête entrante")
        response = await call_next(request)
        logger.info("Réponse {status}", status=response.status_code)
        return response

@app.get("/")
async def home():
    logger.info("Endpoint home appelé")
    return {"hello": "world"}
```

### 10. Migration depuis `logging` standard (rapide)

- `logging.getLogger(__name__)` → `from loguru import logger`
- `handler + formatter` → `logger.add(sink, format=..., level=...)`
- `extra={}` → `logger.bind(**extra)`
- `exc_info=True` → `logger.opt(exception=True)`
- `basicConfig` → `logger.configure(handlers=[...])`

### 11. FAQ & Dépannage courant

- **Logs en double** → `logger.remove()` avant `add()`
- **Pas de logs** → niveau trop haut ou pas de sink
- **Fichiers dupliqués en multiprocessing** → configure dans `if __name__ == "__main__":` ou utilise `enqueue=True`
- **NoneType: None** → `logger.exception()` hors d’un `except`
- **Curly braces dans les messages** → n’utilise pas d’f-string avec `{}` dans le message, passe les variables en arguments

Tu veux que je te génère :
- Un fichier `logger_config.py` prêt à l’emploi ?
- Une version avec structlog + loguru (le combo ultime 2026) ?
- Un middleware FastAPI/Django complet avec request_id ?

---

Voici des exemples concrets et commentés pour **chacune des méthodes principales** de **loguru** (basé sur la version ~0.7.x en 2026). Tous les exemples supposent que tu as fait :

```python
from loguru import logger
```

et que tu as déjà configuré/supprimé les handlers par défaut si besoin (`logger.remove()`).

### 1. Les méthodes de logging de base

```python
# debug → niveau le plus bas, pour le développement
logger.debug("Détail technique : variable x = {x}", x=42)

# info → informations normales de fonctionnement
logger.info("L'application a démarré correctement")

# success → niveau custom sympa de loguru (plus visible que info)
logger.success("Tâche terminée avec succès ! 🎉")

# warning → quelque chose d'inhabituel mais pas fatal
logger.warning("La connexion à la DB est lente (> 500ms)")

# error → erreur gérée, l'app continue
logger.error("Impossible de charger la config : fichier manquant")

# critical → erreur grave, l'app va probablement crasher
logger.critical("La base de données principale est DOWN !")

# trace → niveau encore plus bas que debug (activé avec level="TRACE")
logger.trace("Entrée dans la boucle while - itération #{i}", i=17)
```

### 2. logger.opt() → options temporaires (lazy, colors, exception, depth…)

```python
# Lazy evaluation : la fonction n'est appelée que si le niveau est actif
logger.opt(lazy=True).debug(
    "Utilisateur lourd : {user_data}",
    user_data=lambda: fetch_user_from_db(very_expensive=True)
)

# Couleurs manuelles dans le message
logger.opt(colors=True).info("<bold><red>ALERTE</red></bold> : action urgente requise")

# Ajouter une exception manuellement (équivalent à .exception mais plus flexible)
try:
    1 / 0
except ZeroDivisionError as e:
    logger.opt(exception=True).error("Division interdite !")

# Changer la profondeur de la trace (utile dans les wrappers)
def my_wrapper(func):
    def wrapped(*args, **kwargs):
        return logger.opt(depth=1).info("Appel de {func}", func=func.__name__)
    return wrapped
```

### 3. logger.bind() → ajouter du contexte persistant

```python
# Contexte pour tout un utilisateur / requête
user_logger = logger.bind(user_id=1234, username="aria", ip="196.168.1.45")

user_logger.info("Connexion réussie")
user_logger.warning("Tentative d'accès à une ressource interdite")

# Chaînage possible
admin_logger = user_logger.bind(role="admin", privileges=["delete", "ban"])
admin_logger.critical("Suppression massive demandée")
```

### 4. logger.contextualize() → contexte temporaire (avec with)

```python
# Idéal pour les middlewares (FastAPI, etc.)
with logger.contextualize(request_id="req-abc123", path="/api/v1/users"):
    logger.info("Début traitement requête")
    # ... tout le code de la requête ...
    logger.info("Fin traitement", status=200)
```

### 5. logger.catch() → décorateur / context manager anti-crash

```python
# Décorateur (reraise=True par défaut → relance l'exception après log)
@logger.catch(message="Erreur dans process_data() !", onerror=lambda _: exit(1))
def process_data(file_path):
    with open(file_path) as f:
        data = json.load(f)  # peut planter
    return data

# Version context manager
with logger.catch(reraise=False):  # attrape mais ne relance pas
    risky_operation()
    logger.info("Cette ligne ne sera jamais atteinte si exception")
```

### 6. logger.exception() → logger une exception + traceback

**Important** : uniquement dans un bloc `except` (sinon → NoneType: None)

```python
try:
    response = requests.get("https://api.example.com/data", timeout=0.1)
    response.raise_for_status()
except requests.RequestException:
    logger.exception("Échec appel API")          # ← traceback complet + beau
    # Ou avec message custom :
    logger.exception("Échec appel API après {attempt} tentatives", attempt=3)
```

### 7. logger.patch() → modifier le record à la volée (très puissant)

```python
# Ajouter automatiquement l'heure UTC + hostname
import socket
from datetime import datetime, timezone

def patcher(record):
    record["extra"]["utc_time"] = datetime.now(timezone.utc).isoformat()
    record["extra"]["host"] = socket.gethostname()

logger = logger.patch(patcher)

logger.info("Message avec utc_time et host automatiquement ajoutés")
```

### 8. Autres méthodes utiles (niveaux custom, remove, etc.)

```python
# Créer un niveau custom
logger.level("METRICS", no=25, color="<magenta>", icon="📊")

logger.log("METRICS", "Temps traitement = {elapsed_ms} ms", elapsed_ms=47.2)

# Supprimer un handler précis (retourne l'id quand tu add())
handler_id = logger.add("file.log")
# ... plus tard ...
logger.remove(handler_id)
```

### Petit récap visuel rapide

| Méthode          | Quand l'utiliser ?                              | Exemple court                          |
|------------------|--------------------------------------------------|----------------------------------------|
| `debug/info/...` | Logging normal                                   | `logger.info("Hello")`                 |
| `opt()`          | Options one-shot (lazy, colors, exception…)      | `logger.opt(colors=True).success(...)` |
| `bind()`         | Contexte persistant (user, request…)             | `logger.bind(user=123).info(...)`      |
| `contextualize()`| Contexte temporaire (with)                       | `with logger.contextualize(...):`      |
| `catch()`        | Attraper automatiquement les exceptions          | `@logger.catch`                        |
| `exception()`    | Logger traceback dans un `except`                | `except: logger.exception(...)`        |
| `patch()`        | Enrichir tous les records (timestamp UTC…)       | `logger = logger.patch(patcher)`       |
