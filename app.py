import os
import psycopg
import dash
from dash import html, dcc, Input, Output, State


# ---------- DB ----------

def _db_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        # fallback local for development if you want
        return "postgresql://localhost:5432/casita"
    # Render often uses postgres://, psycopg prefers postgresql://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


def get_conn():
    return psycopg.connect(_db_url())


# create table on startup
with get_conn() as conn:
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                brand TEXT,
                active INTEGER DEFAULT 1
            )
            """
        )


# ---------- APP ----------
app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H3("Alta de producto"),

    dcc.Input(
        id="name",
        placeholder="Nombre del producto",
        type="text"
    ),
    html.Br(),

    dcc.Input(
        id="brand",
        placeholder="Marca",
        type="text"
    ),
    html.Br(), html.Br(),

    html.Button("Guardar", id="save"),
    html.Br(), html.Br(),

    html.Div(id="msg")
])

# ---------- CALLBACK ----------
@app.callback(
    Output("msg", "children"),
    Input("save", "n_clicks"),
    State("name", "value"),
    State("brand", "value")
)
def save_product(n, name, brand):
    if not n or not name:
        return ""

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO products (name, brand) VALUES (%s, %s)",
                (name, brand)
            )

    return "Producto guardado"

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))