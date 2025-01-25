import json
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Wallet, User, UserWallet, Category, Transactions, Payments
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.csrf import csrf_exempt
from .supabase import supabase
import os


@csrf_exempt
def register_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            fullName = data["full_name"]
            userName = data["user_name"]
            email = data["email"]
            password = data["password"]

            if (
                fullName is None
                or userName is None
                or email is None
                or password is None
            ):
                return JsonResponse(
                    {"message": "All fields are required", "success": False}, status=400
                )

            print(userName, fullName, email, password)  # for debugging

            # Create user with validated data
            user = User.objects.create_user(
                username=userName, fullName=fullName, email=email, password=password
            )
            user.save()
            login(request, user)

            return JsonResponse(
                {"message": "User created successfully", "success": True}, status=201
            )

        except IntegrityError:
            return JsonResponse(
                {"message": "User already exists", "success": False}, status=400
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
            userName = data["user_name"]
            password = data["password"]

            if userName is None or password is None:
                return JsonResponse(
                    {"message": "Username and password are required", "success": False},
                    status=400,
                )

            print(userName, password)  # for debugging

            # check if the user exists in the database
            user = authenticate(request, username=userName, password=password)

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
                            "full_name": user.fullName,
                            "user_name": user.username,
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


def upload_image(file, bucketName="images"):
    try:
        fileName = os.path.basename(file.name)  # Get the file name
        fileContent = file.read()  # Read the file content

        # Upload the file as a binary stream
        response = supabase.storage.from_(bucketName).upload(fileName, fileContent)

        # Generate public URL for the uploaded file
        publicURL = supabase.storage.from_(bucketName).get_public_url(fileName)

        return {"success": True, "url": publicURL}

    except Exception as e:
        return {"success": False, "error": str(e)}


@csrf_exempt
def create_wallet(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                name = data["name"]
                icon = request.FILES.get("icon")

                if name is None:
                    return JsonResponse(
                        {"message": "Name is required", "success": False},
                        status=400,
                    )

                if icon is None:
                    iconURL = supabase.storage.from_("images").get_public_url(
                        "wallet.png"
                    )
                else:
                    link = upload_image(icon)
                    if not link["success"]:
                        return JsonResponse(
                            {"message": "Image upload failed", "success": False},
                            status=500,
                        )
                    iconURL = link["url"]

                # Create wallet with validated data
                Wallet.objects.create(name=name, icon=iconURL)

                return JsonResponse(
                    {
                        "message": "Wallet created successfully",
                        "success": True,
                        "wallet": {"name": name, "icon": iconURL},
                    },
                    status=201,
                )

            except IntegrityError:
                return JsonResponse(
                    {"message": "Wallet already exists", "success": False}, status=400
                )

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
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )


@csrf_exempt
def create_user_wallet(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                user = request.user
                walletID = data["wallet_id"]
                name = data["name"]

                if walletID is None or name is None:
                    return JsonResponse(
                        {
                            "message": "Wallet ID and name are required",
                            "success": False,
                        },
                        status=400,
                    )

                if not Wallet.objects.filter(id=walletID).exists():
                    return JsonResponse(
                        {"message": "Wallet does not exist", "success": False},
                        status=400,
                    )

                # Create user wallet with validated data
                userWallet = UserWallet.objects.create(
                    user=user, wallet=Wallet.objects.get(id=walletID), name=name
                )

                return JsonResponse(
                    {
                        "message": "User wallet created successfully",
                        "success": True,
                    },
                    status=201,
                )

            except IntegrityError:
                return JsonResponse(
                    {"message": "User wallet already exists", "success": False},
                    status=400,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON", "success": False}, status=400
                )

            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse(
                    {"message": "User wallet creation failed", "success": False},
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    "message": "Invalid request method. POST method required",
                    "success": False,
                },
                status=405,
            )
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )


