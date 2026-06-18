"""
Application de gestion Jaffle Shop
Une application Streamlit pour visualiser et gérer les analytiques Jaffle Shop
"""

import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Configuration de la page
st.set_page_config(
    page_title="Gestionnaire Jaffle Shop",
    page_icon="🥪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .header-title {
        color: #FF6B35;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .section-title {
        color: #FF6B35;
        font-size: 1.8em;
        margin-top: 30px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Fonction de connexion à la base de données
@st.cache_resource
def get_db_connection():
    """Créer une connexion à la base de données"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "261005"),
            database=os.getenv("DB_NAME", "jaffle_shop_db"),
            port=os.getenv("DB_PORT", 5432)
        )
        return conn
    except Exception as e:
        st.error(f"Échec de la connexion à la base de données: {e}")
        return None

@st.cache_data(ttl=300)
def query_db(query):
    """Exécuter une requête et retourner les résultats"""
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            results = cur.fetchall()
            return pd.DataFrame(results)
    except Exception as e:
        st.error(f"Query failed: {e}")
        return None
    finally:
        conn.close()

# En-tête
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="header-title">🥪 Gestionnaire Jaffle Shop</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f"*Mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

# Navigation de la barre latérale
st.sidebar.markdown("## 📊 Navigation")
page = st.sidebar.radio(
    "Sélectionner la vue",
    ["📈 Tableau de bord", "👥 Clients", "🛒 Commandes", "📦 Produits", "🏪 Localisations", "⚙️ Paramètres"],
    key="navigation"
)

# ============= PAGE TABLEAU DE BORD =============
if page == "📈 Tableau de bord":
    st.markdown('<div class="section-title">Vue d\'ensemble du tableau de bord</div>', unsafe_allow_html=True)

    # Métriques clés
    col1, col2, col3, col4 = st.columns(4)

    # Total des clients
    customers_df = query_db("SELECT COUNT(*) as count FROM analytics.customers")
    if customers_df is not None:
        with col1:
            st.metric("👥 Total des clients", int(customers_df['count'][0]))

    # Total des commandes
    orders_df = query_db("SELECT COUNT(*) as count FROM analytics.orders")
    if orders_df is not None:
        with col2:
            st.metric("🛒 Total des commandes", int(orders_df['count'][0]))

    # Revenu total
    revenue_df = query_db("SELECT SUM(lifetime_spend) as total FROM analytics.customers")
    if revenue_df is not None and revenue_df['total'][0]:
        with col3:
            st.metric("💰 Revenu total", f"${revenue_df['total'][0]:,.2f}")

    # Clients fidèles
    repeat_df = query_db("""
        SELECT COUNT(*) as count
        FROM analytics.customers
        WHERE customer_type = 'returning'
    """)
    if repeat_df is not None:
        with col4:
            st.metric("🔄 Clients fidèles", int(repeat_df['count'][0]))

    # Ligne de graphiques 1
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Commandes dans le temps")
        orders_time = query_db("""
            SELECT DATE(ordered_at) as order_date, COUNT(*) as count
            FROM analytics.orders
            GROUP BY DATE(ordered_at)
            ORDER BY order_date
        """)
        if orders_time is not None and not orders_time.empty:
            fig = px.line(orders_time, x='order_date', y='count',
                         title="Commandes quotidiennes", markers=True)
            fig.update_layout(xaxis_title="Date", yaxis_title="Nombre de commandes", hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Revenu par type de client")
        revenue_type = query_db("""
            SELECT customer_type, SUM(lifetime_spend) as total_spend
            FROM analytics.customers
            GROUP BY customer_type
        """)
        if revenue_type is not None and not revenue_type.empty:
            fig = px.pie(revenue_type, values='total_spend', names='customer_type',
                        title="Distribution des revenus")
            st.plotly_chart(fig, use_container_width=True)

    # Ligne de graphiques 2
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Produits les plus commandés")
        top_products = query_db("""
            SELECT p.product_name, COUNT(oi.order_item_id) as order_count
            FROM analytics.order_items oi
            JOIN analytics.products p ON oi.product_id = p.product_id
            GROUP BY p.product_id, p.product_name
            ORDER BY order_count DESC
            LIMIT 10
        """)
        if top_products is not None and not top_products.empty:
            fig = px.barh(top_products, x='order_count', y='product_name',
                         title="Top 10 produits")
            fig.update_layout(xaxis_title="Nombre de commandes", yaxis_title="Produit")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Commandes par localisation")
        orders_location = query_db("""
            SELECT l.location_name, COUNT(o.order_id) as order_count
            FROM analytics.orders o
            JOIN analytics.locations l ON o.location_id = l.location_id
            GROUP BY l.location_id, l.location_name
            ORDER BY order_count DESC
        """)
        if orders_location is not None and not orders_location.empty:
            fig = px.bar(orders_location, x='location_name', y='order_count',
                        title="Commandes par localisation")
            fig.update_layout(xaxis_title="Localisation", yaxis_title="Nombre de commandes")
            st.plotly_chart(fig, use_container_width=True)

# ============= PAGE CLIENTS =============
elif page == "👥 Clients":
    st.markdown('<div class="section-title">Gestion des clients</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_name = st.text_input("🔍 Rechercher par nom de client", "")
    with col2:
        min_orders = st.number_input("Min Commandes", value=0, step=1)
    with col3:
        customer_type = st.selectbox("Type", ["Tous", "nouveau", "fidèle"])

    # Construire la requête
    query = """
        SELECT customer_id, customer_name, count_lifetime_orders,
               lifetime_spend, customer_type, first_ordered_at, last_ordered_at
        FROM analytics.customers
        WHERE 1=1
    """

    if search_name:
        query += f" AND LOWER(customer_name) LIKE LOWER('%{search_name}%')"
    if min_orders > 0:
        query += f" AND count_lifetime_orders >= {min_orders}"
    if customer_type != "Tous":
        query += f" AND customer_type = '{customer_type}'"

    query += " ORDER BY lifetime_spend DESC"

    customers = query_db(query)

    if customers is not None and not customers.empty:
        st.dataframe(
            customers.style.format({
                'lifetime_spend': '${:,.2f}',
                'first_ordered_at': lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'),
                'last_ordered_at': lambda x: pd.Timestamp(x).strftime('%Y-%m-%d')
            }),
            use_container_width=True,
            hide_index=True
        )
        st.info(f"Total: {len(customers)} clients")
    else:
        st.warning("Aucun client trouvé")

# ============= PAGE COMMANDES =============
elif page == "🛒 Commandes":
    st.markdown('<div class="section-title">Gestion des commandes</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        order_type = st.selectbox(
            "Filtrer par type de commande",
            ["Tous", "Nourriture uniquement", "Boisson uniquement", "Mixte"]
        )
    with col2:
        min_cost = st.number_input("Coût minimum de la commande ($)", value=0.0, step=10.0)
    with col3:
        sort_by = st.selectbox("Trier par", ["Plus récent", "Coût le plus élevé", "Plus d'articles"])

    # Construire la requête
    query = "SELECT * FROM analytics.orders WHERE 1=1"

    if order_type == "Nourriture uniquement":
        query += " AND is_food_order = true AND is_drink_order = false"
    elif order_type == "Boisson uniquement":
        query += " AND is_drink_order = true AND is_food_order = false"
    elif order_type == "Mixte":
        query += " AND is_food_order = true AND is_drink_order = true"

    if min_cost > 0:
        query += f" AND order_items_subtotal >= {min_cost}"

    if sort_by == "Plus récent":
        query += " ORDER BY ordered_at DESC"
    elif sort_by == "Coût le plus élevé":
        query += " ORDER BY order_items_subtotal DESC"
    else:
        query += " ORDER BY count_order_items DESC"

    orders = query_db(query)

    if orders is not None and not orders.empty:
        st.dataframe(
            orders.style.format({
                'order_items_subtotal': '${:,.2f}',
                'order_cost': '${:,.2f}',
                'ordered_at': lambda x: pd.Timestamp(x).strftime('%Y-%m-%d %H:%M')
            }),
            use_container_width=True,
            hide_index=True
        )
        st.info(f"Total des commandes: {len(orders)} | Revenu total: ${orders['order_items_subtotal'].sum():,.2f}")
    else:
        st.warning("Aucune commande trouvée")

# ============= PAGE PRODUITS =============
elif page == "📦 Produits":
    st.markdown('<div class="section-title">Catalogue de produits</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        search_product = st.text_input("🔍 Rechercher des produits", "")
    with col2:
        sort_by = st.selectbox("Trier par", ["Nom", "Prix", "Commandes"])

    query = "SELECT * FROM analytics.products WHERE 1=1"

    if search_product:
        query += f" AND LOWER(product_name) LIKE LOWER('%{search_product}%')"

    if sort_by == "Prix":
        query += " ORDER BY product_price DESC"
    elif sort_by == "Commandes":
        query += " ORDER BY product_id DESC"
    else:
        query += " ORDER BY product_name"

    products = query_db(query)

    if products is not None and not products.empty:
        st.dataframe(
            products.style.format({
                'product_price': '${:,.2f}'
            }),
            use_container_width=True,
            hide_index=True
        )
        st.info(f"Total des produits: {len(products)}")
    else:
        st.warning("Aucun produit trouvé")

# ============= PAGE LOCALISATIONS =============
elif page == "🏪 Localisations":
    st.markdown('<div class="section-title">Emplacements des magasins</div>', unsafe_allow_html=True)

    locations = query_db("""
        SELECT location_id, location_name, COUNT(o.order_id) as order_count,
               SUM(o.order_items_subtotal) as total_revenue
        FROM analytics.locations l
        LEFT JOIN analytics.orders o ON l.location_id = o.location_id
        GROUP BY l.location_id, l.location_name
        ORDER BY order_count DESC
    """)

    if locations is not None and not locations.empty:
        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(locations, x='location_name', y='order_count',
                        title="Commandes par localisation")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.bar(locations, x='location_name', y='total_revenue',
                        title="Revenu par localisation", color='total_revenue')
            st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            locations.style.format({
                'total_revenue': '${:,.2f}'
            }),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("Aucune localisation trouvée")

# ============= PAGE PARAMÈTRES =============
elif page == "⚙️ Paramètres":
    st.markdown('<div class="section-title">Paramètres de l\'application</div>', unsafe_allow_html=True)

    with st.expander("📊 Configuration de la base de données", expanded=True):
        st.subheader("Configuration actuelle")
        st.code(f"""
DB_HOST: {os.getenv('DB_HOST', 'localhost')}
DB_USER: {os.getenv('DB_USER', 'postgres')}
DB_NAME: {os.getenv('DB_NAME', 'jaffle_shop_db')}
DB_PORT: {os.getenv('DB_PORT', 5432)}
SCHEMA: analytics
        """)
        st.info("Modifiez les variables d'environnement dans le fichier .env pour modifier la connexion à la base de données")

    with st.expander("🔄 Configuration BigQuery", expanded=False):
        st.subheader("Configuration de la base de données de production")
        st.write("""
Pour activer BigQuery comme base de données de production:

1. Configurer un projet Google Cloud
2. Créer un compte de service avec permissions BigQuery
3. Télécharger la clé JSON du compte de service
4. Mettre à jour profiles.yml avec le chemin du fichier de clé:
   ```
   keyfile: /path/to/service-account-key.json
   project: your-gcp-project-id
   ```
5. Exécuter: `dbt run --target prod`
        """)

    with st.expander("📝 À propos", expanded=False):
        st.write(f"""
**Gestionnaire Jaffle Shop**
- Version: 1.0.0
- Projet dbt: Jaffle Shop v3.0.0
- Base de données: PostgreSQL + BigQuery
- Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """)

# Pied de page
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em; margin-top: 30px;'>
    🥪 Gestionnaire Jaffle Shop | Données mises à jour automatiquement toutes les 5 minutes
</div>
""", unsafe_allow_html=True)
