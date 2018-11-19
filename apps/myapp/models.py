from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.db import models 
import bcrypt
import re
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]*$')

class UserManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}
		#first names
		if len(postData['first_name']) < 1:
			errors['first_name'] = "*Name field must be at least 2 characters long"
		elif not NAME_REGEX.match(postData['first_name']):
			errors['first_name'] = "*Name must not contain special characters or numbers"
		#last names
		if len(postData['last_name']) < 1:
			errors['last_name'] = "*Name field must be at least 2 characters long"
		elif not NAME_REGEX.match(postData['last_name']):
			errors['last_name'] = "*Name must not contain special characters or numbers"
		#Email
		if not EMAIL_REGEX.match(postData['email']):
			errors['email'] = "*Email must be in email format"
		elif User.objects.filter(email = postData['email']):
			errors['email'] = "*Email is already in the database"
		#Password
		if len(postData['password']) < 7:
			errors['password'] = "*Password must be atleast 8 character long"
		elif postData['password_confirmation'] != postData['password']:
			errors['password'] = "*Password and Password Confirmation fields do not match"

		return errors

	def login_validator(self, postData):
		errors = {}

		if User.objects.filter(email = postData['email_log']):
			user = User.objects.get(email = postData['email_log'])

		else: 
			errors['email_log'] = "*Email is not in the database"
			return errors

		if not bcrypt.checkpw(postData['password_log'].encode(), user.password.encode()):
			errors['password_log'] = "*Email and password do not match"

		return errors
class TripManager(models.Manager):
	def trip_validator(self, postData):
		errors= {}

		if not postData['destination']:
			errors['destination'] = "Destination Field cannot be blank"

		if not postData['description']:
			errors['description'] = "Description Field cannot be blank"

		if not postData['travel_start']:
			errors['travel_start'] = "Travel Date From Field cannot be blank"

		elif postData['travel_start'] < str(datetime.datetime.now()):
			errors['travel_start'] = "Travel Date has to be in the future"

		if not postData['travel_end']:
			errors['travel_end'] = "Travel Date To Field cannot be blank"

		elif postData['travel_end'] < postData['travel_start']:
			errors['travel_start'] = "Travel Date End has cannot be before the Travel Start"

		return errors

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email= models.CharField(max_length=255)
	password= models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	# uploaded_trip : One to many (Trip)

	objects = UserManager()

class Trip(models.Model):
	destination = models.CharField(max_length=255)
	startDate = models.DateField()
	endDate = models.DateField()
	plan = models.CharField(max_length=255)
	guests = models.ManyToManyField(User, related_name="trips")
	uploader = models.ForeignKey(User, related_name="uploaded_trip")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	#guests : One to many(User)
	objects = TripManager()


