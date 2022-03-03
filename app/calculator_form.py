from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField
from wtforms.validators import DataRequired, ValidationError


# validation for form inputs
class Calculator_Form(FlaskForm):
    # this variable name needs to match with the input attribute name in the html file
    # you are NOT ALLOWED to change the field type, however, you can add more built-in validators and custom messages
    BatteryPackCapacity = StringField("Battery Pack Capacity", [DataRequired()])
    InitialCharge = StringField("Initial Charge", [DataRequired()])
    FinalCharge = StringField("Final Charge", [DataRequired()])
    StartDate = DateField("Start Date", [DataRequired("Data is missing or format is incorrect")], format='%d/%m/%Y')
    StartTime = TimeField("Start Time", [DataRequired("Data is missing or format is incorrect")], format='%H:%M')
    ChargerConfiguration = StringField("Charger Configuration", [DataRequired()])
    PostCode = StringField("Post Code", [DataRequired()])

    # use validate_ + field_name to activate the flask-wtforms built-in validator
    # this is an example for you
    def validate_BatteryPackCapacity(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValidationError("cannot fetch data")

        if float(field.data) <= 0:
            raise ValueError('Battery pack capacity is invalid (capacity must be a positive value)')

    # validate initial charge here
    def validate_InitialCharge(self, field):
        if field.data is None or field.data == '':
            raise ValidationError('Field data is empty')

        # another example of how to compare initial charge with final charge
        # you may modify this part of the code
        if float(field.data) >= float(self.FinalCharge.data):
            raise ValueError("Initial charge data must be less than final charge")

        if float(field.data) < 0 or float(field.data) > 100:
            raise ValueError("Initial charge must be within a valid range")

    # validate final charge here
    def validate_FinalCharge(self, field):
        if field.data is None or field.data == '':
            raise ValidationError('Field data is empty')

        if float(field.data) <= float(self.InitialCharge.data):
            raise ValueError("Initial charge data must be less than final charge")

        if float(field.data) < 0 or float(field.data) > 100:
            raise ValueError("Final charge must be within a valid range")

    def validate_StartDate(self, field):
        if field.data is None or field.data == '':
            raise ValidationError('Field data is empty')

    # validate start time here
    def validate_StartTime(self, field):
        if field.data is None or field.data == '':
            raise ValidationError('Field data is empty')

        hour_time = field.data.hour
        min_time = field.data.minute

        if hour_time < 0 or hour_time >= 24:
            raise ValueError("Invalid time")

        if min_time < 0 or min_time >= 60:
            raise ValueError("Invalid time")

    # validate charger configuration here
    def validate_ChargerConfiguration(self, field):
        if field.data is None or field.data == '':
            raise ValidationError('Field data is empty')

        try:
            if float(field.data) % 1 != 0:
                raise ValueError("Configuration must be an integer")
        except ValueError:
            raise ValueError("Configuration does not exist")

        if float(field.data) < 1 or float(field.data) > 8:
            raise ValueError("Configuration does not exist")

    def validate_PostCode(self, field):
        if field.data is None or field.data == '':
            raise ValidationError('Field data is empty')

        if len(field.data) != 4 or not field.data.isdigit():
            raise ValueError('Invalid Australian Postcode')


class ChargerConfig:
    """
    Class acts as an object for the different configurations of chargers and holds all their relevant data
    """
    def __init__(self, config):
        if config == 1:
            self.voltage = 240
            self.amperage = 10
            self.power = 2
            self.basePrice = 5
        elif config == 2:
            self.voltage = 240
            self.amperage = 16
            self.power = 3.6
            self.basePrice = 5
        elif config == 3:
            self.voltage = 240
            self.amperage = 32
            self.power = 7.2
            self.basePrice = 10
        elif config == 4:
            self.voltage = 415
            self.amperage = 16
            self.power = 11
            self.basePrice = 12.5
        elif config == 5:
            self.voltage = 415
            self.amperage = 32
            self.power = 22
            self.basePrice = 15
        elif config == 6:
            self.voltage = 450
            self.amperage = 80
            self.power = 36
            self.basePrice = 20
        elif config == 7:
            self.voltage = 450
            self.amperage = 200
            self.power = 90
            self.basePrice = 30
        elif config == 8:
            self.voltage = 500
            self.amperage = 700
            self.power = 350
            self.basePrice = 50

