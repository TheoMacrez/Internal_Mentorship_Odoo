from datetime import date

from flask import Blueprint, redirect, render_template, request, url_for

from repositories.employee_repository import EmployeeRepository
from services.employee_service import EmployeeService

employee_blueprint = Blueprint("employees", __name__)

employee_service = EmployeeService(EmployeeRepository())


@employee_blueprint.route("/employees")
def employees_index():
    return redirect(url_for("employees.select_employee"))


@employee_blueprint.route("/employees/new", methods=["GET", "POST"])
def create_employee():
    error = None

    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        birth_date_value = request.form.get("birth_date", "").strip()

        try:
            birth_date = date.fromisoformat(birth_date_value)
            employee = employee_service.create_employee(
                first_name,
                last_name,
                email,
                phone,
                birth_date
            )
            return redirect(url_for(
                "employees.employee_hub",
                employee_id=employee.id_employee
            ))
        except ValueError as exception:
            error = str(exception)

    return render_template("employee_form.html", error=error)


@employee_blueprint.route("/employees/select")
def select_employee():
    employees_list = employee_service.get_all_employees()

    return render_template(
        "employee_select.html",
        employees=employees_list
    )


@employee_blueprint.route("/employees/connect", methods=["POST"])
def connect_employee():
    employee_id = request.form.get("employee_id")

    return redirect(url_for(
        "employees.employee_hub",
        employee_id=employee_id
    ))


@employee_blueprint.route("/employees/<int:employee_id>/hub")
def employee_hub(employee_id):
    employee = employee_service.get_employee_by_id(employee_id)

    if not employee:
        return redirect(url_for("employees.select_employee"))

    return render_template(
        "employee_hub.html",
        employee=employee
    )
