# Guide du projet - Projet dbt Jaffle Shop

## Référence rapide

**Type de projet:** Projet dbt Analytics Engineering  
**Base de données:** PostgreSQL (configurable vers BigQuery, Snowflake, etc.)  
**Langage principal:** SQL avec modèles Jinja2  
**Version:** 3.0.0

## Vue d'ensemble du projet

Ceci est un projet dbt (data build tool) de démonstration pour un pipeline d'analytique e-commerce. Il transforme les données brutes en ensembles de données analytiques propres suivant l'architecture médaillon à trois couches:

- **Couche brute:** Seeds (fichiers CSV)
- **Couche staging:** Nettoyage et standardisation des données (vues)
- **Couche marts:** Tables analytiques prêtes pour l'entreprise

## Fichiers et répertoires clés

### Configuration
- `dbt_project.yml` - Configuration dbt principale, paramètres de matérialisation des modèles
- `profiles.yml` - Détails de connexion à la base de données (PostgreSQL par défaut + BigQuery en prod)
- `Taskfile.yml` - Exécuteur de tâches automatisé pour la configuration et les tests

### Modèles
- `models/staging/` - Nettoyage des données brutes et standardisation des champs
- `models/marts/` - Tables de logique métier agrégée
- Chaque modèle a un fichier YAML correspondant avec tests de colonnes et descriptions

### Données
- `seeds/jaffle-data/` - 6 fichiers CSV avec données e-commerce d'exemple (générées par jafgen)
- Les données incluent: clients, commandes, articles, produits, magasins, approvisionnements

### Code personnalisé
- `macros/cents_to_dollars.sql` - Aide de conversion de devises multi-base de données
- `macros/generate_schema_name.sql` - Convention de nommage des schémas

### Application
- `app.py` - Tableau de bord Streamlit avec 6 pages de gestion
- `app_requirements.txt` - Dépendances Python pour l'application

## Tâches courantes

### Configuration et chargement des données
```bash
task load  # Configuration complète avec données seed
```

### Exécution de dbt
```bash
dbt run              # Transformer tous les modèles
dbt test             # Exécuter les tests de qualité des données
dbt build            # Run + test (recommandé)
dbt docs generate && dbt docs serve  # Visualiser la documentation
```

### Exécution sélective
```bash
dbt run -s customers         # Exécuter un modèle spécifique
dbt run -s +customers        # Inclure les dépendances
dbt run -s path:models/marts # Exécuter tous les modèles de marts
```

### Lancer l'application de gestion
```bash
pip install -r app_requirements.txt
cp .env.example .env  # Configurer les identifiants de base de données
streamlit run app.py
```
L'application s'ouvre sur http://localhost:8501

## Détails de la structure du projet

### Modèles de staging (stg_*)
- Objectif: Nettoyer et renommer les champs bruts, conversions de type basiques
- Matérialisés comme des vues (rapides, légers)
- Mappage un-à-un avec les tables brutes
- Localisés dans: `models/staging/`

### Modèles de marts
- **customers** - Dimension client avec métriques lifetime
- **orders** - Table de faits de commandes avec champs calculés
- **order_items** - Détail au niveau des articles
- **products** - Dimension produit
- **supplies** - Dimension chaîne d'approvisionnement
- **locations** - Localisations des magasins
- **metricflow_time_spine** - Dimension temps

### Colonnes clés à connaître

**Clients:**
- `customer_id` (CL)
- `lifetime_spend` - Revenu total par client
- `customer_type` - 'nouveau' ou 'fidèle'

**Commandes:**
- `order_id` (CL)
- `customer_id` (CF)
- `order_cost` - Coût total d'approvisionnement
- `is_food_order`, `is_drink_order` - Drapeaux de catégorie

## Tests et qualité

Tous les modèles incluent des définitions YAML avec:
- Descriptions des colonnes
- Tests d'unicité (validation CL)
- Tests de non-null
- Tests de relation (validation CF)
- Tests de valeurs acceptées

Visualisez les tests dans: `models/<couche>/<modèle>.yml`

## Sources et fraîcheur

Données sources brutes définies dans: `models/staging/__sources.yml`
- Schéma: `raw`
- Tables: raw_customers, raw_orders, raw_items, raw_products, raw_stores, raw_supplies
- Contrôles de fraîcheur sur les commandes et magasins

## Configuration multi-bases de données

**Architecture à deux niveaux:**

### Développement (PostgreSQL)
- Base de données locale sur le port 5432
- Nom de la cible: `dev`
- Cible par défaut
- Utilisée pour les tests et le développement

### Production (BigQuery)
- Nom de la cible: `prod`
- Nécessite un projet Google Cloud + compte de service
- Concurrence plus élevée (8 threads vs 4)
- Pour l'analytique d'entreprise

**Basculer entre les bases de données:**
```bash
dbt run --target dev   # Développement
dbt run --target prod  # Production (BigQuery)
```

**Configuration de la production:**
1. Créer un projet GCP et un dataset BigQuery
2. Créer un compte de service avec permissions BigQuery
3. Télécharger le fichier de clé JSON
4. Mettre à jour `profiles.yml` avec l'ID du projet et le chemin du fichier de clé
5. Installer l'adaptateur: `pip install dbt-bigquery`

## Application Web (Streamlit)

**Fichier:** `app.py`
**Dépendances:** `app_requirements.txt`

**Fonctionnalités:**
- Tableau de bord avec KPIs et graphiques
- Recherche et filtrage des clients
- Gestion et analyse des commandes
- Catalogue de produits
- Performance des localisations
- Paramètres et configuration

**Exécution:** `streamlit run app.py` → http://localhost:8501

**Sources de données:** Se connecte à PostgreSQL (dev) ou BigQuery (prod) via variables d'environnement dans `.env`

## Dépannage

```bash
dbt debug              # Tester la connexion à la base de données
dbt parse              # Vérifier la syntaxe SQL/Jinja2
dbt run --fail-fast    # Arrêter à la première erreur
dbt run -s model --debug  # Logging verbeux
```

## Hooks de pré-commit

Configurés dans `.pre-commit-config.yaml`:
- Linting SQL avec SQLFluff (règles `.sqlfluff`)
- Formatage Python

## Prochaines étapes pour amélioration

- Ajouter des modèles de marts plus sophistiqués pour des unités métier spécifiques
- Implémenter la matérialisation incrémentale pour les grandes tables
- Ajouter des modèles snapshot pour les dimensions qui changent lentement
- Créer des tests dbt génériques pour des patterns de validation courants
- Configurer dbt Cloud pour l'automatisation CI/CD

## Nouveaux fichiers ajoutés

- **app.py** - Tableau de bord Streamlit avec 6 pages
- **app_requirements.txt** - Dépendances Python pour l'application
- **.env.example** - Modèle de variables d'environnement pour la configuration de base de données
- **profiles.yml** - Mise à jour avec cible production BigQuery

## Ressources de support

- [README.md](./README.md) - Documentation complète du projet
- [dbt Docs](https://docs.getdbt.com/)
- [Meilleures pratiques dbt](https://docs.getdbt.com/guides/best-practices)
- [Documentation Streamlit](https://docs.streamlit.io/)
- [Documentation BigQuery](https://cloud.google.com/bigquery/docs)
