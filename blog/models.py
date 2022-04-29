from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from PIL import Image


class Ticket(models.Model):
    title = models.CharField(max_length=128, verbose_name="titre")
    description = models.TextField(
        max_length=2048, blank=True, verbose_name="description"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, verbose_name="image")
    time_created = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)

    IMAGE_MAX_SIZE = (500, 500)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()

    def reopen(self):
        self.closed = False


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="note"
    )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128, verbose_name="titre")
    body = models.TextField(max_length=8192, blank=True, verbose_name="description")
    time_created = models.DateTimeField(auto_now_add=True)
