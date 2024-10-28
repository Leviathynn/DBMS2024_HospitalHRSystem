from flask import Blueprint, render_template, request

views = Blueprint('views', __name__)

@views.route('/')
def info():
    return render_template("info.html")

@views.route("/calculations/", methods=['GET', 'POST'])
def calc():
    if request.method == 'POST' :
        ageInput = request.form.get('age')
        sexInput = request.form.get('sex')
        print(ageInput, sexInput)
    return render_template("calc.html")

@views.route("/references/")
def ref():
    return render_template("ref.html")