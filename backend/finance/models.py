from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    fullName = models.CharField(max_length=100)

    def __str__(self):
        return self.fullName


class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    icon = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class UserWallet(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_wallets"
    )
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="user_wallets"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Transactions(models.Model):
    id = models.AutoField(primary_key=True)
    userWallet = models.ForeignKey(
        UserWallet, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.DecimalField(decimal_places=1, max_digits=10)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="transactions"
    )
    type = models.CharField(max_length=10)
    description = models.TextField()
    spPerson = models.CharField(max_length=50)

    def __str__(self):
        return f"Transaction {self.id} by {self.user.fullName}"


class Payments(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    type = models.CharField(max_length=50)
    description = models.TextField()
    spPerson = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=1, max_digits=10)
    state = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.id} by {self.spPerson}"
