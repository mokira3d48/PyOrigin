# Origin Project
![](https://img.shields.io/badge/Python-3.10.12-blue)
![](https://img.shields.io/badge/LICENSE-MIT-%2300557f)
![](https://img.shields.io/badge/lastest-2025--01--20-green)
![](https://img.shields.io/badge/contact-dr.mokira%40gmail.com-blueviolet)


Referencielle clonnable pour initialiser un projet Python dans les bonnes
pratiques.

## Table des matières
- [Description](#description)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Fonctionnalités](#fonctionnalités)
- [Tests](#tests)
- [Contribuer](#contribuer)
- [Licence](#licence)
- [Contact](#contact)


## Description

Mon Projet Python est une application simple qui permet aux utilisateurs de créer, lire, mettre à jour et supprimer des tâches. Il est conçu pour être facile à utiliser et à étendre.

## Installation

Pour installer le projet, assurez-vous d'avoir Python 3.7 ou une version ultérieure et `pip` installés sur votre machine. Ensuite, exécutez les commandes suivantes :

```bash
git clone git@github.com:mokira3d48/PyOrigin.git my_project
cd my_project
sudo rm -r .git
git init
pip install -r requirements.txt
```

1. `sudo apt install cmake python3-venv` Install *Cmake* and *Virtual env*;
2. `make venv` create a virtual env into directory named `env`;
3. `source env/bin/activate` activate the virtual environment named `env`;
4. `make install` install the requirements of this package;
5. `make dev` install the package in dev mode in virtual environment;
6. `make test` run the unit test scripts located at `tests` directory;
7. `make run` run script located at `src/package_name/__main__.py`.
8. Or Run `mycmd` as a command line to run `src/package_name/__main__.py`.

## Utilisation

Voici un exemple de la façon d'ajouter une nouvelle tâche :

```python
from package_name.utils import get_file_paths_list


def main():
    """Main function
    """
    file_paths = get_file_paths_list('./')
    file_paths = sorted(file_paths)
    print("List of file paths:", file_paths)


if __name__ == '__main__':
    main()

```

## Fonctionnalités

- Ajouter des tâches
- Marquer des tâches comme complètes
- Supprimer des tâches
- Afficher toutes les tâches

## Tests

Pour exécuter les tests, assurez-vous d'avoir `pytest` installé,
puis exécutez :

```bash
make test  # ou pytest
```

## Contribuer

Les contributions sont les bienvenues ! Veuillez suivre ces étapes :

1. Forkez le projet;
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/ma-fonctionnalité`);
3. Commitez vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`);
4. Poussez vers la branche (`git push origin feature/ma-fonctionnalité`);
5. Ouvrez une Pull Request.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE)
pour plus de détails.

## Contact

Pour toute question ou suggestion, veuillez contacter :

- **Nom** : Votre nom (Arnold Mokira)
- **Email** : Votre adresse mail (dr.mokira@gmail.com)
- **GitHub** : [Votre Profil GitHub](https://github.com/mokira3d48)


### Explications des sections : (A supprimer du README.md)

- **Titre et description** : Le titre du projet et une brève description de ce qu'il fait.
- **Table des matières** : Une liste de sections pour faciliter la navigation.
- **Installation** : Instructions claires sur la façon d'installer le projet.
- **Utilisation** : Exemples d'utilisation pour aider les utilisateurs à démarrer rapidement.
- **Fonctionnalités** : Une liste des fonctionnalités principales du projet.
- **Tests** : Instructions sur la façon d'exécuter les tests.
- **Contribuer** : Un guide sur la façon de contribuer au projet.
- **Licence** : Informations sur la licence du projet.
- **Contact** : Informations pour contacter le développeur ou l'équipe du projet.


Cet exemple de `README.md` est structuré et informatif, ce qui le rend utile
pour les utilisateurs et les contributeurs potentiels.


