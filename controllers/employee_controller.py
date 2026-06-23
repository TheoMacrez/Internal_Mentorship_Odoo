from datetime import date

from flask import Blueprint, redirect, render_template, request, url_for

from repositories.employee_repository import EmployeeRepository
from services.employee_service import EmployeeService

employee_blueprint = Blueprint("employees", __name__)

employee_service = EmployeeService(EmployeeRepository())


@employee_blueprint.route("/")
def index():
    return redirect(url_for("employees.list_employees"))


@employee_blueprint.route("/employees", methods=["GET", "POST"])
def list_employees():
    error = None

    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        birth_date_value = request.form.get("birth_date", "").strip()

        try:
            birth_date = date.fromisoformat(birth_date_value)
            employee_service.create_employee(
                first_name,
                last_name,
                email,
                phone,
                birth_date
            )
            return redirect(url_for("employees"))
        except ValueError as exception:
            error = str(exception)

    employees_list = employee_service.get_all_employees()

    return render_template(
        "employees.html",
        employees=employees_list,
        error=error
    )