@csrf_exempt
def delete_user_wallet(request):
    if request.user.is_authenticated:
        if request.method == "DELETE":
            try:
                data = json.loads(request.body)
                userWalletID = data["user_wallet_id"]

                if userWalletID is None:
                    return JsonResponse(
                        {"message": "User wallet ID is required", "success": False},
                        status=400,
                    )

                if not UserWallet.objects.filter(id=userWalletID).exists():
                    return JsonResponse(
                        {"message": "User wallet does not exist", "success": False},
                        status=400,
                    )

                # Delete user wallet
                UserWallet.objects.get(id=userWalletID).delete()

                return JsonResponse(
                    {
                        "message": "User wallet deleted successfully",
                        "success": True,
                    },
                    status=200,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON", "success": False}, status=400
                )

            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse(
                    {"message": "User wallet deletion failed", "success": False},
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    "message": "Invalid request method. DELETE method required",
                    "success": False,
                },
                status=405,
            )
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )


@csrf_exempt
def update_user_wallet(request):
    if request.user.is_authenticated:
        if request.method == "PUT":
            try:
                data = json.loads(request.body)
                userWalletID = data["user_wallet_id"]
                name = data["name"]

                if userWalletID is None or name is None:
                    return JsonResponse(
                        {
                            "message": "User wallet ID and name are required",
                            "success": False,
                        },
                        status=400,
                    )

                if not UserWallet.objects.filter(id=userWalletID).exists():
                    return JsonResponse(
                        {"message": "User wallet does not exist", "success": False},
                        status=400,
                    )

                # Update the user wallet name
                UserWallet.objects.filter(id=userWalletID).update(name=name)

                return JsonResponse(
                    {
                        "message": "User wallet updated successfully",
                        "success": True,
                    },
                    status=200,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON", "success": False}, status=400
                )

            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse(
                    {"message": "User wallet updation failed", "success": False},
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    "message": "Invalid request method. PUT method required",
                    "success": False,
                },
                status=405,
            )
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )


def get_user_wallet(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            try:
                data = json.loads(request.body)
                userWalletID = data["user_wallet_id"]

                if userWalletID is None:
                    return JsonResponse(
                        {
                            "message": "User wallet ID is required",
                            "success": False,
                        },
                        status=400,
                    )

                if not UserWallet.objects.filter(id=userWalletID).exists():
                    return JsonResponse(
                        {"message": "User wallet does not exist", "success": False},
                        status=400,
                    )

                userWallet = UserWallet.objects.get(id=userWalletID)

                return JsonResponse(
                    {
                        "message": "User wallet retrieved successfully",
                        "success": True,
                        "user_wallet": {
                            "id": userWallet.id,
                            "name": userWallet.name,
                            "user": userWallet.user.fullName,
                            "wallet": {
                                "id": userWallet.wallet.id,
                                "name": userWallet.wallet.name,
                                "icon": userWallet.wallet.icon,
                            },
                        },
                    },
                    status=200,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON", "success": False}, status=400
                )

            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse(
                    {"message": "User wallet retrieval failed", "success": False},
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    "message": "Invalid request method. GET method required",
                    "success": False,
                },
                status=405,
            )
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )


def get_all_user_wallet(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            try:
                data = json.loads(request.body)
                user = request.user

                if not UserWallet.objects.filter(user=user).exists():
                    return JsonResponse(
                        {"message": "User wallets do not exist", "success": False},
                        status=400,
                    )

                userWallets = UserWallet.objects.filter(user=user)

                wallets = []
                for userWallet in userWallets:
                    wallets.append(
                        {
                            "id": userWallet.id,
                            "name": userWallet.name,
                            "user": userWallet.user.fullName,
                            "wallet": {
                                "id": userWallet.wallet.id,
                                "name": userWallet.wallet.name,
                                "icon": userWallet.wallet.icon,
                            },
                        }
                    )

                return JsonResponse(
                    {
                        "message": "User wallets retrieved successfully",
                        "success": True,
                        "user_wallets": wallets,
                    },
                    status=200,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON", "success": False}, status=400
                )

            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse(
                    {"message": "User wallet retrieval failed", "success": False},
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    "message": "Invalid request method. GET method required",
                    "success": False,
                },
                status=405,
            )
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )


@csrf_exempt
def create_transaction(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                user = request.user
                userWalletID = data["user_wallet_id"]
                amount = data["amount"]
                categoryID = data["category"]
                transactionType = data["type"]
                description = data["description"]
                spPerson = data["sp_person"]

                if (
                    userWalletID is None
                    or amount is None
                    or categoryID is None
                    or transactionType is None
                ):
                    return JsonResponse(
                        {
                            "message": "User wallet ID, amount, category, and type are required",
                            "success": False,
                        },
                        status=400,
                    )

                if not UserWallet.objects.filter(id=userWalletID).exists():
                    return JsonResponse(
                        {"message": "User wallet does not exist", "success": False},
                        status=400,
                    )

                if not Category.objects.filter(id=categoryID).exists():
                    return JsonResponse(
                        {"message": "Category does not exist", "success": False},
                        status=400,
                    )

                if amount < 0:
                    return JsonResponse(
                        {"message": "Amount cannot be negative", "success": False},
                        status=400,
                    )

                if transactionType not in ["credit", "debit"]:
                    return JsonResponse(
                        {
                            "message": "Transaction type must be either 'credit' or 'debit'",
                            "success": False,
                        },
                        status=400,
                    )

                transaction = Transactions.objects.create(
                    userWallet=UserWallet.objects.get(id=userWalletID),
                    amount=amount,
                    category=Category.objects.get(id=categoryID),
                    type=transactionType,
                    description=description,
                    spPerson=spPerson,
                )

                return JsonResponse(
                    {
                        "message": "Transaction created successfully",
                        "success": True,
                        "transaction": {
                            "id": transaction.id,
                            "user_wallet": {
                                "id": transaction.userWallet.id,
                                "name": transaction.userWallet.name,
                                "user": transaction.userWallet.user.fullName,
                                "wallet": {
                                    "id": transaction.userWallet.wallet.id,
                                    "name": transaction.userWallet.wallet.name,
                                    "icon": transaction.userWallet.wallet.icon,
                                },
                            },
                            "amount": transaction.amount,
                            "category": transaction.category.name,
                            "type": transaction.type,
                            "description": transaction.description,
                            "sp_person": transaction.spPerson,
                        },
                    },
                    status=201,
                )

            except IntegrityError:
                return JsonResponse(
                    {"message": "Transaction already exists", "success": False},
                    status=400,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON", "success": False}, status=400
                )

            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse(
                    {"message": "Transaction creation failed", "success": False},
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    "message": "Invalid request method. POST method required",
                    "success": False,
                },
                status=405,
            )
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )


@csrf_exempt
def delete_transaction(request):
    if request.user.is_authenticated:
        if request.method == "DELETE":
            try:
                data = json.loads(request.body)
                transactionID = data["transaction_id"]

                if transactionID is None:
                    return JsonResponse(
                        {"message": "Transaction ID is required", "success": False},
                        status=400,
                    )

                if not Transactions.objects.filter(id=transactionID).exists():
                    return JsonResponse(
                        {"message": "Transaction does not exist", "success": False},
                        status=400,
                    )

                # Delete transaction
                Transactions.objects.get(id=transactionID).delete()

                return JsonResponse(
                    {
                        "message": "Transaction deleted successfully",
                        "success": True,
                    },
                    status=200,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON", "success": False}, status=400
                )

            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse(
                    {"message": "Transaction deletion failed", "success": False},
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    "message": "Invalid request method. DELETE method required",
                    "success": False,
                },
                status=405,
            )
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )


