import math

from flask import Flask, flash
from flask import render_template
from flask import request
from app.calculator import *
from app.calculator_form import *
import os

SECRET_KEY = os.urandom(32)

ev_calculator_app = Flask(__name__)
ev_calculator_app.config['SECRET_KEY'] = SECRET_KEY

@ev_calculator_app.route('/', methods=['GET', 'POST'])
def operation_result():
    # request.form looks for:
    # html tags with matching "name="
    calculator_form = Calculator_Form(request.form)

    # validation of the form
    if request.method == "POST" and calculator_form.validate():
        # if valid, create calculator to calculate the time and cost
        calculator = Calculator()

        # extract information from the form
        battery_capacity = float(request.form['BatteryPackCapacity'])  # DataType: float
        initial_charge = float(request.form['InitialCharge'])  # DataType: float
        final_charge = float(request.form['FinalCharge'])  # DataType: float
        start_date = request.form['StartDate']  # DataType: string '%d/%m/%Y'
        start_date = datetime.strptime(start_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        start_time = request.form['StartTime']  # DataType: string
        charger_configuration = ChargerConfig(int(request.form['ChargerConfiguration']))  # DataType: object
        post_code = request.form['PostCode']  # DataType: string

        is_peak = calculator.is_peak(start_time)
        is_holiday = calculator.is_surcharge(start_date)
        time = float(
            calculator.time_calculation(initial_charge, final_charge, battery_capacity, charger_configuration.power))

        # Formatting result strings
        time_arr = [None, None, None]
        time_arr_id = [" days, ", " hours, ", " minutes"]
        time_formatted = ""

        time_arr[0] = (time // 1440)  # Time to complete charge in days
        time_arr[0] = "{:.0f}".format(time_arr[0])
        if time_arr[0] == 1: time_arr_id[0] = " day, "
        time_arr[1] = (time % 1440) // 60  # Time to complete charge in hours
        time_arr[1] = "{:.0f}".format(time_arr[1])
        if time_arr[1] == 1: time_arr_id[1] = " hour, "
        time_arr[2] = (time % 1440) % 60  # Time to complete charge in minutes
        time_arr[2] = "{:.2f}".format(time_arr[2])
        if time_arr[2] == 1: time_arr_id[2] = " minute"

        # outputting results string
        for i in range(len(time_arr)):
            if time_arr[i] != 0:
                for j in range(i, len(time_arr)):
                    time_formatted += str(time_arr[j]) + time_arr_id[j]
                break

        location = calculator.get_location(post_code)
        # Calculating cost
        if datetime.strptime(start_date, '%Y-%m-%d') <= datetime.now() + timedelta(days=-2):
            cost = calculator.cost_per_minute_solar(time, initial_charge, final_charge, battery_capacity, start_time,
                                                    start_date, charger_configuration, location)
        else:
            cost = calculator.cost_per_minute_solar_extended(time, initial_charge, final_charge, battery_capacity,
                                                             start_time, start_date, charger_configuration, location)

        #Formatting cost
        cost_formatted = "$" + "{:.2f}".format(cost)

        # values of variables can be sent to the template for rendering the webpage that users will see
        return render_template('calculator.html', cost=cost_formatted, time=time_formatted,
                               calculation_success=True, form=calculator_form)

    else:
        # If error occurs:
        flash_errors(calculator_form)
        return render_template('calculator.html', calculation_success=False, form=calculator_form)


# method to display all errors
def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


if __name__ == '__main__':
    ev_calculator_app.run()
