from django.db import models


class Flow(models.Model):
    """
    This model stores the raw data from the D0010 file.
    mpan = meter point administration number
    meter = meter serial number
    reading = a decimal value that records the cumulative electricity comsumption at a point in time
    filename = the name of the file that the data was imported from
    """
    mpan = models.CharField(max_length=100)
    meter = models.CharField(max_length=100)
    reading = models.DecimalField(max_digits=10, decimal_places=3)
    filename = models.CharField(max_length=100)