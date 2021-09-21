from django.db import models


# Create your models here.

def upload_to(instance, filename):
    return filename


class News(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200)
    full_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_to)

    def __str__(self):
        return self.title


class ImageNews(models.Model):
    image = models.ImageField(upload_to=upload_to)
    news = models.ForeignKey(News, on_delete=models.CASCADE)


class Legislation(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200)
    full_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class LegislationPDF(models.Model):
    legislation = models.ForeignKey(Legislation, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='pdf')

