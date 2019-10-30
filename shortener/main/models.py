from django.db import models

class URL(models.Model):
    id = models.AutoField(primary_key=True)
    short_url = models.CharField(max_length= 10, unique=True)
    long_url = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    custom = models.BooleanField(default=False)
    # user_id field? stats + abuse

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['long_url'], condition=models.Q(custom=False), name='unique_random_url')
        ]
    def __str__(self):
        return f"{self.short_url} for {self.long_url}"

class Visit(models.Model):
    url = models.ForeignKey(URL, on_delete=models.CASCADE)
    visit_time = models.DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.user_ip} visit to {self.url}"