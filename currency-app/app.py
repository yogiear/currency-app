from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API = "https://api.frankfurter.dev/v1"


@app.route("/", methods=["GET", "POST"])
def home():
    # Get the list of available currencies
    currencies = requests.get(f"{API}/currencies", timeout=10).json()
    result = None
    error = None
    form = {"amount": "1", "from_cur": "USD", "to_cur": "IDR"}

    if request.method == "POST":
        form = {
            "amount": request.form["amount"],
            "from_cur": request.form["from_cur"],
            "to_cur": request.form["to_cur"],
        }
        try:
            amount = float(form["amount"])
            if form["from_cur"] == form["to_cur"]:
                converted = amount
            else:
                r = requests.get(
                    f"{API}/latest",
                    params={
                        "amount": amount,
                        "base": form["from_cur"],
                        "symbols": form["to_cur"],
                    },
                    timeout=10,
                )
                r.raise_for_status()
                converted = r.json()["rates"][form["to_cur"]]
            result = f"{amount:,.2f} {form['from_cur']} = {converted:,.2f} {form['to_cur']}"
        except ValueError:
            error = "Please enter a valid number."
        except requests.RequestException:
            error = "Could not get exchange rates. Try again later."

    return render_template("index.html", currencies=currencies,
                           result=result, error=error, form=form)


if __name__ == "__main__":
    app.run(debug=True)