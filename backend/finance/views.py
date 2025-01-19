from django.shortcuts import render
import json
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.csrf import csrf_exempt
from .supabase import supabase
from .models import WalletAccount, TansactionCategory, WalletTransactions
import os

User = get_user_model()


@csrf_exempt
def register_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data["username"]
            email = data["email"]
            password = data["password"]

            # Create user with validated data
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.save()
            login(request, user)

            return JsonResponse(
                {"message": "User created successfully", "success": True}, status=201
            )

        except IntegrityError:
            return JsonResponse(
                {"message": "Username already taken", "success": False}, status=400
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"message": "Invalid JSON", "success": False}, status=400
            )

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse(
                {"message": "User creation failed", "success": False}, status=500
            )
    else:
        return JsonResponse(
            {
                "message": "Invalid request method. POST method required",
                "success": False,
            },
            status=405,
        )


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            # get the data from the form
            data = json.loads(request.body)
            username = data["username"]
            password = data["password"]

            print(username, password)  # for debugging

            # check if the user exists in the database
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                # return a success response
                return JsonResponse(
                    {
                        "message": "User logged in successfully",
                        "success": True,
                        "user": {
                            "id": user.id,
                            "username": user.username,
                            "email": user.email,
                        },
                    },
                    status=200,
                )
            else:
                # return a failure response
                return JsonResponse(
                    {
                        "message": "User not found. Invalid username or password",
                        "success": False,
                        "user": None,
                    },
                    status=401,
                )

        except json.JSONDecodeError:
            return JsonResponse(
                {"message": "Invalid JSON", "success": False}, status=400
            )

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse(
                {"message": "User login failed", "success": False}, status=500
            )
    else:
        return JsonResponse(
            {
                "message": "Invalid request method. POST method required",
                "success": False,
            },
            status=405,
        )


@csrf_exempt
def logout_view(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse(
                {"message": "User logged out successfully", "success": True}, status=200
            )

        else:
            return JsonResponse(
                {"message": "User not logged in", "success": False}, status=401
            )

    else:
        return JsonResponse(
            {
                "message": "Invalid request method. POST method required",
                "success": False,
            },
            status=405,
        )


def upload_image(file, bucket_name="images"):
    try:
        file_name = os.path.basename(file.name)  # Get the file name
        file_content = file.read()  # Read the file content

        # Upload the file as a binary stream
        response = supabase.storage.from_(bucket_name).upload(file_name, file_content)

        # Generate public URL for the uploaded file
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)

        return {"success": True, "url": public_url}

    except Exception as e:
        return {"success": False, "error": str(e)}


