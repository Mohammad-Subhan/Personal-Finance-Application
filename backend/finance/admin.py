from django.contrib import admin
from .models import User, UserWallet, Wallet, Category, Transaction, Payment

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display =["id", "username", "fullName"]

class WalletAdmin(admin.ModelAdmin):
    list_display=["id", "name", "icon"]

class UserWalletAdmin(admin.ModelAdmin):
    list_display=["id", "user", "wallet", "name"]

class CategoryAdmin(admin.ModelAdmin):
    list_display=["id", "name"]

class TransactionsAdmin(admin.ModelAdmin):
    list_display=["id", "userWallet", "amount", "category", "type", "spPerson"]

class PaymentsAdmin(admin.ModelAdmin):
    list_display=["id", "user", "type", "spPerson", "amount", "state"]


# Register the models
admin.site.register(User, UserAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(UserWallet, UserWalletAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TransactionsAdmin)
admin.site.register(Payment, PaymentsAdmin)