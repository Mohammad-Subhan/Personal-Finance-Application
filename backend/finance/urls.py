from django.urls import path
from . import views

urlpatterns = [
    path("auth/register", views.register_view, name="register"),
    path("auth/login", views.login_view, name="login"),
    path("auth/logout", views.logout_view, name="logout"),
    path("wallet/create", views.create_wallet, name="create_wallet"),
    path("user/wallet/create", views.create_user_wallet, name="create_user_wallet"),
    path("user/wallet/delete", views.delete_user_wallet, name="delete_user_wallet"),
    path("user/wallet/update", views.update_user_wallet, name="update_user_wallet"),
    path("user/wallet/get", views.get_user_wallet, name="get_user_wallet"),
    path("user/wallet/get/all", views.get_all_user_wallet, name="get_all_user_wallet"),
    path("wallet/transaction/create", views.create_transaction, name="create_transaction"),
    path("wallet/transaction/delete", views.delete_transaction, name="delete_transaction"),
    path("wallet/transaction/update", views.update_transaction, name="update_transaction"),
    path("wallet/transaction/get", views.get_transaction, name="get_transaction"),
    path("wallet/transaction/get/all", views.get_all_transactions, name="get_all_transaction"),
    path("user/payments/create", views.create_payment, name="create_payment"),
    path("user/payments/delete", views.delete_payment, name="delete_payment"),
    path("user/payments/update", views.update_payment, name="update_payment"),
    path("user/payments/get", views.get_payment, name="get_payment"),
    path("user/payments/get/all", views.get_all_payments, name="get_all_payments"),
    path("user/payment/mark", views.mark_payment, name="mark_payment"),
]
