from django.db import models

class Scan(models.Model):

    url = models.URLField()

    status_code = models.IntegerField()

    score = models.IntegerField()

    https = models.CharField(max_length=10)

    ssl = models.CharField(max_length=20)

    technology = models.CharField(max_length=100)

    response_time = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url