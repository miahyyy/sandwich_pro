# Projet dbt Jaffle Shop

Un projet dbt (data build tool) de démonstration présentant les meilleures pratiques pour les workflows modernes de transformation de données utilisant un ensemble de données d'exemple e-commerce appelé "Jaffle Shop".

## 📋 Vue d'ensemble

Ce projet est une implémentation dbt complète d'un pipeline d'analytique pour un commerce électronique. Il transforme les données transactionnelles brutes en ensembles de données analytiques propres et bien organisés, prêts pour les outils de business intelligence.

**Version:** 3.0.0  
**Version dbt:** >= 1.5.0  
**Base de données:** PostgreSQL (configurable)

## 🏗️ Architecture

Le projet suit un modèle d'architecture à trois couches :

```
Données brutes (Seeds) → Modèles de staging → Modèles de marts → Analytique
```

### Couche 1 : Données brutes (Staging)
- **Localisation:** `seeds/jaffle-data/`
- **Contient:** 6 fichiers CSV de seed avec des données e-commerce brutes
  - `raw_customers.csv` - Information des clients
  - `raw_orders.csv` - Transactions de commandes
  - `raw_items.csv` - Articles par commande
  - `raw_products.csv` - Catalogue de produits
  - `raw_stores.csv` - Emplacements des magasins
  - `raw_supplies.csv` - Données de la chaîne d'approvisionnement

### Couche 2 : Modèles de staging
- **Localisation:** `models/staging/`
- **Objectif:** Nettoyage et standardisation des données
- **Modèles:**
  - `stg_customers` - Champs client renommés et normalisés
  - `stg_orders` - Données de commandes nettoyées
  - `stg_order_items` - Données d'article au niveau de la commande
  - `stg_products` - Dimension produit
  - `stg_supplies` - Dimension approvisionnement
  - `stg_locations` - Dimension localisation du magasin
- **Matérialisation:** Vues (légères, récupération rapide)

### Couche 3 : Modèles de marts
- **Localisation:** `models/marts/`
- **Objectif:** Ensembles de données analytiques prêts pour l'entreprise
- **Modèles:**
  - `customers` - Dimension client avec métriques lifetime
  - `orders` - Table de faits de commandes avec métriques calculées
  - `order_items` - Analyse au niveau des lignes
  - `products` - Dimension produit
  - `supplies` - Dimension chaîne d'approvisionnement
  - `locations` - Dimension magasin/localisation
  - `metricflow_time_spine` - Dimension temps pour agrégations
- **Matérialisation:** Tables (optimisées pour les requêtes)

## 🚀 Démarrage rapide

### Prérequis
- Python 3.8+
- PostgreSQL (pour la configuration par défaut) ou tout adaptateur dbt supporté
- Task (optionnel, pour la configuration automatisée) ou commandes shell directes
- Git (pour le contrôle de version)

### Installation

**Option 1: Utiliser Task (Recommandé)**
```bash
task load
```

Cela exécute toutes les étapes de configuration en séquence:
1. Crée un environnement virtuel Python
2. Installe dbt et l'adaptateur PostgreSQL
3. Génère des données d'exemple (6 ans)
4. Charge les données seed dans PostgreSQL
5. Nettoie les fichiers temporaires

**Option 2: Configuration manuelle**
```bash
# Créer un environnement virtuel
python3 -m venv dbt-env

# Activer l'environnement virtuel
# Sur Windows:
dbt-env\Scripts\activate
# Sur macOS/Linux:
source dbt-env/bin/activate

# Installer dbt et les dépendances
pip install --upgrade pip
pip install -r requirements.txt
pip install dbt-postgres

# Générer les données seed (6 ans de données d'exemple)
jafgen 6

# Déplacer les données générées vers le dossier seeds
mv jaffle-data seeds/

# Charger les seeds dans la base de données
dbt seed --full-refresh --vars '{"load_source_data": true}'
```

### Configuration

Mettez à jour `profiles.yml` avec vos identifiants PostgreSQL:

```yaml
jaffle_shop_profile:
  outputs:
    dev:
      type: postgres
      host: localhost
      user: postgres
      pass: your_password
      port: 5432
      dbname: jaffle_shop_db
      schema: analytics
      threads: 4
  target: dev
```

