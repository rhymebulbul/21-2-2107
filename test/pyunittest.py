import os
from app.calculator import *
from app.calculator_form import *
import unittest
from flask import Flask
from werkzeug.datastructures import ImmutableMultiDict, MultiDict
from wtforms import ValidationError
from datetime import datetime


class TestFormValidators(unittest.TestCase):
    def test_validate_BatteryPackCapacity(self):
        """
        Author: Christian Zubcic
        This tests that only positive numbers are accepted as valid inputs for battery pack capacity
        Valid Inputs: positive numbers
        Invalid Inputs: a negative number (out-point), 0 since it is a boundary off-point, a string (invalid data type),
        and a blank input.
        """
        valid_inputs = [1, 100]
        invalid_inputs = [-10, 0, "a", ""]
        invalid_outputs = [ValueError, ValueError, ValueError, ValidationError]
        inputs = [valid_inputs, invalid_inputs]

        for i in range(len(inputs)):
            # Creating mock data structures to replicate the user form
            for j in range(len(inputs[i])):
                form = None
                SECRET_KEY = os.urandom(32)

                data = MultiDict()
                data.add('BatteryPackCapacity', inputs[i][j])
                mock_data = ImmutableMultiDict(data)

                app = Flask(__name__)
                app.config['SECRET_KEY'] = SECRET_KEY

                with app.test_request_context('/'):
                    form = Calculator_Form(mock_data)

                # Testing valid inputs do not raise any exceptions
                if i == 0:
                    try:
                        Calculator_Form.validate_BatteryPackCapacity(form, form.BatteryPackCapacity)
                    except Exception:
                        self.fail("validate_BatteryPackCapacity() unexpectedly raised exception")

                else:
                    # Testing invalid inputs raise exceptions and are handled
                    self.assertRaises(invalid_outputs[j], lambda: Calculator_Form.validate_BatteryPackCapacity(form, form.BatteryPackCapacity))

    def test_validate_Charges(self):
        """
        Author: Christian Zubcic
        This tests that only the initial and final charge states are positve, are valid percentages and that the initial
        charge is less than the final charge
        Valid Inputs (initial charge, final charge): (0,100) - boundary on-points, (50,60) - valid in-points
        Invalid Inputs: (100, 50) - final charge is greater than initial charge, (-50, 150) - boundary out-points are
        used, (50, 50) - initial charge is not smaller than final charge, ("a", "b") - incorrect data types are used,
        ("", "") - input fields are blank. These should all be handled as errors.
        """
        valid_inputs = [(0, 100), (50, 60)]
        invalid_inputs = [(100, 50), (-50, 150), (50, 50), ("a", "b"), ("", "")]
        invalid_outputs = [ValueError, ValueError, ValueError, ValueError, ValidationError]
        inputs = [valid_inputs, invalid_inputs]

        # Creating mock data to mimic user input form
        for i in range(len(inputs)):
            for j in range(len(inputs[i])):
                form = None
                SECRET_KEY = os.urandom(32)

                data = MultiDict()
                data.add('InitialCharge', inputs[i][j][0])
                data.add('FinalCharge', inputs[i][j][1])
                mock_data = ImmutableMultiDict(data)

                app = Flask(__name__)
                app.config['SECRET_KEY'] = SECRET_KEY

                with app.test_request_context('/'):
                    form = Calculator_Form(mock_data)

                if i == 0:
                    # Testing valid inputs do not raise any exceptions
                    try:
                        Calculator_Form.validate_InitialCharge(form, form.InitialCharge)
                    except Exception:
                        self.fail("validate_InitialCharge() unexpectedly raised exception")

                    try:
                        Calculator_Form.validate_FinalCharge(form, form.FinalCharge)
                    except Exception:
                        self.fail("validate_FinalCharge() unexpectedly raised exception")

                # Testing that invalid inputs do raise exceptions
                else:
                    self.assertRaises(invalid_outputs[j], lambda: Calculator_Form.validate_InitialCharge(form, form.InitialCharge))
                    self.assertRaises(invalid_outputs[j], lambda: Calculator_Form.validate_FinalCharge(form, form.FinalCharge))

    def test_validate_StartDate(self):
        """
        Author: Christian Zubcic
        This tests that the non-existent dates are handled when inputted
        Valid Inputs: "1/1/2021" - lower boundary on-point for days and months, "31/12/2021" - upper boundary on-point
        for days and months, "29/2/2020" - testing leap year date is valid, "05/05/2021" - testing padded values are
        considered valid.
        Invalid Inputs: "29/2/2021" - non-leap year leap day (also an off point), "2.5/abc/!.." - invalid data type
        for inputs, "5.5.2021" - incorrect formatting, "" - field left blank
        """
        valid_inputs = ["1/1/2021", "31/12/2021", "29/2/2020", "05/05/2021"]
        invalid_inputs = ["29/2/2021", "2.5/abc/!..", "5.5.2021", ""]
        invalid_outputs = [ValueError, ValueError, ValueError, ValidationError]
        inputs = [valid_inputs, invalid_inputs]

        # Creating mock data to mimic user input form
        for i in range(len(inputs)):
            for j in range(len(inputs[i])):
                form = None
                SECRET_KEY = os.urandom(32)

                data = MultiDict()
                data.add('StartDate', inputs[i][j])
                mock_data = ImmutableMultiDict(data)

                app = Flask(__name__)
                app.config['SECRET_KEY'] = SECRET_KEY

                with app.test_request_context('/'):
                    form = Calculator_Form(mock_data)

                if i == 0:
                    # Checking valid inputs do not raise errors
                    try:
                        Calculator_Form.validate_StartDate(form, form.StartDate)
                    except Exception:
                        self.fail("validate_StartDate() unexpectedly raised exception")

                else:
                    # Checking invalid inputs do raise errors
                    self.assertRaises(invalid_outputs[j], lambda: Calculator_Form.validate_StartDate(form, form.StartDate))

    def test_validate_StartTime(self):
        """
        Author: Christian Zubcic
        This tests that inputted time is validated correctly, and invalid inputs are raised
        Valid Inputs: "00:00", "23:59" - lower and upper boundary on-points; "5:00" - in-point; "05:30" - padded time
        Invalid Inputs: "25:60" - exceeding boundary off-point for both hours and minutes; "ab:cd" - non-numerical
        entry; "12-00" - invalid hour:minute separator; "" - blank input
        """
        valid_inputs = ["00:00", "5:00", "05:30", "23:59"]
        invalid_inputs = ["25:60", "ab:cd", "12-00", ""]
        invalid_outputs = [ValueError, ValueError, ValueError, ValidationError]
        inputs = [valid_inputs, invalid_inputs]

        # Mocking user input form for start time
        for i in range(len(inputs)):
            for j in range(len(inputs[i])):
                form = None
                SECRET_KEY = os.urandom(32)

                data = MultiDict()
                data.add('StartTime', inputs[i][j])
                mock_data = ImmutableMultiDict(data)

                app = Flask(__name__)
                app.config['SECRET_KEY'] = SECRET_KEY

                with app.test_request_context('/'):
                    form = Calculator_Form(mock_data)

                if i == 0:
                    # Testing valid inputs do not raise any errors
                    try:
                        Calculator_Form.validate_StartTime(form, form.StartTime)
                    except Exception:
                        self.fail("validate_StartTime() unexpectedly raised exception")

                else:
                    # Testing invalid inputs raise errors
                    self.assertRaises(invalid_outputs[j], lambda: Calculator_Form.validate_StartTime(form, form.StartTime))


    def test_validate_ChargerConfiguration(self):
        """
        Author: Christian Zubcic
        This tests that non-valid charger configurations are rejected and valid ones are accepted
        Valid Inputs: 1, 8 - upper and lower boundary on-points; 4 - in-point
        Invalid Inputs: 1.3 - non-integer input; 0, 9 - lower and upper boundary off-points; "a" - non-numerical input;
        "" - input field left empty
        """
        valid_inputs = [1, 4, 8]
        invalid_inputs = [1.3, 0, 9, "a", ""]
        invalid_outputs = [ValueError, ValueError, ValueError, ValueError, ValidationError]
        inputs = [valid_inputs, invalid_inputs]

        # Mocking charger configuration input
        for i in range(len(inputs)):
            for j in range(len(inputs[i])):
                form = None
                SECRET_KEY = os.urandom(32)

                data = MultiDict()
                data.add('ChargerConfiguration', inputs[i][j])
                mock_data = ImmutableMultiDict(data)

                app = Flask(__name__)
                app.config['SECRET_KEY'] = SECRET_KEY

                with app.test_request_context('/'):
                    form = Calculator_Form(mock_data)

                if i == 0:
                    # checking valid inputs do not raise errors
                    try:
                        Calculator_Form.validate_ChargerConfiguration(form, form.ChargerConfiguration)
                    except Exception:
                        self.fail("validate_ChargerConfiguration() unexpectedly raised exception")

                else:
                    # testing invalid inputs raise errors
                    self.assertRaises(invalid_outputs[j], lambda: Calculator_Form.validate_ChargerConfiguration(form, form.ChargerConfiguration))

    def test_validate_PostCode(self):
        """
        Author: Christian Zubcic
        This tests that non-valid charger postcodes are rejected and valid ones are accepted
        Valid Inputs: 3000, 4000, 1000 - 4-digit integers
        Invalid Inputs: 1 - not 4 digits; a - wrong data type; "" - blank input;
        "" - input field left empty
        """
        valid_inputs = ["3000", "4000", "1000"]
        invalid_inputs = ["1", "a", ""]
        invalid_outputs = [ValueError, ValueError, ValidationError]
        inputs = [valid_inputs, invalid_inputs]

        # Mocking charger configuration input
        for i in range(len(inputs)):
            for j in range(len(inputs[i])):
                form = None
                SECRET_KEY = os.urandom(32)

                data = MultiDict()
                data.add('PostCode', inputs[i][j])
                mock_data = ImmutableMultiDict(data)

                app = Flask(__name__)
                app.config['SECRET_KEY'] = SECRET_KEY

                with app.test_request_context('/'):
                    form = Calculator_Form(mock_data)

                if i == 0:
                    # checking valid inputs do not raise errors
                    try:
                        Calculator_Form.validate_PostCode(form, form.PostCode)
                    except Exception:
                        self.fail("validate_ChargerConfiguration() unexpectedly raised exception")

                else:
                    # testing invalid inputs raise errors
                    self.assertRaises(invalid_outputs[j], lambda: Calculator_Form.validate_PostCode(form, form.PostCode))


