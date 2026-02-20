import sqlite3
import dash
from dash import html, dcc, Input, Output, State


# ---------- DB ----------
conn = sqlite3.connect("tienda.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand TEXT,
    active INTEGER DEFAULT 1
)
""")

conn.commit()
conn.close()

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

    conn = sqlite3.connect("tienda.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO products (name, brand) VALUES (?, ?)",
        (name, brand)
    )

    conn.commit()
    conn.close()

    return "Producto guardado"

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)