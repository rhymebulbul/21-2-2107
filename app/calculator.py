import csv
import os
from datetime import datetime, timedelta
import calendar
import requests

class Calculator():
    # you can choose to initialise variables here, if needed.
    def __init__(self):
        self.national_holiday = []
        pwd = os.getcwd()
        with open("national_holidays.csv") as file:
            for row in file:
                self.national_holiday.append(row.split(",")[0])

        self.national_holiday.pop(0)  # removes header column

    # you may add more parameters if needed, you may also modify the formula.
    # Calculates how long it takes to charge the car in minutes
    def time_calculation(self, initial_state, final_state, capacity, power):
        time_hours = (((final_state - initial_state) / 100) * capacity) / power
        time_mins = time_hours * 60
        return time_mins

    # Calculates the cost to charge per minute - so surcharges are added if applicable mid-way through a charge
    def cost_per_minute(self, time, initial_state, final_state, capacity, clock_time, date, charger_config):
        charge_per_min = ((final_state - initial_state) / 100 * capacity) / time
        cost = 0

        for i in range(int(time)):
            clock_time, date = self.time_incrementer(clock_time, date)
            cost += self.cost_per_min_aux(charge_per_min, clock_time, date, charger_config)

        # adds to the cost the fraction of the final minute
        clock_time, date = self.time_incrementer(clock_time, date)
        cost += self.cost_per_min_aux(charge_per_min * (time - int(time)), clock_time, date, charger_config)

        return cost

    def time_percent(self, sunrise, sunset):
        return [int(sunrise[0]), ((60 - sunrise[1]) * 60 + (60 - sunrise[2])) / 3600], \
               [int(sunset[0]), (sunset[1] * 60 + sunset[2]) / 3600]

    def calculate_solar_energy_day_list(self, location, date, consider_cloud=False):
        solar_energy = [0] * 24
        sunrise, sunset = self.get_day_light_time(location, date)
        sunrise, sunset = self.time_percent(sunrise, sunset)
        si = self.get_solar_insolation(location, date)
        dl = self.get_day_light_length(location, date)
        if consider_cloud:
            cc = self.get_cloud_cover(location, date)
            if not len(cc) == 24:
                raise ValueError(cc, "len(cc) should be 24")
            for i in range(sunrise[0], sunset[0] + 1):
                solar_energy[i] += si * (1 / dl) * (1 - cc[i]) * 50 * 0.2
        else:
            for i in range(sunrise[0], sunset[0] + 1):
                solar_energy[i] += si * (1 / dl) * 1 * 50 * 0.2
        solar_energy[sunrise[0]] *= sunrise[1]
        solar_energy[sunset[0]] *= sunset[1]
        return solar_energy

    def date_reference(self, date):
        if len(date) > 10:
            raise ValueError("inputs were too large")
        date = datetime.strptime(date, '%Y-%m-%d')
        current_date = datetime.now()
        if date <= current_date:
            raise ValueError("input date is not in future")
        reference_dates = []
        month = date.month
        year = current_date.year if \
            date.month < current_date.month or (date.month == current_date.month and date.day <= current_date.day) \
            else current_date.year - 1
        for i in range(3):
            day = min(calendar.monthrange(year - i, month)[1], date.day)
            reference_dates.append(datetime(year - i, month, day).strftime('%Y-%m-%d'))
        return reference_dates

    def calculate_solar_energy_day_list_extended(self, location, date):
        reference_dates = self.date_reference(date)
        solar_energys = []
        for reference_date in reference_dates:
            reference_solar_energy = self.calculate_solar_energy_day_list(location, reference_date, True)
            solar_energys.append(reference_solar_energy)
        return solar_energys

    # Calculates the cost to charge minus solar energy generation per minute
    def cost_per_minute_solar(self, time, initial_state, final_state, capacity, clock_time, date, charger_config,
                              location, consider_cloud=False):
        input_date = datetime.strptime(date, '%Y-%m-%d')
        if input_date < datetime(2008, 7, 1) or input_date > datetime.now() + timedelta(days=-2):
            raise ValueError(
                "Date must be specified, formatted in YYYY-MM-DD and be between 2008-07-01 and 2 days before")
        charge_per_min = ((final_state - initial_state) / 100 * capacity) / time
        cost = 0
        solar_energy_list = [date, self.calculate_solar_energy_day_list(location, date, consider_cloud)]
        for i in range(int(time)):
            if solar_energy_list[0] != date:
                solar_energy_list = [date, self.calculate_solar_energy_day_list(location, date, consider_cloud)]
            clock_time_hour = int(clock_time.split(":")[0])
            cost += self.cost_per_min_aux(charge_per_min - solar_energy_list[1][clock_time_hour] / 60, clock_time, date,
                                          charger_config)
            clock_time, date = self.time_incrementer(clock_time, date)
        # adds to the cost the fraction of the final minute
        if solar_energy_list[0] != date:
            solar_energy_list = [date, self.calculate_solar_energy_day_list(location, date, consider_cloud)]
        cost += self.cost_per_min_aux(
            (charge_per_min - solar_energy_list[1][clock_time_hour] / 60) * (time - int(time)), clock_time, date,
            charger_config)
        return max(cost, 0)

    # Calculates the cost to charge minus solar energy generation per minute
    def cost_per_minute_solar_extended(self, time, initial_state, final_state, capacity, clock_time, date,
                                       charger_config, location):
        input_date = datetime.strptime(date, '%Y-%m-%d')
        if input_date <= datetime.now() + timedelta(days=-2):
            return self.cost_per_minute_solar(time, initial_state, final_state, capacity, clock_time, date,
                                              charger_config, location)
        charge_per_min = ((final_state - initial_state) / 100 * capacity) / time
        cost = 0
        solar_energy_list = [date, self.calculate_solar_energy_day_list_extended(location, date)]
        for i in range(int(time)):
            if solar_energy_list[0] != date:
                solar_energy_list = [date, self.calculate_solar_energy_day_list_extended(location, date)]
            clock_time_hour = int(clock_time.split(":")[0])
            for solar_energy in solar_energy_list[1]:
                cost += self.cost_per_min_aux(charge_per_min - solar_energy[clock_time_hour] / 60, clock_time, date,
                                              charger_config)
            clock_time, date = self.time_incrementer(clock_time, date)

        # adds to the cost the fraction of the final minute
        if solar_energy_list[0] != date:
            solar_energy_list = [date, self.calculate_solar_energy_day_list_extended(location, date)]
        clock_time_hour = int(clock_time.split(":")[0])
        for solar_energy in solar_energy_list[1]:
            cost += self.cost_per_min_aux((charge_per_min - solar_energy[clock_time_hour] / 60) * (time - int(time)),
                                          clock_time, date, charger_config)
        cost /= 3
        return max(cost, 0)

    # Computes the cost for each minute
    def cost_per_min_aux(self, charge_per_min, clock_time, date, charger_config):
        if self.is_peak(clock_time):
            peak_factor = 100
        else:
            peak_factor = 200

        if self.is_surcharge(date):
            surcharge_factor = 1.1
        else:
            surcharge_factor = 1

        cost = charge_per_min * (charger_config.basePrice / peak_factor) * surcharge_factor
        return cost

    # Increments time by one minute and returns new clock time
    def time_incrementer(self, time, date):
        time = time.split(":")
        new_date = date

        if int(time[1]) == 59:
            time[0] = int(time[0]) + 1
            time[1] = 0
        else:
            time[1] = int(time[1]) + 1

        if int(time[0]) == 24:
            time[0] = int(time[0]) - 24
            new_date = self.date_incrementer(date)

        new_time = str(time[0]).zfill(2) + ":" + str(time[1]).zfill(2)

        return new_time, new_date

    # Increments the date if charge occurs overnight
    def date_incrementer(self, date):
        new_date = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        return new_date

    # you may create some new methods at your convenience, or modify these methods, or choose not to use them.
    def is_surcharge(self, start_date):
        date = start_date.split("-")
        year = date[0]
        month = date[1].zfill(2)
        day = date[2].zfill(2)
        input_string = year + month + day

        date = datetime(int(year), int(month), int(day))
        weekday = date.weekday()

        # Added surcharge for weekdays
        if 0 <= weekday <= 4:
            return True

        if input_string in self.national_holiday:
            return True
        elif int(input_string[0:3]) > 2022:
            if "2022" + month + day in self.national_holiday:
                return True
            else:
                return False
        elif int(input_string[0:3]) < 2014:
            if "2014" + month + day in self.national_holiday:
                return True
            else:
                return False
        else:
            return False

    # Returns True if charging time is during peak hours, False otherwise (off-peak)
    def is_peak(self, time):
        hour_time = int(time.split(":")[0])

        if 6 <= hour_time < 18:
            return True
        else:
            return False

    def get_location(self, postcode):
        response = requests.get(
            "http://118.138.246.158/api/v1/location?postcode=" + str(postcode))
        if response.status_code != 200:
            raise ValueError(response.json()["message"] + "[within get_location inputs: postcode - "
                             + str(postcode) + "]")
        return response.json()[0]['id']

    # to be acquired through API
    def get_day_light_time(self, location, date):
        response = requests.get(
            "http://118.138.246.158/api/v1/weather?location=" + str(location) + "&date=" + str(date))
        if len(response.json()) < 14:
            raise ValueError(response.json()["message"] + "[within get_day_light_length inputs: location - " +
                             str(location) + " date - " + str(date) + "]")
        sunrise = response.json()["sunrise"]
        sunset = response.json()["sunset"]
        return self.time_converter(sunrise), self.time_converter(sunset)

    def get_day_light_length(self, location, date):
        response = requests.get(
            "http://118.138.246.158/api/v1/weather?location=" + str(location) + "&date=" + str(date))
        if len(response.json()) < 14:
            raise ValueError(response.json()["message"] + "[within get_day_light_length inputs: location - " +
                             str(location) + " date - " + str(date) + "]")
        sunrise = response.json()["sunrise"]
        sunset = response.json()["sunset"]
        hours1, minutes1, seconds1 = self.time_converter(sunrise)
        hours2, minutes2, seconds2 = self.time_converter(sunset)
        hour = hours2 - hours1
        minute = minutes2 - minutes1
        second = seconds2 - seconds1
        total_time = hour + (minute / 60) + (second / 3600)
        return total_time

    # to be acquired through API
    def get_solar_insolation(self, location, date):
        response = requests.get(
            "http://118.138.246.158/api/v1/weather?location=" + str(location) + "&date=" + str(date))
        if len(response.json()) < 14:
            raise ValueError(response.json()["message"] + "[within get_solar_insolation inputs: location - " +
                             str(location) + " date - " + str(date) + "]")
        return float(response.json()["sunHours"])

    # to be acquired through API
    def get_cloud_cover(self, location, date):
        response = requests.get(
            "http://118.138.246.158/api/v1/weather?location=" + str(location) + "&date=" + str(date))
        if len(response.json()) < 14:
            raise ValueError(response.json()["message"] + "[within get_cloud_cover inputs: location - " + str(location)
                             + " date - " + str(date) + "]")
        cloudCoverPctList = []
        for i in range(24):
            cloudCoverPctList.append(float(response.json()["hourlyWeatherHistory"][i]["cloudCoverPct"] / 100))
        return cloudCoverPctList

    def calculate_solar_energy_day(self, location, date):
        cc = self.get_cloud_cover(location, date)
        si = self.get_solar_insolation(location, date)
        dl = self.get_day_light_length(location, date)
        solar_energy_sum = 0
        if len(cc) == 24:
            for i in range(len(cc)):
                solar_energy_sum += si * (1 / dl) * (1 - cc[i]) * 50 * 0.2
        return solar_energy_sum

    def date_decrementer(self, date):
        if len(date) > 10:
            raise ValueError("inputs were too large")
        new_date = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=-1)).strftime('%Y-%m-%d')
        return new_date

    def calculate_solar_energy(self, location, date, amount_of_days):
        response = requests.get(
            "http://118.138.246.158/api/v1/weather?location=" + str(location) + "&date=" + str(date))
        if len(response.json()) < 14:
            raise ValueError(response.json()["message"] + "[within calculate_solar_energy inputs: location - "
                             + str(location)
                             + " date - " + str(date) + "]")
        if amount_of_days != 30 and amount_of_days != 365:
            raise ValueError("the amount of days should be a positive integer[within calculate_solar_energy inputs]")
        solar_energy_sum_days = 0
        for i in range(amount_of_days):
            solar_energy_sum_days += self.calculate_solar_energy_day(location, date)
            date = self.date_decrementer(date)
        return solar_energy_sum_days

    def time_converter(self, time):
        if len(time) > 8:
            raise ValueError("inputs were too large")
        hours = float(time[0:2])
        minutes = float(time[3:5])
        seconds = float(time[6:8])
        if seconds > 60 or seconds < 0 or minutes > 60 or minutes < 0 or hours > 24 or hours < 0:
            raise ValueError("time input was wrong")
        return hours, minutes, seconds

