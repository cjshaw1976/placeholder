from django.db import models

import datetime

""" Callable current hour """
def currentHour():
    return datetime.datetime.utcnow().replace(minute=0, second=0, microsecond=0)

""" Cities for geographic location """
class GeoCities(models.Model):
    geoname_id = models.IntegerField(default=0, unique=True)
    locale_code = models.CharField(blank=True, null=True, max_length=8)
    continent_code = models.CharField(blank=True, null=True, max_length=8)
    continent_name = models.CharField(blank=True, null=True, max_length=16)
    country_iso_code = models.CharField(blank=True, null=True, max_length=8)
    country_name = models.CharField(blank=True, null=True, max_length=64)
    subdivision_1_iso_code = models.CharField(blank=True, null=True, max_length=8)
    subdivision_1_name = models.CharField(blank=True, null=True, max_length=128)
    subdivision_2_iso_code = models.CharField(blank=True, null=True, max_length=8)
    subdivision_2_name = models.CharField(blank=True, null=True, max_length=128)
    city_name = models.CharField(blank=True, null=True, max_length=64)
    metro_code = models.CharField(blank=True, null=True, max_length=32)
    time_zone = models.CharField(blank=True, null=True, max_length=32)
    is_in_european_union = models.SmallIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['continent_name', 'country_name',]),
            models.Index(fields=['country_name', 'city_name',]),
            models.Index(fields=['city_name',]),
        ]

    def __str__(self):
        if self.city_name:
            return ({}, {}).format(self.city_name, self.country_name)
        else:
            return self.country_name


class GeoIP(models.Model):
    network = models.CharField(max_length=64)
    start_ip = models.CharField(max_length=16)
    end_ip = models.CharField(max_length=16)
    geoname_id = models.ForeignKey(GeoCities, to_field='geoname_id', on_delete=models.CASCADE)
    registered_country_geoname_id = models.IntegerField(blank=True, null=True)
    represented_country_geoname_id = models.IntegerField(blank=True, null=True)
    is_anonymous_proxy = models.SmallIntegerField(default=0)
    is_satellite_provider = models.SmallIntegerField(default=0)
    postal_code = models.CharField(blank=True, null=True, max_length=16)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    accuracy_radius = models.IntegerField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['network',]),
            models.Index(fields=['latitude', 'longitude',]),
        ]


""" Log clients location per hour per geocity """
class LocationLog(models.Model):
    count = models.IntegerField(default=1)
    hour = models.DateTimeField("Hour", default=currentHour())
    location = models.ForeignKey(GeoCities, to_field='geoname_id',
                                 on_delete=models.CASCADE, blank = True,
                                 null=True, default=None)

    class Meta:
        indexes = [
            models.Index(fields=['hour', 'location']),
        ]
        unique_together = (("hour", "location"),)

""" Log clients per 10 minutes """
class VisitorLog(models.Model):
    count = models.IntegerField(default=0)
    remote = models.CharField("REMOTE_ADDR", max_length=16)
    agent = models.TextField("HTTP_USER_AGENT", default="")
    location = models.ForeignKey(GeoCities, to_field='geoname_id',
                                 on_delete=models.CASCADE, blank = True,
                                 null=True, default=None)
    date_added = models.DateTimeField("Created", auto_now_add=True)


""" Log hit of uri from of URI from referer per hour """
class DataLog(models.Model):
    count = models.IntegerField(default=0)
    hour = models.DateTimeField("Hour", default=currentHour())
    referer = models.CharField("HTTP_REFERER", max_length=128)
    uri = models.CharField("REQUEST_URI", max_length=128)

    class Meta:
        indexes = [
            models.Index(fields=['hour',]),
            models.Index(fields=['referer',]),
            models.Index(fields=['uri',]),
        ]
        unique_together = (("hour", "referer", "uri"),)
