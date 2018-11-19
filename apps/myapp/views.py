from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
	request.session.clear()
	return render(request, "myapp/index.html")

def create(request):
	errors = User.objects.basic_validator(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.add_message(request, messages.ERROR, value, extra_tags='register')
		return redirect('/')
	else:
		password = request.POST['password']
		password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		User.objects.create(first_name= request.POST['first_name'], last_name = request.POST['last_name'], email= request.POST['email'], password= password)
		request.session['email'] = request.POST['email']
		request.session['user_id'] = User.objects.get(email= request.POST['email']).id 
	return redirect('/logged')

def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.add_message(request, messages.ERROR, value, extra_tags= "login")
		return redirect('/')
	else: 
		request.session['email'] = request.POST['email_log']
		request.session['user_id'] = User.objects.get(email= request.POST['email_log']).id 

	return redirect('/logged')

def logged(request):
	if 'user_id' not in request.session:
		return redirect('/')
	else:
		other_trips =[]
		all_trips = Trip.objects.all()
		mytrips = User.objects.get(id=request.session['user_id']).trips.all()
		print(mytrips)
		for trip in all_trips:
			if trip not in mytrips:
				other_trips.append(trip)
		print(other_trips)
		context = {
		"trips": other_trips,
		"user" : User.objects.get(id= request.session['user_id']),
		"mytrips" : mytrips
		}
		return render(request, 'myapp/logged.html', context) 

def addplan(request):
	if 'user_id' not in request.session:
		return redirect('/')
	else:
		return render(request, 'myapp/addplan.html')

def maketrip(request):
	errors = Trip.objects.trip_validator(request.POST)
	if errors:
		for key, error in errors.items():
			messages.add_message(request, messages.ERROR, error)
		print(errors)
		return redirect('/addplan')
	else:
		trip =Trip.objects.create(destination= request.POST['destination'],startDate= request.POST['travel_start'], endDate= request.POST['travel_end'], plan = request.POST['description'], uploader_id= request.session["user_id"])
		trip.guests.add(User.objects.get(id=request.session['user_id']))
		return redirect('/logged')

def destination(request, tripid):
	trip = Trip.objects.get(id=tripid)
	print(trip)
	context = {
	"trip": trip,
	"users": trip.guests.all()
	}
	print(trip.guests.all())
	return render(request, "myapp/destination.html", context)

def join(request, tripid):
	trip = Trip.objects.get(id=tripid)
	trip.guests.add(User.objects.get(id=request.session['user_id']))
	return redirect('/logged')



