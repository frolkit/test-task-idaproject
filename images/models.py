from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Image(models.Model):
    width = models.IntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(limit_value=0),
                    MaxValueValidator(limit_value=7680)],
        verbose_name='Ширина')
    height = models.IntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(limit_value=0),
                    MaxValueValidator(limit_value=4320)],
        verbose_name='Высота')
    image = models.ImageField(upload_to='', verbose_name='Файл изображения')
