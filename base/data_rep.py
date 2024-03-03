from django.shortcuts import render, redirect  # To render HTML page and redirect from one page to another
from django.http import HttpResponse  # For Text printing
from django.db.models import Q  # Is used to Query data from table by sorting it with some parameter
from django.contrib.auth.models import User  # For user Authentication
from django.contrib.auth import authenticate, login, logout  # To Login, logout, functionality
from django.contrib.auth.decorators import login_required  # Wrap funtion inside decorater which checks login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  # To show message
from .models import Room, Topic, Message  # Externally created DataBases
from .forms import RoomForm, UserForm  # Auto generated form for user input


def login_page(request):
	"""For user login"""

	page = "login"

	# If user is already loged in and sends request on login url they will be redirected to home page
	if request.user.is_authenticated:
		return redirect("home")

	# Post req means user has submitted the form
	if request.method == "POST":
		# Collect input data
		name = request.POST.get("username").lower()
		password = request.POST.get("password")

		# Check if user is authenticated or not, show message if not authenticate user
		try:
			user = User.is_authenticated(username=name)
		except:
			messages.error(request, 'User does not exists')

		# If user is authenticated then, let user login
		user = authenticate(request, username=name, password=password)

		if user is not None:
			# "login()" method will pass a request object and make a session variable for the given user
			login(request, user)
			return redirect("home")
		else:
			messages.error(request, "User Name OR Password doesn't exist")

	context = {"page": page}
	return render(request, "base/login_register.html", context)


def log_out(request):
	"""For user log-out"""

	# Delete the session object
	logout(request)
	return redirect("home")


def register_page(request):
	""" Create Auto Generated Registration form using "UserCreationForm" method"""

	form = UserCreationForm()

	if request.method == "POST":
		form = UserCreationForm(request.POST)
		try:
			if form.is_valid:
				user = form.save(commit=False)
				user.username = user.username.lower()
				user.save()
				login(request, user)
				return redirect("home")
		except:
			messages.error(request, "Some Error Occured, Try Again ..!")

	return render(request, "base/login_register.html", {"form": form})


def home(request):
	""" Fetches all the objects of room model from database and pass it as context to home page to print """

	# Will fetch the data from url inside q and if q doesn't match any data then return empty string
	q = request.GET.get("q") if request.GET.get('q') != None else " "

	# Here instead of using 'topic__name' we'll use 'topic__name_icontains'
	# It will filter as: Atleast value in q has to be there in topic(not complete match of 100%)
	# [i] in 'icontains' stands for case sensitive
	rooms = Room.objects.filter(
		Q(topic__name__icontains=q) |
		Q(name__icontains=q) |
		Q(description__icontains=q)
	)

	# Count total number of room entry
	room_count = rooms.count()

	# Will fetch all topics name and display it for filter by topic
	topics = Topic.objects.all()[0:5]

	# Grab all the message related to room name filter applied
	room_messages = Message.objects.filter(
		Q(room__topic__name__icontains=q) |
		Q(room__name__icontains=q)
	)

	context = {"rooms": rooms, "topics": topics, "room_count": room_count,
			   "room_messages": room_messages}

	return render(request, "base/home.html", context=context)

def user_profile(request, pk):
	"""For Displaying all the information of a specific user"""


