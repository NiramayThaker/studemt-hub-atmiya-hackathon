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


# Create your views here.

# BOILERPLATE DATA
# rooms = [
#     {"id": 1, "name": "Python"},
#     {"id": 2, "name": "Back-end"},
#     {"id": 3, "name": "Front-end"},
# ]


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


def room(request, pk):
	""" pk is being used for dynamic url redirection
		It will have a ID through which we can distingues between rooms
	"""

	# Here we are extracting all the data of a room which has id PK which is passed as parameter
	room = Room.objects.get(id=pk)
	# And passing the data of that specific room as context to room.html and it will display it

	# It will fetch all the data from message model related to room model in the form of 'sets'
	room_messages = room.message_set.all().order_by('-created')  # Filp the order by last posted first
	# Message is a DB Model which is child of Room model

	# Fetch all the participants name from table for a single room
	participants = room.participants.all()

	if request.method == 'POST':
		# Using inbuld message model to putting our meesage on screen
		message = Message.objects.create(
			user=request.user,
			room=room,
			body=request.POST.get('body')
		)

		""" It will work as if any user has commented in the room then 
		he will be automatically added inside the participates list """
		room.participants.add(request.user)

		# Reloading page so we are back with get request
		return redirect("room", pk=room.id)

	context = {"room": room, "room_messages": room_messages, "participants": participants}

	return render(request, "base/room.html", context)


def user_profile(request, pk):
	"""For Displaying all the information of a specific user"""

	user = User.objects.get(id=pk)

	rooms = user.room_set.all()
	room_messages = user.message_set.all()
	topics = Topic.objects.all()
	context = {"user": user, "rooms": rooms, "room_messages": room_messages, "topics": topics}

	return render(request, "base/profile.html", context)


@login_required(login_url='/login')
def create_room(request):
	# Creating RoomForm object which has model ready for form input
	form = RoomForm()
	topics = Topic.objects.all()

	# If request method is "POST" means form is submitted
	if request.method == "POST":
		topic_name = request.POST.get("topic")
		# It will take all obj and check if name is in topic & if not then will create it's obj
		# If name is found then created value will be falsed
		topic, created = Topic.objects.get_or_create(name=topic_name)
		# Then pass all the data received as response of our request of post methord and pass it to RoomForm in the form on dictionary

		Room.objects.create(
			host=request.user,
			topic=topic,
			name=request.POST.get('name'),
			description=request.POST.get('description')
		)
		return redirect("home")

	context = {'form': form, "topics": topics}
	return render(request, "base/room_form.html", context)

	# form = RoomForm(request.POST)
	# if form.is_valid:
	#     # After hiding form fields we will just create an instance of room where host is not specified
	#     room = form.save(commit=False)
	#     # And then set the host value externally
	#     room.host = request.user
	#     # Save data if form is valid and redirect user to home page
	#     room.save()


# It is a decorater which checks if user is not authenticated their session ID isn't in browser they will be redirected to login page(we can choose) 
@login_required(login_url='/login')
def update_room(request, pk):
	# Get hold on the room you want to update
	room = Room.objects.get(id=pk)
	topics = Topic.objects.all()

	# Send the form to fill which will be the instance of the room object we are updating currently
	form = RoomForm(instance=room)
	# IF the value(key) doesn't match then form won't be submitted

	# Anyone should not be able to update room if not loged in
	if request.user != room.host:
		return HttpResponse("You're not allowed here ..!")

	if request.method == 'POST':
		topic_name = request.POST.get("topic")
		# It will take all obj and check if name is in topic & if not then will create it's obj
		# If name is found then created value will be falsed
		topic, created = Topic.objects.get_or_create(name=topic_name)
		# Then pass all the data received as response of our request of post methord and pass it to RoomForm in the form on dictionary
		room.name = request.POST.get("name")
		room.topic = topic
		room.description = request.POST.get("description")
		room.save()

		return redirect("home")

	context = {'form': form, "topics": topics, "room": room}

	return render(request, "base/room_form.html", context)


@login_required(login_url='/login')
def delete_room(request, pk):
	# Fetch room object you want to delete as per passed parameter in url(pk)
	room = Room.objects.get(id=pk)
	context = {"obj": room}

	if request.user != room.host:
		return HttpResponse("You're not allowed here ..!")

	if request.method == "POST":
		# If request method is post delete the room and redirect to home page
		room.delete()
		return redirect("home")

	# pass the room object to page which has to be deleted
	return render(request, "base/delete.html", context)


@login_required(login_url='/login')
def delete_message(request, pk):
	# Fetch message object you want to delete as per passed parameter in url(pk)
	message = Message.objects.get(id=pk)
	context = {"obj": message}

	if request.user != message.user:
		return HttpResponse("You're not allowed here ..!")

	if request.method == "POST":
		# If request method is post delete the message and redirect to home page
		message.delete()
		return redirect("home")

	# pass the message object to page which has to be deleted
	return render(request, "base/delete.html", context)


@login_required(login_url="login")
def update_user(request):
	"""Page for user profile update"""

	user = request.user
	form = UserForm(instance=user)

	if request.method == "POST":
		form = UserForm(request.POST, instance=user)
		if form.is_valid():
			form.save()
			return redirect("user-profile", pk=user.id)

	context = {"form": form}

	return render(request, 'base/update-user.html', context)


def show_topics(request):
	"""FOR Mobile responsive Will fetch the data from url inside q
	and if q doesn't match any data then return empty string"""

	# Currently redirecting and using home search of room not these one !!!
	q = request.GET.get("q") if request.GET.get('q') != None else " "

	# topics = Topic.objects.filter(name__icontains=q)
	topics = Topic.objects.filter()
	context = {"topics": topics}

	return render(request, "base/topics.html", context)


def activities(request):
	room_messages = Message.objects.all()

	return render(request, 'base/activity.html', {"room_messages": room_messages})
