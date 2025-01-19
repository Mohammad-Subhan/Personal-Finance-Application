from django.urls import path
from . import views

urlpatterns = [
    path("auth/register/", views.register_view, name="register"),
    path("auth/login/", views.login_view, name="login"),
    path("auth/logout/", views.logout_view, name="logout"),
    path("wallet/create/", views.create_wallet, name="create_wallet"),
    path("wallet/transaction/add", views.add_transaction, name="add_transaction"),
    path("wallet/transaction/delete", views.delete_transaction, name="delete_transaction"),
    path("wallet/transaction/update", views.update_transaction, name="update_transaction"),
    # path("wallet/transaction/get", views.get_transaction, name="get_transaction"),
]
