# 🥪 Jaffle Shop - Guide de démarrage rapide

Soyez opérationnel avec Jaffle Shop en quelques minutes!

## 1️⃣ Configuration initiale

### Option A: Configuration automatisée (Recommandée)
```bash
# Utilisez l'exécuteur Task pour automatiser tout
task load
```

Cela automatise:
- Crée un environnement virtuel Python
- Installe dbt et l'adaptateur PostgreSQL
- Génère 6 ans de données d'exemple
- Charge les données dans PostgreSQL

### Option B: Configuration manuelle
```bash
# Créer un environnement virtuel
python3 -m venv dbt-env

# Activer (Windows)
dbt-env\Scripts\activate
# Ou (macOS/Linux)
source dbt-env/bin/activate

# Installer dbt
pip install --upgrade pip
pip install -r requirements.txt
pip install dbt-postgres

# Générer et charger les données
jafgen 6
mv jaffle-data seeds/
dbt seed --full-refresh --vars '{"load_source_data": true}'
```

## 2️⃣ Configurer la connexion à la base de données

Modifiez `profiles.yml` avec vos identifiants PostgreSQL:
```yaml
jaffle_shop_profile:
  outputs:
    dev:
      type: postgres
      host: localhost
      user: postgres
      pass: YOUR_PASSWORD  # Changez ceci!
      port: 5432
      dbname: jaffle_shop_db
      schema: analytics
```

## 3️⃣ Exécuter le pipeline dbt

```bash
# Tester la connexion
dbt debug

# Exécuter toutes les transformations
dbt run

# Exécuter les tests
dbt test

# Ou exécuter les deux
dbt build

# Visualiser la documentation
dbt docs generate
dbt docs serve  # S'ouvre sur http://localhost:8000
```

## 4️⃣ Lancer l'application de gestion (Optionnel)

```bash
# Installer les dépendances de l'application
pip install -r app_requirements.txt

# Copier le modèle d'environnement
cp .env.example .env

# Exécuter l'application Streamlit
streamlit run app.py
```

S'ouvre sur: http://localhost:8501

### Fonctionnalités de l'application:
- **📈 Tableau de bord** - KPIs, tendances, analyse par localisation
- **👥 Clients** - Recherche, filtrage, métriques lifetime
- **🛒 Commandes** - Détails commandes, coûts, filtrage
- **📦 Produits** - Catalogue et tarification
- **🏪 Localisations** - Analyse de performance des magasins
- **⚙️ Paramètres** - Configuration de base de données

## 5️⃣ Configurer la production (BigQuery) - Optionnel

### Prérequis:
- Projet Google Cloud
- BigQuery activé
- Compte de service avec rôle BigQuery Admin

### Étapes:
```bash
# 1. Télécharger la clé JSON du compte de service

# 2. Installer l'adaptateur BigQuery
pip install dbt-bigquery

# 3. Mettre à jour profiles.yml (déjà configuré)
# Modifiez: project, dataset, chemin du fichier de clé

# 4. Exécuter contre la production
dbt run --target prod
dbt test --target prod
```

## 📊 Structure du projet

```
├── models/
│   ├── staging/      → Nettoyage des données (vues)
│   └── marts/        → Tables métier (tables)
├── seeds/            → Données CSV d'exemple
├── macros/           → Fonctions SQL personnalisées
├── app.py            → Tableau de bord Streamlit
├── dbt_project.yml   → Configuration dbt
├── profiles.yml      → Connexions aux bases de données
└── README.md         → Documentation complète
```

## 🔄 Commandes courantes

```bash
# Transformation de données
dbt run                    # Exécuter tous les modèles
dbt run -s customers       # Exécuter un modèle spécifique
dbt run -s path:models/marts  # Exécuter tous les marts

# Tests et validation
dbt test                   # Exécuter les tests
dbt source freshness       # Vérifier la fraîcheur des données

# Documentation
dbt docs generate
dbt docs serve

# Débogage
dbt debug                  # Tester la connexion
dbt parse                  # Vérifier la syntaxe

# Exécutions sélectives
dbt run -s +customers      # Avec dépendances
dbt run -s customers+      # Avec dépendants
```

## 🐛 Dépannage

| Problème | Solution |
|----------|----------|
| Connexion échouée | Exécutez `dbt debug` et vérifiez que PostgreSQL est lancé |
| Données manquantes | Exécutez `dbt seed --full-refresh` |
| Erreurs de modèle | Exécutez `dbt parse` pour vérifier la syntaxe SQL |
| Problèmes de schéma | Exécutez `dbt run --full-refresh` |
| Impossible de trouver profiles.yml | Assurez-vous qu'il est à la racine du projet (pas dans .gitignore) |

## 📚 Documentation

- **[README.md](README.md)** - Documentation complète du projet
- **[CLAUDE.md](CLAUDE.md)** - Guide de référence Claude Code
- **[dbt Docs](https://docs.getdbt.com/)** - Documentation officielle dbt
- **[Documentation Streamlit](https://docs.streamlit.io/)** - Documentation du framework d'application

## 🚀 Prochaines étapes

1. ✅ Terminer la configuration initiale (étapes 1-3)
2. ✅ Explorer les modèles dbt
3. ✅ Lancer l'application Streamlit (étape 4)
4. ✅ Ajouter des modèles personnalisés ou des tests
5. ✅ Configurer la production BigQuery (étape 5)

## 💡 Conseils

- Utilisez `dbt source freshness` pour monitorer la fraîcheur des données
- Ajoutez des tests dans les fichiers YAML pour la validation des données
- Utilisez `dbt test` pour valider la qualité des données
- Générez des docs avec `dbt docs serve` pour partager avec l'équipe
- Utilisez le cache de données Streamlit avec `@st.cache_data`

---

**Des questions?** Consultez les fichiers complets [README.md](README.md) ou [CLAUDE.md](CLAUDE.md).

**Dernière mise à jour:** Juin 2026
