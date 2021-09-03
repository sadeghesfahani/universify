from datetime import timedelta
from django.db import models
from django.utils.datetime_safe import date
from account.models import Faculty, User
from university_controller import settings


class Book(models.Model):
    name = models.CharField(max_length=60)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    picture = models.ImageField(null=True, blank=True)
    author = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def reminded(self):
        return self.quantity - Lend.objects.filter(book=self).count()


class Lend(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField()
    renewal = models.SmallIntegerField(default=settings.MAX_RENEWAL)

    def save(self, *args, **kwargs):
        self.end_date = date.today() + timedelta(days=settings.TIME_TO_LENT)
        super(Lend, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.name} - {self.user.last_name}"