## 📁 Structure du projet

```
sandwich_pro/
├── models/
│   ├── staging/          # Nettoyage et préparation des données
│   │   ├── __sources.yml # Définitions des tables sources
│   │   ├── stg_*.sql     # Modèles de staging
│   │   └── stg_*.yml     # Documentation des colonnes
│   └── marts/            # Tables prêtes pour l'analytique
│       ├── customers.sql # Dimension client
│       ├── orders.sql    # Table de faits des commandes
│       ├── order_items.sql
│       ├── products.sql  # Dimension produit
│       ├── supplies.sql
│       ├── locations.sql
│       └── *.yml         # Tests et documentation des colonnes
├── seeds/
│   └── jaffle-data/      # Fichiers de données brutes en CSV
├── macros/               # Fonctions dbt personnalisées
│   ├── cents_to_dollars.sql    # Aide conversion de devises
│   └── generate_schema_name.sql # Convention de nommage des schémas
├── analyses/             # Requêtes SQL ad-hoc
├── data-tests/           # (Réservé pour tests personnalisés)
├── app.py                # Application Streamlit de gestion
├── dbt_project.yml       # Configuration du projet dbt
├── profiles.yml          # Paramètres de connexion BD (dev + prod)
├── .env.example          # Modèle de variables d'environnement
├── Taskfile.yml          # Automatisation des tâches (optionnel)
├── app_requirements.txt   # Dépendances de l'application
└── README.md             # Ce fichier
```

## 🌐 Application Web - Gestionnaire Jaffle Shop

Un tableau de bord basé sur Streamlit pour visualiser et gérer les analytiques Jaffle Shop.

### Exécution de l'application

```bash
# Installer les dépendances de l'application
pip install -r app_requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditez .env avec vos identifiants de base de données

# Lancer l'application
streamlit run app.py
```

L'application s'ouvrira à `http://localhost:8501`

### Fonctionnalités de l'application

**📈 Tableau de bord**
- Métriques clés: Clients totaux, commandes, revenus, clients fidèles
- Tendance des commandes dans le temps
- Distribution des revenus par type de client
- Produits les plus commandés
- Analyse des commandes par lieu

**👥 Clients**
- Rechercher les clients par nom
- Filtrer par nombre minimum de commandes
- Filtrer par type de client (nouveau/fidèle)
- Visualiser les métriques: dépense lifetime, nombre de commandes, dates

**🛒 Commandes**
- Filtrer par type de commande (Nourriture, Boisson, Mixte)
- Filtrer par coût minimum
- Trier par date, coût ou nombre d'articles
- Visualiser les détails, coûts et comptes d'articles

**📦 Produits**
- Rechercher le catalogue de produits
- Visualiser tous les produits avec tarification
- Trier par nom ou prix

**🏪 Localisations**
- Visualiser les performances par localisation
- Voir le nombre de commandes et les revenus par localisation
- Graphiques visuels pour l'analyse par localisation

**⚙️ Paramètres**
- Visualiser la configuration de la base de données
- Instructions de configuration BigQuery
- Informations sur l'application

### Dépendances de l'application

```
streamlit>=1.28.0
pandas>=2.0.0
psycopg2-binary>=2.9.0
plotly>=5.17.0
python-dotenv>=1.0.0
```

## 🔄 Commandes dbt

### Opérations dbt courantes

```bash
# Analyser et vérifier le projet
dbt parse

# Exécuter tous les modèles (actualiser le pipeline complet)
dbt run

# Exécuter un modèle spécifique
dbt run -s customers

# Exécuter avec vérification de fraîcheur
dbt source freshness

# Exécuter les tests (validations de colonnes, relations, unicité, etc.)
dbt test

# Générer la documentation
dbt docs generate
dbt docs serve  # Ouvre l'interface de documentation localement sur le port 8000

# Exécuter tout (run + test)
dbt build

# Actualisation complète (supprimer et recréer tous les modèles)
dbt run --full-refresh

# Mode débogage (utile pour le dépannage)
dbt debug
```

### Exécution sélective

