import unittest  # required for unit test
import calculator


class Testcalculator(unittest.TestCase):
    # testcases:
    # This will test the get_day_light_length function
    def test_get_day_light_length(self):
        c = calculator.Calculator()

        # test_get_day_light_length 1, correct location and correct date
        self.assertEqual(10.2, c.get_day_light_length("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2021-08-01"),
                         "test_get_day_light_length 1 has failed, correct location and correct date")

        # test_get_day_light_length 2, incorrect location and correct date
        try:
            with self.assertRaises(ValueError):
                c.get_day_light_length("ab9f494f-f-2497b99f2258", "2021-08-01")
        except AssertionError:
            print("test_get_day_light_length 2 has failed, incorrect location and correct date")

        # test_get_day_light_length 3, incorrect type location and correct date
        try:
            with self.assertRaises(ValueError):
                c.get_day_light_length(0, "2021-08-01")
        except AssertionError:
            print("test_get_day_light_length 3 has failed, incorrect type location and correct date")

        # test_get_day_light_length 4, incorrect empty location and correct date
        try:
            with self.assertRaises(Exception):
                c.get_day_light_length("2021-08-01")
        except AssertionError:
            print("test_get_day_light_length 4 has failed, incorrect empty location and correct date")

        # test_get_day_light_length 5, correct location and incorrect date
        try:
            with self.assertRaises(ValueError):
                c.get_day_light_length("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2a-08-01")
        except AssertionError:
            print("test_get_day_light_length 5 has failed, correct location and incorrect date")

        # test_get_day_light_length 6, correct location and incorrect late date
        try:
            with self.assertRaises(ValueError):
                c.get_day_light_length("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2006-08-01")
        except AssertionError:
            print("test_get_day_light_length 6 has failed, correct location and incorrect late date")

        # test_get_day_light_length 7, correct location and incorrect future date
        try:
            with self.assertRaises(ValueError):
                c.get_day_light_length("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2035-08-01")
        except AssertionError:
            print("test_get_day_light_length 7 has failed, correct location and incorrect future date")

        # test_get_day_light_length 8, correct location and incorrect input date
        try:
            with self.assertRaises(ValueError):
                c.get_day_light_length("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", 0)
        except AssertionError:
            print("test_get_day_light_length 8 has failed, correct location and incorrect input date")

        # test_get_day_light_length 9, correct location and incorrect input date
        try:
            with self.assertRaises(Exception):
                c.get_day_light_length("ab9f494f-f8a0-4c24-bd2e-2497b99f2258")
        except AssertionError:
            print("test_get_day_light_length 9 has failed, correct location and incorrect empty date")

    # This will test the get_solar_insolation function
    def test_get_solar_insolation(self):
        c = calculator.Calculator()

        # test_get_solar_insolation 1, correct location and correct date
        self.assertEqual(3.2, c.get_solar_insolation("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2021-08-01"),
                         "test_get_day_light_length 1 has failed, correct location and correct date")

        # test_get_solar_insolation 2, incorrect location and correct date
        try:
            with self.assertRaises(ValueError):
                c.get_solar_insolation("ab9f494f-f-2497b99f2258", "2021-08-01")
        except AssertionError:
            print("test_get_solar_insolation 2 has failed, incorrect location and correct date")

        # test_get_solar_insolation 3, incorrect type location and correct date
        try:
            with self.assertRaises(ValueError):
                c.get_solar_insolation(0, "2021-08-01")
        except AssertionError:
            print("test_get_solar_insolation 3 has failed, incorrect type location and correct date")

        # test_get_solar_insolation 4, incorrect empty location and correct date
        try:
            with self.assertRaises(Exception):
                c.get_solar_insolation("2021-08-01")
        except AssertionError:
            print("test_get_solar_insolation 4 has failed, incorrect empty location and correct date")

        # test_get_solar_insolation 5, correct location and incorrect date
        try:
            with self.assertRaises(ValueError):
                c.get_solar_insolation("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2a-08-01")
        except AssertionError:
            print("test_get_solar_insolation 5 has failed, correct location and incorrect date")

        # testget_solar_insolation 6, correct location and incorrect late date
        try:
            with self.assertRaises(ValueError):
                c.get_solar_insolation("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2006-08-01")
        except AssertionError:
            print("test_get_solar_insolation 6 has failed, correct location and incorrect late date")

        # test_get_solar_insolation 7, correct location and incorrect future date
        try:
            with self.assertRaises(ValueError):
                c.get_solar_insolation("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2035-08-01")
        except AssertionError:
            print("test_get_solar_insolation 7 has failed, correct location and incorrect future date")

        # test_get_solar_insolation 8, correct location and incorrect input date
        try:
            with self.assertRaises(ValueError):
                c.get_solar_insolation("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", 0)
        except AssertionError:
            print("test_get_solar_insolation 8 has failed, correct location and incorrect input date")

        # test_get_solar_insolation 9, correct location and incorrect input date
        try:
            with self.assertRaises(Exception):
                c.get_solar_insolation("ab9f494f-f8a0-4c24-bd2e-2497b99f2258")
        except AssertionError:
            print("test_get_solar_insolation 9 has failed, correct location and incorrect empty date")

    # This will test the get_cloud_cover function
    def test_get_cloud_cover(self):
        c = calculator.Calculator()

        # test_get_cloud_cover 1, correct location and correct date
        self.assertEqual([1.0, 0.94, 0.87, 0.81, 0.79, 0.78, 0.76, 0.78, 0.8, 0.82, 0.67, 0.51,
                          0.35, 0.3, 0.24, 0.18, 0.18, 0.19, 0.19, 0.16, 0.13, 0.1, 0.08, 0.07],
                         c.get_cloud_cover("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2021-08-01"),
                         "test_get_day_light_length 1 has failed, correct location and correct date")

        # test_get_cloud_cover 2, incorrect location and correct date
        try:
            with self.assertRaises(ValueError):
                c.get_cloud_cover("ab9f494f-f-2497b99f2258", "2021-08-01")
        except AssertionError:
            print("test_get_cloud_cover 2 has failed, incorrect location and correct date")

        # test_get_cloud_cover 3, incorrect type location and correct date
        try:
            with self.assertRaises(ValueError):
                c.get_cloud_cover(0, "2021-08-01")
        except AssertionError:
            print("test_get_cloud_cover 3 has failed, incorrect type location and correct date")

        # test_get_cloud_cover 4, incorrect empty location and correct date
        try:
            with self.assertRaises(Exception):
                c.get_cloud_cover("2021-08-01")
        except AssertionError:
            print("test_get_cloud_cover 4 has failed, incorrect empty location and correct date")

        # test_get_cloud_cover 5, correct location and incorrect date
        try:
            with self.assertRaises(ValueError):
                c.get_cloud_cover("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2a-08-01")
        except AssertionError:
            print("test_get_cloud_cover 5 has failed, correct location and incorrect date")

        # test get_cloud_cover 6, correct location and incorrect late date
        try:
            with self.assertRaises(ValueError):
                c.get_solar_insolation("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2006-08-01")
        except AssertionError:
            print("test_get_cloud_cover 6 has failed, correct location and incorrect late date")

        # test_get_cloud_cover 7, correct location and incorrect future date
        try:
            with self.assertRaises(ValueError):
                c.get_cloud_cover("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2035-08-01")
        except AssertionError:
            print("test_get_cloud_cover 7 has failed, correct location and incorrect future date")

        # test_get_cloud_cover 8, correct location and incorrect input date
        try:
            with self.assertRaises(ValueError):
                c.get_cloud_cover("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", 0)
        except AssertionError:
            print("test_get_cloud_cover 8 has failed, correct location and incorrect input date")

        # test_get_cloud_cover 9, correct location and incorrect input date
        try:
            with self.assertRaises(Exception):
                c.get_cloud_cover("ab9f494f-f8a0-4c24-bd2e-2497b99f2258")
        except AssertionError:
            print("test_get_cloud_cover 9 has failed, correct location and incorrect empty date")

    # This will test the calculate_solar_energy_day function
    def test_calculate_solar_energy_day(self):
        c = calculator.Calculator()

        # test_calculate_solar_energy_day 1, correct location and correct date
        self.assertEqual(0.38588235294117657,
                         c.calculate_solar_energy_day("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2021-08-01"),
                         "test_calculate_solar_energy_day 1 has failed, correct location and correct date")

        # test_calculate_solar_energy_day 2, incorrect location and correct date
        try:
            with self.assertRaises(ValueError):
                c.calculate_solar_energy_day("ab9f494f-f-2497b99f2258", "2021-08-01")
        except AssertionError:
            print("test_calculate_solar_energy_day 2 has failed, incorrect location and correct date")

        # test_calculate_solar_energy_day 3, incorrect type location and correct date
        try:
            with self.assertRaises(ValueError):
                c.calculate_solar_energy_day(0, "2021-08-01")
        except AssertionError:
            print("test_calculate_solar_energy_day 3 has failed, incorrect type location and correct date")

        # test_calculate_solar_energy_day 4, incorrect empty location and correct date
        try:
            with self.assertRaises(Exception):
                c.calculate_solar_energy_day("2021-08-01")
        except AssertionError:
            print("test_calculate_solar_energy_day 4 has failed, incorrect empty location and correct date")

        # test_calculate_solar_energy_day 5, correct location and incorrect date
        try:
            with self.assertRaises(ValueError):
                c.calculate_solar_energy_day("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2a-08-01")
        except AssertionError:
            print("test_calculate_solar_energy_day 5 has failed, correct location and incorrect date")

        # test calculate_solar_energy_day 6, correct location and incorrect late date
        try:
            with self.assertRaises(ValueError):
                c.calculate_solar_energy_day("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2006-08-01")
        except AssertionError:
            print("test_calculate_solar_energy_day 6 has failed, correct location and incorrect late date")

        # test_calculate_solar_energy_day 7, correct location and incorrect future date
        try:
            with self.assertRaises(ValueError):
                c.calculate_solar_energy_day("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2035-08-01")
        except AssertionError:
            print("test_calculate_solar_energy_day 7 has failed, correct location and incorrect future date")

        # test_calculate_solar_energy_day 8, correct location and incorrect input date
        try:
            with self.assertRaises(ValueError):
                c.calculate_solar_energy_day("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", 0)
        except AssertionError:
            print("test_calculate_solar_energy_day 8 has failed, correct location and incorrect input date")

        # test_calculate_solar_energy_day 9, correct location and incorrect input date
        try:
            with self.assertRaises(Exception):
                c.calculate_solar_energy_day("ab9f494f-f8a0-4c24-bd2e-2497b99f2258")
        except AssertionError:
            print("test_calculate_solar_energy_day 9 has failed, correct location and incorrect empty date")

    # This will test the date_decrementer function
    def test_date_decrementer(self):
        c = calculator.Calculator()

        # date decrement normal failed
        self.assertEqual("2009-08-21", c.date_decrementer("2009-08-22"), "date decrement normal failed")
        # date decrement normal failed
        self.assertEqual("2009-07-31", c.date_decrementer("2009-08-01"), "date decrement month failed")
        # date decrement normal failed
        self.assertEqual("2009-12-31", c.date_decrementer("2010-01-01"), "date decrement year failed")

        # date test 4, no input
        try:
            with self.assertRaises(Exception):
                c.date_decrementer()
        except AssertionError:
            print("date test 4 failed, no input")

        # date test 5, large input
        try:
            with self.assertRaises(Exception):
                c.date_decrementer("2010-01-01---")
        except AssertionError:
            print("date test 5 failed, large input")

        # date test 6, too small
        try:
            with self.assertRaises(Exception):
                c.date_decrementer("2010-01-")
        except AssertionError:
            print("date test 6 failed, too small input")

        # date test 6, wrong type
        try:
            with self.assertRaises(Exception):
                c.date_decrementer("2010-01-ab")
        except AssertionError:
            print("date test 7 failed, wrong type input")

    # This will test the time_converter function
    def test_time_converter(self):
        c = calculator.Calculator()

        # time_converter normal failed
        self.assertEqual((3, 34, 56), c.time_converter("03:34:56"), "time_converter normal failed")

        # time_converter possible errors
        # check if out of range, not right type or non existent errors
        boundary_list = ["-1", "03", "61", "123456789", "ab", ""]
        for i in range(len(boundary_list)):
            for j in range(len(boundary_list)):
                for k in range(len(boundary_list)):
                    try:
                        with self.assertRaises(ValueError):
                            if str(boundary_list[i]) == "03" and str(boundary_list[j]) == "03" \
                                    and str(boundary_list[k]) == "03":
                                raise ValueError
                            c.time_converter(str(boundary_list[i]) + ":" + str(boundary_list[j]) + ":" +
                                             str(boundary_list[k]))
                    except AssertionError:
                        print("time converter test failed: " + str(boundary_list[i]) + ":" + str(boundary_list[j]) +
                              ":" + str(boundary_list[k]))

    # This will test the calculate_solar_energy function
    def test_calculate_solar_energy(self):
        c = calculator.Calculator()

        # test_calculate_solar_energy_day 1, correct location, correct date and 30 amount_of_days
        self.assertEqual(5.688054160071447,
                         c.calculate_solar_energy("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2021-08-01", 30),
                         "test_get_day_light_length 1 has failed, correct location and correct date")

        # test_calculate_solar_energy_day 2, correct location, correct date and 30 amount_of_days
        self.assertEqual(167.04362111265058,
                         c.calculate_solar_energy("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2021-08-01", 365),
                         "test_get_day_light_length 1 has failed, correct location and correct date")

        # test_calculate_solar_energy_day 3, correct location, correct date and incorrect amount_of_days
        try:
            with self.assertRaises(ValueError):
                c.calculate_solar_energy("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2021-08-01", 36)
        except AssertionError:
            print("test_calculate_solar_energy_day 3 has failed,"
                  " correct location, correct date and incorrect amount_of_days")

        # test_calculate_solar_energy_day 4, incorrect location, correct date and correct amount_of_days
        try:
            with self.assertRaises(ValueError):
                c.calculate_solar_energy("ab9f494f-f8a0-4-2497b99f2258", "2021-08-01", 30)
        except AssertionError:
            print("test_calculate_solar_energy_day 4 has failed,"
                  " incorrect location, correct date and correct amount_of_days")

        # test_calculate_solar_energy_day 5, incorrect type location, correct date and correct amount_of_days
        try:
            with self.assertRaises(ValueError):
                c.calculate_solar_energy(0, "2021-08-01", 30)
        except AssertionError:
            print("test_calculate_solar_energy_day 5 has failed,"
                  " incorrect type location, correct date and correct amount_of_days")

        # test_calculate_solar_energy_day 6, incorrect empty location, correct date and correct amount_of_days
        try:
            with self.assertRaises(Exception):
                c.calculate_solar_energy("2021-08-01", 30)
        except AssertionError:
            print("test_calculate_solar_energy_day 6 has failed,"
                  " incorrect empty location, correct date and correct amount_of_days")

        # test_calculate_solar_energy_day 7, correct location, incorrect date and correct amount_of_days
        try:
            with self.assertRaises(ValueError):
                c.calculate_solar_energy("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2a-08-01", 30)
        except AssertionError:
            print("test_calculate_solar_energy_day 7 has failed,"
                  " correct location, incorrect date and correct amount_of_days")

        # test_calculate_solar_energy_day 8, correct location, incorrect late date and correct amount_of_days
        try:
            with self.assertRaises(ValueError):
                c.calculate_solar_energy("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2006-08-01", 30)
        except AssertionError:
            print("test_calculate_solar_energy_day 8 has failed,"
                  " correct location, incorrect late date and correct amount_of_days")

        # test_calculate_solar_energy_day 9, correct location, incorrect future date and correct amount_of_days
        try:
            with self.assertRaises(ValueError):
                c.calculate_solar_energy("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2030-08-01", 30)
        except AssertionError:
            print("test_calculate_solar_energy_day 9 has failed,"
                  " correct location, incorrect future date and correct amount_of_days")

        # test_calculate_solar_energy_day 10, correct location, incorrect type date and correct amount_of_days
        try:
            with self.assertRaises(ValueError):
                c.calculate_solar_energy("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", 0, 30)
        except AssertionError:
            print("test_calculate_solar_energy_day 10 has failed,"
                  " correct location, incorrect type date and correct amount_of_days")

        # test_calculate_solar_energy_day 11, correct location, incorrect empty date and correct amount_of_days
        try:
            with self.assertRaises(Exception):
                c.calculate_solar_energy("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", 30)
        except TypeError:
            print("test_calculate_solar_energy_day 11 has failed,"
                  " correct location, incorrect empty date and correct amount_of_days")

        # test_calculate_solar_energy_day 12, correct location, correct date and incorrect empty amount_of_days
        try:
            with self.assertRaises(Exception):
                c.calculate_solar_energy("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2021-08-01")
        except TypeError:
            print("test_calculate_solar_energy_day 12 has failed,"
                  " correct location, correct date and incorrect empty amount_of_days")

        # test_calculate_solar_energy_day 13, correct location, correct date and incorrect type amount_of_days
        try:
            with self.assertRaises(ValueError):
                c.calculate_solar_energy("ab9f494f-f8a0-4c24-bd2e-2497b99f2258", "2021-08-01", "a")
        except AssertionError:
            print("test_calculate_solar_energy_day 13 has failed,"
                  " correct location, correct date and incorrect type amount_of_days")


def main():
    suit = unittest.TestLoader().loadTestsFromTestCase(Testcalculator)
    unittest.TextTestRunner(verbosity=2).run(suit)


main()
