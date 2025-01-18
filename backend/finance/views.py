from django.shortcuts import render
import json
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.csrf import csrf_exempt
from .supabase import supabase

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


# def upload_image(file, bucket_name="images"):
#     try:
#         file_name = file.name  # Get the file name
#         file_content = file.read()  # Read file content

#         # Upload the file to Supabase Storage
#         response = supabase.storage.from_(bucket_name).upload(file_name, file_content)

#         # Generate public URL for the uploaded file
#         public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)

#         return {"success": True, "url": public_url}

#     except Exception as e:
#         return {"success": False, "error": str(e)}

# @csrf_exempt
# def create_wallet(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             name = data["name"]
#             icon = open("D:\\Programming Projects\\Personal-Finance-Application\\backend\\finance\\test.jpg", "b")
            
#             if name is None or icon is None:
#                 return JsonResponse(
#                     {"message": "Name and icon are required", "success": False},
#                     status=400,
#                 )
                
#             link = upload_image(icon)
#             print(link)
#             return JsonResponse(
#                 {"test":"OK"}
#             )
            
#         except json.JSONDecodeError:
#             return JsonResponse(
#                 {"message": "Invalid JSON", "success": False}, status=400
#             )

#         except Exception as e:
#             print(f"Error: {e}")
#             return JsonResponse(
#                 {"message": "Wallet creation failed", "success": False}, status=500
#             )
#     else:
#         return JsonResponse(
#             {
#                 "message": "Invalid request method. POST method required",
#                 "success": False,
#             },
#             status=405,
#         )