```bash
# Exécuter uniquement les modèles de staging
dbt run -s path:models/staging

# Exécuter uniquement les modèles de marts
dbt run -s path:models/marts

# Exécuter un modèle et ses dépendances
dbt run -s +customers

# Exécuter un modèle et ses dépendants
dbt run -s customers+

# Exécuter les modèles modifiés depuis la branche main
dbt run -s state:modified+ --state ./target
```

## 📊 Documentation des modèles de données

### Dimension Clients
La table `customers` fournit une dimension client complète avec les métriques de valeur lifetime.

**Champs clés:**
- `customer_id` (Clé primaire)
- `customer_name`
- `count_lifetime_orders` - Total des commandes
- `lifetime_spend` - Revenu total
- `customer_type` - 'nouveau' ou 'fidèle'
- `first_ordered_at` - Date du premier achat
- `last_ordered_at` - Achat le plus récent

### Table de faits Commandes
La table `orders` est la table de faits contenant les métriques au niveau de la commande.

**Champs clés:**
- `order_id` (Clé primaire)
- `customer_id` (Clé étrangère)
- `order_cost` - Coût total des articles
- `order_items_subtotal` - Prix total avant taxes
- `count_food_items` - Nombre d'articles alimentaires
- `count_drink_items` - Nombre d'articles boisson
- `is_food_order` - Drapeau booléen
- `is_drink_order` - Drapeau booléen
- `customer_order_number` - Numéro d'ordre séquentiel par client

### Articles de commande
Données détaillées au niveau des articles pour chaque commande.

### Produits et Approvisionnements
Dimensions de produits et chaîne d'approvisionnement avec catégorisation et données de coût.

### Localisations
Dimension magasin/localisation pour l'analyse géographique.

## 🛠️ Macros

### cents_to_dollars
Convertit les centimes entiers en montants décimaux en dollars avec transtypage approprié, supportant plusieurs dialectes de base de données (PostgreSQL, BigQuery, Fabric).

**Utilisation:**
```sql
select
  product_id,
  {{ cents_to_dollars('price_cents') }} as price_dollars
from raw_products
```

### generate_schema_name
Implémentation personnalisée de convention de nommage des schémas.

## 🧪 Tests et qualité

Le projet inclut des tests de qualité des données définis dans les fichiers YAML:
- **Tests d'unicité** - Assurent que les clés primaires sont uniques
- **Tests de non-null** - Valident que les champs obligatoires sont remplis
- **Tests de relation** - Vérifient les relations de clés étrangères
- **Tests de valeurs acceptées** - Assurent que les champs catégoriques correspondent aux valeurs autorisées

Exécutez les tests avec:
```bash
dbt test
```

## 📚 Sources et lignage des données

Toutes les sources de données brutes sont définies dans `models/staging/__sources.yml`:
- **Schéma:** `raw`
- **Tables:** 6 tables sources du système ecom
- **Contrôles de fraîcheur:** Configurés pour les commandes et magasins

Visualisez le DAG de lignage avec:
```bash
dbt docs generate && dbt docs serve
```

## 🔐 Variables et configuration

Variables de projet définies dans `dbt_project.yml`:
- `dbt_date:time_zone` - Défini à "America/Los_Angeles"
- `load_source_data` - Contrôle le chargement des données seed (faux par défaut)

Remplacez à l'exécution:
```bash
dbt run --vars '{"load_source_data": true}'
```

## 🗄️ Support multi-bases de données (Dev et Prod)

Ce projet supporte à la fois PostgreSQL (développement) et BigQuery (production):

### Base de données de développement (PostgreSQL)
```yaml
jaffle_shop_profile:
  outputs:
    dev:
      type: postgres
      host: localhost
      port: 5432
      dbname: jaffle_shop_db
      schema: analytics
      threads: 4
  target: dev
```

**Exécution de dbt contre le développement:**
```bash
dbt run --target dev
dbt test --target dev
```

### Base de données de production (BigQuery)

Configurez BigQuery dans `profiles.yml`:
```yaml
prod:
  type: bigquery
  method: service-account
  project: your-gcp-project-id
  dataset: jaffle_shop_analytics
  keyfile: /path/to/service-account-key.json
  threads: 8
  location: US
  priority: interactive
```

