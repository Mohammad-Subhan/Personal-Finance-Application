from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    pass


class WalletAccount(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    icon = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class TansactionCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WalletTransactions(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_account = models.ForeignKey(WalletAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(TansactionCategory, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.description