class TestCalculator(unittest.TestCase):
    def test_is_peak(self):
        """
        Author: Christian Zubcic
        This tests that is_peak function returns True if time is between 6:00 and 18:00 and false otherwise
        Expected True: "6:00", "17:59" - lower and upper boundary on-points; "12:00" - in-point
        Expected False: "5:59", "18:00" - lower and upper boundary off-points; "00:00" - out-point
        """
        self.calculator = Calculator()
        test_inputs = ["6:00", "17:59", "12:00", "5:59", "18:00", "00:00"]
        expected_output = [True, True, True, False, False, False]

        for i in range(len(test_inputs)):
            self.assertEquals(self.calculator.is_peak(test_inputs[i]), expected_output[i])


    def test_is_surcharge(self):
        """
        Author: Christian Zubcic
        This tests that surcharges are applied for weekdays and holidays, and not applied for weekends
        Expected True: "25/4/2022" - Weekend and a holiday, "25/12/2010" - a weekend holiday lower than the range of
        the csv data file, "24/9/2021" - a regular weekday
        Expected False: "26/9/2021" -  a regular weekend day; "14/8/2010" - a regular weekend below csv range
        """
        self.calculator = Calculator()

        test_inputs = ['2022-01-01', '2010-12-25', '2023-12-25', '2027-09-25', '2021-09-26', '2021-09-24', '2021-09-27']
        expected_output = [True, True, True, False, False, True, True]

        for i in range(len(test_inputs)):
            self.assertEquals(self.calculator.is_surcharge(test_inputs[i]), expected_output[i])

    # Tests both time incrementer and date incrementer
    def test_time_incrementer(self):
        """
        Author: Christian Zubcic
        This tests that time is incremented correctly when passing through the time_incrementer function, and that the
        date is also correctly incremented if time surpasses midnight
        Test Inputs: ("23:59", "31/12/2020") - tests time resets to 00:00 and day/month/year of date is all incremented,
        ("23:59", "28/2/2020") - testing leap years are considered in date increment, ("00:00", "26/9/2021") - testing
        minute increments without date changing using lower boundary on point, ("11:59", "26/9/2021") - testing time
        increment with in-point
        """
        self.calculator = Calculator()
        test_inputs = [('23:59', '2020-12-31'), ('23:59', '2010-12-25'), ('23:59', '2021-02-28'),
                       ('23:59', '2020-02-28'), ('00:00', '2021-09-26'), ('11:59', '2021-09-26')]
        expected_outputs = [('00:00', '2021-01-01'), ('00:00', '2010-12-26'), ('00:00', '2021-03-01'),
                            ('00:00', '2020-02-29'), ('00:01', '2021-09-26'), ('12:00', '2021-09-26')]

        for i in range(len(test_inputs)):
            time, date = self.calculator.time_incrementer(test_inputs[i][0], test_inputs[i][1])
            self.assertEquals(time, expected_outputs[i][0])
            self.assertEquals(datetime.strptime(date, '%Y-%m-%d'),
                              datetime.strptime(expected_outputs[i][1], '%Y-%m-%d'))


    def test_time_calculation(self):
        """
        Author: Christian Zubcic
        This tests that the time_calculation function is valid using logic and some random examples
        Justification for test cases explained in block comments
        """
        self.calculator = Calculator()

        # Mocking configuration data structure
        configuration_powers = []
        for i in range(1, 9):
            configuration_powers.append(ChargerConfig(i).power)

        # Power increases with each configuration. This changes only the configuration used by each function and
        # validates correctness by testing that higher charger configuration number should take less time than smaller
        # configuration numbers.
        for i in range(1, len(configuration_powers)):
            self.assertTrue(self.calculator.time_calculation(0, 100, 100, configuration_powers[i]) < self.calculator.time_calculation(0, 100, 100, configuration_powers[i-1]))

        # This test uses similar logic, however only the capacity of the vehicle changes. As the list of inputs is
        # ascending, each preceeding capacity should take LESS time to charge than the proceeding capacity
        test_capacities = [10, 50, 100, 500, 1000]
        for i in range(1, len(test_capacities)):
            self.assertTrue(self.calculator.time_calculation(0, 100, test_capacities[i], 350) > self.calculator.time_calculation(0, 100, test_capacities[i-1], 350))

        # This tests that the total charge (final - initial) returns the same values regardless of the implicit
        # initial and final charges are. Also tests that larger charges take more time than smaller ranges.
        test_ranges = [(0, 50), (30, 80), (50, 100), (0, 100)]
        self.assertTrue(self.calculator.time_calculation(test_ranges[0][0], test_ranges[0][1], 100, 350) == self.calculator.time_calculation(test_ranges[1][0], test_ranges[1][1], 100, 350) == self.calculator.time_calculation(test_ranges[2][0], test_ranges[2][1], 100, 350))
        self.assertTrue(self.calculator.time_calculation(test_ranges[0][0], test_ranges[0][1], 100, 350) < self.calculator.time_calculation(test_ranges[3][0], test_ranges[3][1], 100, 350))

        # Random test cases which were solved by hand to check the values being returned are correct as well as the
        # above logic
        self.assertEqual(float("{:.2f}".format(self.calculator.time_calculation(20, 80, 82, configuration_powers[8-1]))), 8.43)
        self.assertEqual(float("{:.2f}".format(self.calculator.time_calculation(0, 100, 100, configuration_powers[1-1]))), 3000)
        self.assertEqual(float("{:.2f}".format(self.calculator.time_calculation(50, 100, 10, configuration_powers[4-1]))), 27.27)

    def test_get_location(self):
        """
        Author: Haoming Chen
        For testing able to find the location or not
        """
        self.calculator = Calculator()
        location = self.calculator.get_location("6001")
        self.assertEquals(location, "5bea7b46-9809-4189-aafe-160208da94f7")

    def test_cost_per_minute(self):
        """
        Author: Christian Zubcic
        This tests that the cost_per_minute method calculates the cost per minute - adapting to changes in circumstances
        which affect price
        Justification for test cases explained in block comments
        """
        self.calculator = Calculator()
        # Constants for the test cases
        initial_state, final_state, capacity, charger_config = 0, 100, 100, ChargerConfig(8)
        test_time = self.calculator.time_calculation(initial_state, final_state, capacity, charger_config.power)

        # variable inputs selected are designed to test the outcome of: the entire charge occuring in off-peak and
        # on non-surchargable day, the entire charge occuring in peak times and on a surchargable day, and to test
        # when these conditions change in a charge
        off_peak_time, slightly_off_peak_time, peak_time, date_change_time = "01:00", "05:55", "12:00", "23:55"
        surcharge_date, non_surcharge_date = "2021-09-27", "2021-09-26"

        # Testing that charging in peak time is more expensive than off peak time
        self.assertTrue(self.calculator.cost_per_minute(test_time, initial_state, final_state, capacity, peak_time, non_surcharge_date, charger_config) > self.calculator.cost_per_minute(test_time, initial_state, final_state, capacity, off_peak_time, non_surcharge_date, charger_config))

        # Testing a surcharged date is more expensive than than non-surcharge date
        self.assertTrue(self.calculator.cost_per_minute(test_time, initial_state, final_state, capacity, off_peak_time, surcharge_date, charger_config) > self.calculator.cost_per_minute(test_time, initial_state, final_state, capacity, off_peak_time, non_surcharge_date, charger_config))

        # Testing peak time costs are applied as they occur (during a charge)
        self.assertTrue(self.calculator.cost_per_minute(test_time, initial_state, final_state, capacity, slightly_off_peak_time, non_surcharge_date, charger_config) > self.calculator.cost_per_minute(test_time, initial_state, final_state, capacity, off_peak_time, non_surcharge_date, charger_config))

        # Testing surcharge costs are applied as they occur - dates change during this charge (during a charge)
        self.assertTrue(self.calculator.cost_per_minute(test_time, initial_state, final_state, capacity, date_change_time, non_surcharge_date, charger_config) > self.calculator.cost_per_minute(test_time, initial_state, final_state, capacity, off_peak_time, non_surcharge_date, charger_config))

        # Random test cases with assertEquals
        initial_state, final_state, capacity, clock_time, date, charger_config = 20, 80, 82, "8:00", "2021-09-27", ChargerConfig(8)
        self.assertEqual("{:.2f}".format(self.calculator.cost_per_minute(self.calculator.time_calculation(initial_state, final_state, capacity, charger_config.power), initial_state, final_state, capacity, clock_time, date, charger_config)), str(27.06))

        initial_state, final_state, capacity, clock_time, date, charger_config = 0, 100, 100, "12:00", "2021-09-14", ChargerConfig(1)
        self.assertEqual("{:.2f}".format(self.calculator.cost_per_minute(self.calculator.time_calculation(initial_state, final_state, capacity, charger_config.power), initial_state, final_state, capacity, clock_time, date, charger_config)), str(4.18))

        initial_state, final_state, capacity, clock_time, date, charger_config = 50, 100, 10, "8:00", "2021-01-01", ChargerConfig(4)
        self.assertEqual("{:.2f}".format(self.calculator.cost_per_minute(self.calculator.time_calculation(initial_state, final_state, capacity, charger_config.power), initial_state, final_state, capacity, clock_time, date, charger_config)), str(0.69))

    def test_cost_per_minute_solar(self):
        """
                Author: Haoming Chen
                For testing c/m in solar
                """
        self.calculator = Calculator()
        test_inputs = ('5bea7b46-9809-4189-aafe-160208da94f7', "2020-12-25")
        expected_outputs = [0, 0]
        cost=self.calculator.cost_per_minute_solar(60, 80, 100, 36, "8:00", "2020-12-25", ChargerConfig(3), '5bea7b46-9809-4189-aafe-160208da94f7')
        self.assertAlmostEquals(cost, 0.127363)

    def test_date_reference(self):
        """
                        Author: Haoming Chen
                        For testing date reference
                        """
        self.calculator = Calculator()
        test_inputs = ["2022-02-22", "2024-02-29"]
        expected_outputs = [['2021-02-22', '2020-02-22', '2019-02-22'],['2021-02-28', '2020-02-29', '2019-02-28']]
        for i in range(len(test_inputs)):
            location = self.calculator.date_reference(test_inputs[i])
            self.assertEquals(location, expected_outputs[i])

    def test_get_day_light_time(self):
        """
                        Author: Haoming Chen
                        For testing sunrise and down
                        """
        self.calculator = Calculator()
        sunrise, sunset = self.calculator.get_day_light_time("5bea7b46-9809-4189-aafe-160208da94f7", '2020-12-25')
        self.assertTupleEqual(sunrise, (5.0, 10.0, 0.0))
        self.assertTupleEqual(sunset, (19.0, 24.0, 0.0))

    def test_cost_per_minute_solar_extended(self):
        """
                                Author: Haoming Chen
                                For testing solar extended situation
                                """
        self.calculator = Calculator()
        #location = self.calculator.get_location("7250")
        test_inputs = ('22d72902-b72f-4ca0-a522-4dbfb77a7b78', "2022-02-22")
        expected_outputs = []
        time = float(self.calculator.time_calculation(80, 100, 27, ChargerConfig(3).power))
        self.assertEqual(time, 45)
        cost = self.calculator.cost_per_minute_solar_extended(time, 80, 100, 27, "17:30", "2022-02-22", ChargerConfig(3), '5998b29a-8e3d-4c1e-857c-b5dce80eea6d')
        self.assertAlmostEquals(cost, 0.22579179619444564)







    # you may create test suite if needed
    if __name__ == "__main__":
        unittest.main()
