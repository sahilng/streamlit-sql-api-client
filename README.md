# DuckDB SQL Client

A Streamlit-based SQL client for querying a DuckDB HTTP API.

## Repository Structure

```
├── streamlit_app.py    # Streamlit application code
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Prerequisites

- Python 3.8+  
- pip  
- Streamlit  
- Requests  
- Pandas  

## Installation

1. **Clone the repository**  
   ```bash
   git clone <streamlit-repo-url>
   cd <repo-dir>
   ```

2. **Create and activate a virtual environment**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**  
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Configuration

The app requires access to your DuckDB HTTP API. In the Streamlit sidebar, specify:

- **API Host**: e.g. `http://localhost:8000`  
- **API Key**: your `DUCKDB_API_KEY` value  

No additional environment variables are needed for the client.

## Running the App

Launch the Streamlit app with:

```bash
streamlit run streamlit_app.py
```

The UI will open in your browser (usually at `http://localhost:8501`).

## Usage

- **Catalog Pane** (left): Browse attached databases, schemas, and tables. Click any table to auto-populate `SELECT * FROM schema.table LIMIT 10` in the query editor.  
- **SQL Pane** (right): Edit or enter any `SELECT` statement and click **Run Query**. Results display below.

## Customization

- To change the default port or browser behavior, use Streamlit command-line flags, e.g.:  
  ```bash
  streamlit run streamlit_app.py --server.port 8502
  ```
