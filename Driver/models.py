from django.db import models
import datetime
from django.contrib.auth.models import User, Group

class new_model(models.Model):
	test = models.CharField(max_length=100, default="")

class Car(models.Model):
	make = models.CharField(max_length=200, default="")
	model = models.CharField(max_length=200, default="")
	year = models.IntegerField(default=0)
	id_num = models.IntegerField(default=0)
	name = models.CharField(max_length=200, default="")
	temporary = models.BooleanField(default=False)
	selected = models.BooleanField(default=False)

class Driver(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, default="")
	cars = models.ManyToManyField("Car")
	current_car_id = models.IntegerField(default=0)
	email = models.CharField(max_length=200, default="")
	current_service_key = models.IntegerField(default=1)
	requests = models.ManyToManyField("Request")
	current_request_id = models.IntegerField(default=1)
	phone_number = models.IntegerField(default=0)
	address = models.CharField(max_length=300, default="")

class Dispatch(models.Model):
	company = models.CharField(max_length=200, default="")
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	requests = models.ManyToManyField("Request")
	consecutive_requests = models.IntegerField(default=0)
	last_request_time = models.DateTimeField(auto_now=True)

class Service(models.Model):
	name = models.CharField(max_length=200, default="")
	cost = models.IntegerField(default = 0)
	estimated_time = models.CharField(max_length=200, default="")
	provider = models.CharField(max_length=200, default="")
	id_num = models.IntegerField(default=1)
	description = models.CharField(max_length=500, default="")

class Contact(models.Model):
	email = models.CharField(max_length=200, default="")
	phone_number = models.CharField(max_length=200, default="")	

class Request(models.Model):
	id_num = models.IntegerField(default=0)
	service = models.CharField(max_length=200, default="")
	cost = models.IntegerField(default = 0)
	initial_ETA = models.CharField(max_length=200, default="")
	time_created = models.DateTimeField(auto_now_add=True)
	provider = models.CharField(max_length=200, default="")
	requester = models.CharField(max_length=200, default="")
	confirmed = models.BooleanField(default=False)
	car = models.OneToOneField(Car, default="", null=True, blank=True)
	car_info = models.CharField(max_length=200, default="")
	contact = models.OneToOneField(Contact, default="", null=True, blank=True)
#	REQUEST INFORMATION	
	flat_tires = models.CharField(max_length=200, default="")
	message = models.CharField(max_length=1000, default="")
	in_ditch = models.BooleanField(default=False)
	accident = models.BooleanField(default=False)
	claimed = models.BooleanField(default=False)
	time_claimed = models.DateTimeField(auto_now_add=True)
	completed = models.BooleanField(default=False)
	# payment = models.OneToOneField("PaymentInfo")

class PaymentInfo (models.Model):
	cardholder_name = models.CharField(max_length=200, default="")
	billing_address = models.CharField(max_length=200, default="")
	city_state_zip = models.CharField(max_length=200, default="")
	card_number = models.IntegerField(default=0)
	expiry_date = models.IntegerField(default=0)
	security_code = models.IntegerField(default=0)


class Repair_Shop(models.Model):
	provider = models.CharField(max_length=200, default="")







	




