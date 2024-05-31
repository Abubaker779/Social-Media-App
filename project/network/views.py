import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Comment


def index(request):
    return render(request, "network/index.html")


# posts and comments
@login_required
@csrf_exempt
def get_posts(request):

    # Check for the Get request to send the email
    if request.method == "GET":
        try:

            posts=Post.objects.filter(user=request.user).all()
            posts=posts.order_by("date,time").all()

            return JsonResponse([post.serialize() for post in posts], safe=False)
        
        except User.DoesNotExist:
            return JsonResponse({"error":"User does not exist."},status=400)
        
        except Post.DoesNotExist:
            return JsonResponse({"error":"Post Does not exist."},status=400)
        
    else:
        return JsonResponse({"error":"This method is Invalid 'GET' method required."}, status=400)    
    

# Route for adding post 
@login_required
def add_post(request):

    # Check for Post method and then save the user
    if request.method == "POST":

        try:
            
            body=request.POST["body"]
            post=Post(user=request.user,body=body)  
            post.save()

        except User.DoesNotExist:
            return JsonResponse({"error":"User DoesNotExist."},status=400)    

        return JsonResponse({"success":"Posted successfully."},status=201)
    
    else:
        return JsonResponse({"error":f"'{request.method}' method is Invalid ('POST' method required)."},status=403)


# Route for deleting post
@login_required
def del_post(request,post_id):

    # checks if method is POST then delete the particular post
    if request.method == "POST":

        try:

            post=Post.objects.filter(pk=post_id, user=request.user)
            post.delete()
            
        except Post.DoesNotExist:
            return JsonResponse({"error":"This particular post doesn't exist."}, status=400)
        
    else:
        return JsonResponse({"error":f"'{request.method}' method is Invalid ('POST' method required)"})  
    

# Route to make modifications to the posts 
@csrf_exempt
@login_required
def modify_post(request,post_id,modification_type,comment=""):    

    # Check for the Put method and then modify the posts as wanted
    if request.method == "PUT":
        
        try:

            if modification_type=="like":

                post=Post.objects.get(pk=post_id)
                post.like()

            elif modification_type=="unlike":

                post=Post.objects.get(pk=post_id)
                post.like()

            elif modification_type=="add_comment":

                post=Post.objects.get(pk=post_id)
                comment=Comment(user=request.user,comment=comment)
                post.comment.add(comment)
                
            elif modification_type=="delete_comment":

                post=Post.objects.get(pk=post_id)
                comment=post.comment.filter(user=request.user, comment=comment)
                comment.delete()

        except Post.DoesNotExist:
            return JsonResponse({"error":f"Post with post_id ({post_id}) doesn't exist."},status=400)

        except User.DoesNotExist:
            return JsonResponse({"error":f"This ({request.user}) particular user doesn't exist."},status=400)

    else:
        return JsonResponse({"error":f"'{request.method}' method is Invalid ('Put' method required)."}, status=400)        
    

# Route to follow someone
@csrf_exempt
@login_required
def follow(request, person_id, n_o_t):

    # Checking for Put method and then follow the user
    if request.method == "PUT" and n_o_t == 'true':

        try:

            person = User.objects.get(pk=person_id)
            user = User.objects.get(username=request.user.username)
            user.followers.add(person)

        except User.DoesNotExist:
            return JsonResponse({"error":"User Dosen't exist."})    

    # Checking for Put method and then un fo    
    if request.method == "PUT" and n_o_t == 'false':

        try:

            person=User.objects.get(pk=person_id)
            user=User.objects.get(username=request.user.username)
            user.followers.remove(user=person)
        
        except User.DoesNotExist:
            return JsonResponse({"error":"User doest not exist."}, status=400)
        
    return JsonResponse({"error":"This method is Invalid (PUT) method required"}, status=400)


#Route to log the User In
def login_view(request):

    # Checking the method and LoggingIn
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    
    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:

            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:

            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:

            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)

        return HttpResponseRedirect(reverse("index"))
    
    else: 

        return render(request, "network/register.html")
