from flask import Flask, render_template

from controllers.employee_controller import employee_blueprint

app = Flask(__name__)

app.register_blueprint(employee_blueprint)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
