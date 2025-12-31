from flask import Flask, render_template, request
from splitlogic import compute_balances, settle_debts

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    names = request.form.getlist("name")
    amounts = list(map(float, request.form.getlist("amount")))

    total, share, balances = compute_balances(names, amounts)
    transactions = settle_debts(balances)

    return render_template("result.html",
                           names=names,
                           amounts=amounts,
                           total=total,
                           share=share,
                           balances=balances,
                           transactions=transactions)

if __name__ == "__main__":
    app.run(debug=True)