from flask import Flask, render_template, request, redirect
from database import get_connection, init_db

app = Flask(__name__)
init_db()


@app.route("/")
def home():
    conn = get_connection()
    transactions = conn.execute(
        "SELECT * FROM transactions ORDER BY date DESC, id DESC"
    ).fetchall()
    totals = conn.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN type = 'income' THEN amount END), 0) AS income,
            COALESCE(SUM(CASE WHEN type = 'expense' THEN amount END), 0) AS expense
        FROM transactions
    """).fetchone()
    categories = conn.execute("""
        SELECT category, SUM(amount) AS total
        FROM transactions
        WHERE type = 'expense'
        GROUP BY category
        ORDER BY total DESC
    """).fetchall()
    conn.close()

    income = totals["income"]
    expense = totals["expense"]
    balance = income - expense
    return render_template(
        "index.html",
         transactions=transactions,
         income=income,
         expense=expense,
         balance=balance,
         categories=categories,
    )


@app.route("/add", methods=["POST"])
def add():
    amount = float(request.form["amount"])
    type_ = request.form["type"]
    category = request.form["category"]
    date = request.form["date"]
    note = request.form["note"]

    conn = get_connection()
    conn.execute(
        "INSERT INTO transactions (amount, type, category, date, note) VALUES(?, ?, ?, ?, ?)",
        (amount, type_, category, date, note),
    )
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_connection()
    conn.execute("DELETE FROM transactions WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_connection()

    if request.method == "POST":
        amount = float(request.form["amount"])
        type_ = request.form["type"]
        category = request.form["category"]
        date = request.form["date"]
        note = request.form["note"]
        conn.execute(
            "UPDATE transactions SET amount = ?, type = ?, category = ?, date = ?, note = ? WHERE id = ?",
            (amount, type_, category, date, note, id),
        )
        conn.commit()
        conn.close()
        return redirect("/")

    transaction = conn.execute(
        "SELECT * FROM transactions WHERE id = ?", (id,)
    ).fetchone()    
    conn.close()
    return render_template("edit.html", t=transaction)

if __name__ == "__main__":
    app.run(debug=True)
    

 