@csrf_exempt
def update_transaction(request):
    if request.user.is_authenticated:
        if request.method == "PUT":
            try:
                data = json.loads(request.body)
                transactionID = data["transaction_id"]
                amount = data["amount"]
                categoryID = data["category"]
                transactionType = data["type"]
                description = data["description"]
                spPerson = data["sp_person"]

                if transactionID is None:
                    return JsonResponse(
                        {"message": "Transaction ID is required", "success": False},
                        status=400,
                    )

                if not Transactions.objects.filter(id=transactionID).exists():
                    return JsonResponse(
                        {"message": "Transaction does not exist", "success": False},
                        status=400,
                    )

                transaction = Transactions.objects.get(id=transactionID)

                if amount is None:
                    amount = transaction.amount
                else:
                    if amount < 0:
                        return JsonResponse(
                            {"message": "Amount cannot be negative", "success": False},
                            status=400,
                        )

                if categoryID is None:
                    categoryID = transaction.category.id
                else:
                    if not Category.objects.filter(id=categoryID).exists():
                        return JsonResponse(
                            {"message": "Category does not exist", "success": False},
                            status=400,
                        )

                if transactionType is None:
                    transactionType = transaction.type
                else:
                    if transactionType not in ["credit", "debit"]:
                        return JsonResponse(
                            {
                                "message": "Transaction type must be either 'credit' or 'debit'",
                                "success": False,
                            },
                            status=400,
                        )

                if description is None:
                    description = transaction.description

                if spPerson is None:
                    spPerson = transaction.spPerson

                # Update the transaction
                Transactions.objects.filter(id=transactionID).update(
                    amount=amount,
                    category=Category.objects.get(id=categoryID),
                    type=transactionType,
                    description=description,
                    spPerson=spPerson,
                )

                transaction = Transactions.objects.get(id=transactionID)

                return JsonResponse(
                    {
                        "message": "Transaction updated successfully",
                        "success": True,
                        "transaction": {
                            "id": transaction.id,
                            "user_wallet": {
                                "id": transaction.userWallet.id,
                                "name": transaction.userWallet.name,
                                "user": transaction.userWallet.user.fullName,
                                "wallet": {
                                    "id": transaction.userWallet.wallet.id,
                                    "name": transaction.userWallet.wallet.name,
                                    "icon": transaction.userWallet.wallet.icon,
                                },
                            },
                            "amount": transaction.amount,
                            "category": transaction.category.name,
                            "type": transaction.type,
                            "description": transaction.description,
                            "sp_person": transaction.spPerson,
                        },
                    },
                    status=200,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON", "success": False}, status=400
                )

            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse(
                    {"message": "Transaction update failed", "success": False},
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    "message": "Invalid request method. PUT method required",
                    "success": False,
                },
                status=405,
            )
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )


def get_transaction(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            try:
                data = json.loads(request.body)
                transactionID = data["transaction_id"]

                if transactionID is None:
                    return JsonResponse(
                        {"message": "Transaction ID is required", "success": False},
                        status=400,
                    )

                if not Transactions.objects.filter(id=transactionID).exists():
                    return JsonResponse(
                        {"message": "Transaction does not exist", "success": False},
                        status=400,
                    )

                transaction = Transactions.objects.get(id=transactionID)

                return JsonResponse(
                    {
                        "message": "Transaction retrieved successfully",
                        "success": True,
                        "transaction": {
                            "id": transaction.id,
                            "user_wallet": {
                                "id": transaction.userWallet.id,
                                "name": transaction.userWallet.name,
                                "user": transaction.userWallet.user.fullName,
                                "wallet": {
                                    "id": transaction.userWallet.wallet.id,
                                    "name": transaction.userWallet.wallet.name,
                                    "icon": transaction.userWallet.wallet.icon,
                                },
                            },
                            "amount": transaction.amount,
                            "category": transaction.category.name,
                            "type": transaction.type,
                            "description": transaction.description,
                            "sp_person": transaction.spPerson,
                        },
                    },
                    status=200,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON", "success": False}, status=400
                )

            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse(
                    {"message": "Transaction update failed", "success": False},
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    "message": "Invalid request method. GET method required",
                    "success": False,
                },
                status=405,
            )
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )


