import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="DuckDB SQL Client", layout="wide")
st.title("🔍 DuckDB SQL Client")

# — Sidebar: connection settings —
st.sidebar.header("Connection Settings")
api_host = st.sidebar.text_input("API Host (no trailing slash)", "http://localhost:8000")
api_key  = st.sidebar.text_input("API Key", type="password")

if not api_key:
    st.sidebar.error("🔑 Enter your API key above")
    st.stop()

# Helper to call your DuckDB HTTP API
def run_sql(sql: str) -> pd.DataFrame:
    resp = requests.post(
        f"{api_host.rstrip('/')}/query",
        headers={"X-API-Key": api_key, "Content-Type": "application/json"},
        json={"sql": sql},
        timeout=30,
    )
    resp.raise_for_status()
    return pd.DataFrame(resp.json().get("results", []))

# Initialize session state
if "query" not in st.session_state:
    st.session_state["query"] = ""
if "df" not in st.session_state:
    st.session_state["df"] = pd.DataFrame()
if "error" not in st.session_state:
    st.session_state["error"] = None

def select_and_run(catalog: str, schema: str, table: str):
    q = f"SELECT * FROM {catalog}.{schema}.{table} LIMIT 10"
    st.session_state["query"] = q
    try:
        st.session_state["df"] = run_sql(q)
        st.session_state["error"] = None
    except Exception as e:
        st.session_state["df"] = pd.DataFrame()
        st.session_state["error"] = str(e)

# Two-column layout
col1, col2 = st.columns([1, 2])

# ─── Column 1: Catalog ─────────────────────────────────────────────────────────
with col1:
    st.subheader("📚 Catalog")
    try:
        tables_df = run_sql("""
            SELECT table_catalog,
                   table_schema,
                   table_name
              FROM information_schema.tables
             WHERE table_type='BASE TABLE'
               AND table_schema NOT IN ('information_schema','pg_catalog')
             ORDER BY table_catalog, table_schema, table_name
        """)
    except Exception as e:
        st.error(f"Could not load catalog: {e}")
        st.stop()

    if tables_df.empty:
        st.info("No tables found.")
    else:
        for catalog, cat_group in tables_df.groupby("table_catalog"):
            st.markdown(f"### {catalog}")
            for schema, schema_group in cat_group.groupby("table_schema"):
                with st.expander(schema, expanded=False):
                    for tbl in schema_group["table_name"]:
                        st.button(
                            tbl,
                            key=f"{catalog}.{schema}.{tbl}",
                            on_click=select_and_run,
                            args=(catalog, schema, tbl),
                        )

# ─── Column 2: SQL Client ───────────────────────────────────────────────────────
with col2:
    st.subheader("🖋️ SQL Query")
    sql = st.text_area("SQL", value=st.session_state["query"], height=180)

    # Manual run as before
    if st.button("Run Query"):
        if not sql.strip():
            st.error("Enter a SQL statement first.")
        else:
            try:
                st.session_state["df"] = run_sql(sql)
                st.session_state["error"] = None
            except Exception as e:
                st.session_state["df"] = pd.DataFrame()
                st.session_state["error"] = str(e)

    # Show error or results
    if st.session_state["error"]:
        st.error(f"Query failed: {st.session_state['error']}")
    elif not st.session_state["df"].empty:
        st.success(f"Returned {len(st.session_state['df'])} row(s).")
        st.dataframe(st.session_state["df"], use_container_width=True, hide_index=True)