**Étapes de configuration:**
1. Créer un projet Google Cloud
2. Créer un dataset BigQuery
3. Créer un compte de service avec rôle BigQuery Admin
4. Télécharger la clé JSON du compte de service
5. Mettre à jour `profiles.yml` avec l'ID du projet et le chemin de la clé
6. Installer l'adaptateur BigQuery:
   ```bash
   pip install dbt-bigquery
   ```

**Exécution de dbt contre la production:**
```bash
dbt run --target prod
dbt test --target prod
dbt docs generate --target prod
```

### Basculer entre les bases de données

Modifiez la cible par défaut dans `profiles.yml`:
```yaml
jaffle_shop_profile:
  target: dev  # ou 'prod'
```

Ou spécifiez à la ligne de commande:
```bash
dbt run --target prod
dbt test --target dev
```

## 🔄 Adaptateurs de base de données

Ce projet est configuré pour PostgreSQL et BigQuery. Pour ajouter d'autres adaptateurs:

1. **Installer l'adaptateur approprié:**
   ```bash
   pip install dbt-snowflake  # pour Snowflake
   pip install dbt-bigquery   # pour BigQuery
   ```

2. **Mettre à jour `profiles.yml`** avec les détails de connexion spécifiques à l'adaptateur

3. **Vérifier que les macros supportent le dialecte** (cents_to_dollars supporte: Postgres, BigQuery, Fabric)

## 📝 Git et CI/CD

Le projet inclut:
- `.pre-commit-config.yaml` - Hooks de pré-commit pour la qualité du code
- `.sqlfluff` - Règles de linting SQL
- `.github/` - Workflows GitHub Actions (si configurés)

## 🐛 Dépannage

### Problèmes de connexion
```bash
dbt debug  # Vérifier la connexion à la base de données
```

### Erreurs de compilation des modèles
```bash
dbt parse  # Analyser et valider Jinja2 et SQL
```

### Données manquantes
Assurez-vous que les seeds sont chargées:
```bash
dbt seed --full-refresh
```

### Problèmes de schéma
Réinitialiser et reconstruire:
```bash
dbt run --full-refresh
dbt test
```

## 📦 Dépendances

**Dépendances Python:**
- dbt-core >= 1.5.0
- dbt-postgres (ou adaptateur de choix)
- Paquets additionnels dans `requirements.txt`

**Paquets dbt:**
- dbt-utils - Macros utilitaires pour transformations courantes
- dbt-date - Fonctions utilitaires date/heure
- audit_helper - Validation et réconciliation des données

**Outils externes:**
- Task (optionnel) - Exécuteur d'automatisation de tâches
- SQLFluff - Formatage et linting du code SQL

## 🤝 Contribution

Lors de l'ajout de nouveaux modèles:

1. **Choisir la bonne couche:**
   - Staging: Nettoyage des données, renommage des champs, transtypage
   - Marts: Logique métier, agrégations, relations

2. **Suivre les conventions de nommage:**
   - Staging: `stg_<table_source>`
   - Marts: `<concept_métier>` (clients, commandes, etc.)

3. **Documenter tout:**
   - Ajouter la documentation YAML avec descriptions
   - Inclure les tests de colonnes (not-null, unique, relations)
   - Utiliser des commentaires SQL significatifs pour la logique complexe

4. **Tester votre travail:**
   ```bash
   dbt run -s +your_model_name
   dbt test -s your_model_name
   ```

## 📖 Ressources d'apprentissage

- [Documentation dbt](https://docs.getdbt.com/)
- [Meilleures pratiques dbt](https://docs.getdbt.com/guides/best-practices)
- [Analytics Engineering avec dbt](https://www.coursera.org/learn/analytics-engineering-with-dbt)
- [Documentation Streamlit](https://docs.streamlit.io/)
- [Documentation BigQuery](https://cloud.google.com/bigquery/docs)

## 📄 Licence

Ceci est un projet de démonstration/apprentissage.

## 🔗 Fichiers connexes

- **Configuration:** `dbt_project.yml`, `profiles.yml`
- **Base de données:** PostgreSQL (par défaut, configurable)
- **Exécution:** `Taskfile.yml` pour les workflows automatisés
- **Qualité du code:** `.sqlfluff`, `.pre-commit-config.yaml`

---

**Dernière mise à jour:** Juin 2026  
**Nom du projet:** Jaffle Shop  
**Statut:** Développement actif