def get_all_transactions(request):
    if request.user.is_autheticated:
        if request.method == "GET":
            try:
                data = json.loads(request.body)
                user = request.user

                if not UserWallet.objects.filter(user=user).exists():
                    return JsonResponse(
                        {"message": "User wallets do not exist", "success": False},
                        status=400,
                    )

                userWallets = UserWallet.objects.filter(user=user)
                transactions = []

                for userWallet in userWallets:
                    for transaction in userWallet.transactions.all():
                        transactions.append(
                            {
                                "id": transaction.id,
                                "user_wallet": {
                                    "id": transaction.userWallet.id,
                                    "name": transaction.userWallet.name,
                                    "user": transaction.userWallet.user.fullName,
                                    "wallet": {
                                        "id": transaction.userWallet.wallet.id,
                                        "name": transaction.userWallet.wallet.name,
                                        "icon": transaction.userWallet.wallet.icon,
                                    },
                                },
                                "amount": transaction.amount,
                                "category": transaction.category.name,
                                "type": transaction.type,
                                "description": transaction.description,
                                "sp_person": transaction.spPerson,
                            }
                        )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON", "success": False}, status=400
                )

            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse(
                    {"message": "Transaction retrieval failed", "success": False},
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    "message": "Invalid request method. GET method required",
                    "success": False,
                },
                status=405,
            )
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )


@csrf_exempt
def create_payment(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                user = request.user
                paymentType = data["type"]
                description = data["description"]
                spPerson = data["sp_person"]
                amount = data["amount"]

                if (
                    paymentType is None
                    or description is None
                    or spPerson is None
                    or amount is None
                ):
                    return JsonResponse(
                        {
                            "message": "Payment type, description, special person, and amount are required",
                            "success": False,
                        },
                        status=400,
                    )

                if amount < 0:
                    return JsonResponse(
                        {"message": "Amount cannot be negative", "success": False},
                        status=400,
                    )

                payment = Payments.objects.create(
                    user=user,
                    type=paymentType,
                    description=description,
                    spPerson=spPerson,
                    amount=amount,
                )

                return JsonResponse(
                    {
                        "message": "Payment created successfully",
                        "success": True,
                        "payment": {
                            "id": payment.id,
                            "user": payment.user.fullName,
                            "type": payment.type,
                            "description": payment.description,
                            "sp_person": payment.spPerson,
                            "amount": payment.amount,
                            "state": payment.state,
                        },
                    },
                    status=201,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON", "success": False}, status=400
                )

            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse(
                    {"message": "Payment creation failed", "success": False},
                    status=500,
                )

        else:
            return JsonResponse(
                {
                    "message": "Invalid request method. POST method required",
                    "success": False,
                },
                status=405,
            )
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )


@csrf_exempt
def delete_payment(request):
    if request.user.is_authenticated:
        if request.mothod == "DELETE":
            try:
                data = json.loads(request.body)
                paymentID = data["payment_id"]

                if paymentID is None:
                    return JsonResponse(
                        {"message": "Payment ID is required", "success": False},
                        status=400,
                    )

                if not Payments.objects.filter(id=paymentID).exists():
                    return JsonResponse(
                        {"message": "Payment does not exist", "success": False},
                        status=400,
                    )

                # Delete payment
                Payments.objects.get(id=paymentID).delete()

                return JsonResponse(
                    {
                        "message": "Payment deleted successfully",
                        "success": True,
                    },
                    status=200,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON", "success": False}, status=400
                )

            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse(
                    {"message": "Payment deletion failed", "success": False},
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    "message": "Invalid request method. DELETE method required",
                    "success": False,
                },
                status=405,
            )
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )


