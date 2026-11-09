from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database connection
def get_db():
    conn = sqlite3.connect("shopping.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create database table
def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS shopping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            product TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

    #database run
    @app.route("/database")
    def database():
        conn = get_db()
        data = conn.execute("SELECT * FROM shopping").fetchall()
        conn.close()

        return render_template("database.html", data=data)

# Home page
@app.route("/")
def index():
    conn = get_db()

    items = conn.execute(
        "SELECT * FROM shopping"
    ).fetchall()

    conn.close()

    return render_template("index.html", items=items)

# Add shopping record
@app.route("/add", methods=["POST"])
def add():

    customer = request.form["customer"]
    product = request.form["product"]
    price = request.form["price"]
    quantity = request.form["quantity"]

    conn = get_db()

    conn.execute("""
        INSERT INTO shopping
        (customer, product, price, quantity)
        VALUES (?, ?, ?, ?)
    """, (customer, product, price, quantity))

    conn.commit()
    conn.close()

    return redirect("/")

# Delete shopping record
@app.route("/delete/<int:id>")
def delete(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM shopping WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    create_table()
    app.run(debug=True)