@csrf_exempt
def create_wallet(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data["name"]
            icon = request.FILES.get("icon")

            if name is None or icon is None:
                return JsonResponse(
                    {"message": "Name and icon are required", "success": False},
                    status=400,
                )

            link = upload_image(icon)
            print(link)
            return JsonResponse({"test": "OK"})

        except json.JSONDecodeError:
            return JsonResponse(
                {"message": "Invalid JSON", "success": False}, status=400
            )

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse(
                {"message": "Wallet creation failed", "success": False}, status=500
            )
    else:
        return JsonResponse(
            {
                "message": "Invalid request method. POST method required",
                "success": False,
            },
            status=405,
        )


@csrf_exempt
def add_transaction(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data["user_id"]
            wallet_id = data["wallet_id"]
            amount = data["amount"]
            category_id = data["category"]
            description = data["description"]
            transaction_type = data["transaction_type"]

            if (
                user_id is None
                or wallet_id is None
                or amount is None
                or category_id is None
                or description is None
                or transaction_type is None
            ):
                return JsonResponse(
                    {"message": "All fields are required", "success": False},
                    status=400,
                )

            if not User.objects.filter(id=user_id).exists():
                return JsonResponse(
                    {"message": "User does not exist", "success": False},
                    status=400,
                )

            if not WalletAccount.objects.filter(id=wallet_id).exists():
                return JsonResponse(
                    {"message": "Wallet does not exist", "success": False},
                    status=400,
                )

            if not TansactionCategory.objects.filter(id=category_id).exists():
                return JsonResponse(
                    {"message": "Category does not exist", "success": False},
                    status=400,
                )

            if amount < 0:
                return JsonResponse(
                    {"message": "Amount cannot be negative", "success": False},
                    status=400,
                )

            if transaction_type not in ["credit", "debit"]:
                return JsonResponse(
                    {
                        "message": "Transaction type must be either 'credit' or 'debit'",
                        "success": False,
                    },
                    status=400,
                )

            # Create transaction with validated data
            transaction = WalletTransactions(
                user=User.objects.get(id=user_id),
                wallet_account=wallet_id,
                amount=amount,
                category=TansactionCategory.objects.get(id=category_id),
                description=description,
                type=transaction_type,
            )

            return JsonResponse(
                {"message": "Transaction created successfully", "success": True},
                status=201,
            )

        except IntegrityError:
            return JsonResponse(
                {"message": "Transaction already exists", "success": False}, status=400
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"message": "Invalid JSON", "success": False}, status=400
            )

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse(
                {"message": "Transaction creation failed", "success": False}, status=500
            )
    else:
        return JsonResponse(
            {
                "message": "Invalid request method. POST method required",
                "success": False,
            },
            status=405,
        )


def delete_transaction(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            wallet_id = data.get("wallet_id")

            if user_id is None or wallet_id is None:
                return JsonResponse(
                    {
                        "message": "User ID and Wallet ID both are required",
                        "success": False,
                    },
                    status=400,
                )

            if not WalletTransactions.objects.filter(
                user=User.objects.filter(id=user_id),
                wallet_account=WalletAccount.objects.filter(id=wallet_id),
            ).exists():
                return JsonResponse(
                    {"message": "Transaction does not exist", "success": False},
                    status=400,
                )

            # Delete transaction
            WalletTransactions.objects.get(
                user=User.objects.filter(id=user_id),
                wallet_account=WalletAccount.objects.filter(id=wallet_id),
            ).delete()

            return JsonResponse(
                {"message": "Transaction deleted successfully", "success": True},
                status=200,
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"message": "Invalid JSON", "success": False}, status=400
            )

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse(
                {"message": "Transaction deletion failed", "success": False}, status=500
            )
    else:
        return JsonResponse(
            {
                "message": "Invalid request method. DELETE method required",
                "success": False,
            },
            status=405,
        )


def update_transaction(request):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            wallet_id = data.get("wallet_id")
            amount = data.get("amount")
            category_id = data.get("category")
            description = data.get("description")
            transaction_type = data.get("transaction_type")

            if user_id is None or wallet_id is None:
                return JsonResponse(
                    {
                        "message": "User ID and Wallet ID both are required",
                        "success": False,
                    },
                    status=400,
                )

            if not User.objects.filter(id=user_id).exists():
                return JsonResponse(
                    {"message": "User does not exist", "success": False}, status=400
                )

            if not WalletAccount.objects.filter(id=wallet_id).exists():
                return JsonResponse(
                    {"message": "Wallet does not exist", "success": False}, status=400
                )

            transaction = WalletTransactions.objects.filter(
                user=User.objects.filter(id=user_id),
                wallet_account=WalletAccount.objects.filter(id=wallet_id),
            ).update(
                amount=amount,
                category=TansactionCategory.objects.filter(id=category_id),
                type=transaction_type,
                description=description,
            )

            return JsonResponse(
                {"message": "Transaction updated successfully", "success": True},
                status=200,
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"message": "Invalid JSON", "success": False}, status=400
            )

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse(
                {"message": "Transaction update failed", "success": False}, status=500
            )
    else:
        return JsonResponse(
            {
                "message": "Invalid request method. PUT method required",
                "success": False,
            },
            status=405,
        )


# def get_transaction(request):
#     if request.method == "GET":
#         try:
#             data = json.loads(request.body)
        
#         except json.JSONDecodeError:
#             return JsonResponse(
#                 {"message": "Invalid JSON", "success": False}, status=400
#             )
            
#         except Exception as e:
#             print(f"Error: {e}")
#             return JsonResponse(
#                 {"message": "Transaction update failed", "success": False}, status=500
#             )
#     else:
#         return JsonResponse(
#             {
#                 "message": "Invalid request method. GET method required",
#                 "success": False,
#             },
#             status=405,
#         )