@csrf_exempt
def update_payment(request):
    if request.user.is_authenticated:
        if request.method == "PUT":
            try:
                data = json.loads(request.body)
                paymentID = data["payment_id"]
                paymentType = data["type"]
                description = data["description"]
                spPerson = data["sp_person"]
                amount = data["amount"]
                state = data["state"]

                if paymentID is None:
                    return JsonResponse(
                        {"message": "Payment ID is required", "success": False},
                        status=400,
                    )

                if not Payments.objects.filter(id=paymentID).exists():
                    return JsonResponse(
                        {"message": "Payment does not exist", "success": False},
                        status=400,
                    )

                payment = Payments.objects.get(id=paymentID)

                if paymentType is None:
                    paymentType = payment.type

                if description is None:
                    description = payment.description

                if spPerson is None:
                    spPerson = payment.spPerson

                if amount is None:
                    amount = payment.amount
                else:
                    if amount < 0:
                        return JsonResponse(
                            {"message": "Amount cannot be negative", "success": False},
                            status=400,
                        )

                if state is None:
                    state = payment.state

                # Update the payment
                Payments.objects.filter(id=paymentID).update(
                    type=paymentType,
                    description=description,
                    spPerson=spPerson,
                    amount=amount,
                    state=state,
                )

                payment = Payments.objects.get(id=paymentID)

                return JsonResponse(
                    {
                        "message": "Payment updated successfully",
                        "success": True,
                        "payment": {
                            "id": payment.id,
                            "user": payment.user.fullName,
                            "type": payment.type,
                            "description": payment.description,
                            "sp_person": payment.spPerson,
                            "amount": payment.amount,
                            "state": payment.state,
                        },
                    },
                    status=200,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON", "success": False}, status=400
                )

            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse(
                    {"message": "Payment updation failed", "success": False},
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    "message": "Invalid request method. PUT method required",
                    "success": False,
                },
                status=405,
            )
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )


def get_payment(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            try:
                data = json.loads(request.body)
                paymentID = data["payment_id"]

                if paymentID is None:
                    return JsonResponse(
                        {"message": "Payment ID is required", "success": False},
                        status=400,
                    )

                if not Payments.objects.filter(id=paymentID).exists():
                    return JsonResponse(
                        {"message": "Payment does not exist", "success": False},
                        status=400,
                    )

                payment = Payments.objects.get(id=paymentID)

                return JsonResponse(
                    {
                        "message": "Payment retrieved successfully",
                        "success": True,
                        "payment": {
                            "id": payment.id,
                            "user": payment.user.fullName,
                            "type": payment.type,
                            "description": payment.description,
                            "sp_person": payment.spPerson,
                            "amount": payment.amount,
                            "state": payment.state,
                        },
                    },
                    status=200,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON", "success": False}, status=400
                )

            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse(
                    {"message": "Payment retrieval failed", "success": False},
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    "message": "Invalid request method. GET method required",
                    "success": False,
                },
                status=405,
            )
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )


def get_all_payments(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            try:
                user = request.user

                if not Payments.objects.filter(user=user).exists():
                    return JsonResponse(
                        {"message": "Payments do not exist", "success": False},
                        status=400,
                    )

                userPayments = Payments.objects.filter(user=user)
                payments = []

                for payment in userPayments:
                    payments.append(
                        {
                            "id": payment.id,
                            "user": payment.user.fullName,
                            "type": payment.type,
                            "description": payment.description,
                            "sp_person": payment.spPerson,
                            "amount": payment.amount,
                            "state": payment.state,
                        }
                    )

                return JsonResponse(
                    {
                        "message": "Payments retrieved successfully",
                        "success": True,
                        "payments": payments,
                    },
                    status=200,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON", "success": False}, status=400
                )

            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse(
                    {"message": "Payment retrieval failed", "success": False},
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    "message": "Invalid request method. GET method required",
                    "success": False,
                },
                status=405,
            )
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )


@csrf_exempt
def mark_payment(request):
    if request.user.is_authenticated:
        if request.method == "PUT":
            try:
                data = json.loads(request.body)
                paymentID = data["payment_id"]

                if paymentID is None:
                    return JsonResponse(
                        {"message": "Payment ID is required", "success": False},
                        status=400,
                    )

                if not Payments.objects.filter(id=paymentID).exists():
                    return JsonResponse(
                        {"message": "Payment does not exist", "success": False},
                        status=400,
                    )

                Payments.objects.filter(id=paymentID).update(state=True)

                return JsonResponse(
                    {
                        "message": "Payment marked as paid successfully",
                        "success": True,
                    },
                    status=200,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"message": "Invalid JSON", "success": False}, status=400
                )

            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse(
                    {"message": "Payment updation failed", "success": False},
                    status=500,
                )
        else:
            return JsonResponse(
                {
                    "message": "Invalid request method. PUT method required",
                    "success": False,
                },
                status=405,
            )
    else:
        return JsonResponse(
            {"message": "User not logged in", "success": False},
            status=401,
        )
