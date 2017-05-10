import datetime
from django.shortcuts import render
from .models import Car, Driver, Service, Request, Repair_Shop, Dispatch, Contact
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import logout, login, authenticate


def Logout(request):
	logout(request)
	return HttpResponseRedirect("/login")

def Driver_Check(user):
	if (user.is_active):
		return Driver.objects.filter(user=user).exists()
	else:
		return False

def Login(request):
	user = request.user
	print(user.username)
	print("LOGIN TEST")
	# if (Driver_Check(user)):
	# 	print("Driver EXISTS")
	context = {}
	if(request.POST.get("login_btn")):
		print("login button pressed")
		u_name = request.REQUEST.get("username")
		p_word = request.REQUEST.get("password")
		if (u_name == "") or (p_word == ""):
			context["Empty_Input"] = "Please fill in all required form fields"
		if User.objects.filter(username=u_name).exists():
			print("user exists")
			user = User.objects.get(username=u_name)
			user.is_active = True
			user.save()
			print("user is active")
			auth = authenticate(username=u_name, password=p_word)
			print(auth)
			if auth and Driver_Check(user):
				print("authenticated")
				user.save()
				login(request, auth)
				user.save()
				print("LOGIN SUCCESS")
				print(request.user.username)
				username = request.user.username
				user = User.objects.get(username=username)
				print("AUTH")				
				return HttpResponseRedirect('/home/')
		else: 
				return HttpResponseRedirect('/')
	if request.GET.get("go_to_create_account"):
		return HttpResponseRedirect('/signup/')
	return render(request, "Login_Frame.html", context)

def SignUp(request):
	context = {}
	if request.POST.get("create_account"):
		print("TEST")
		f_name = request.REQUEST.get("first_name")
		l_name = request.REQUEST.get("last_name")
		email = request.REQUEST.get("email")
		number = request.REQUEST.get("number")
		p_1 = request.REQUEST.get("p_word")
		p_2 = request.REQUEST.get("p_word_2")
		print("Create Account Button Pressed")
		if (p_1 == p_2 and f_name != "" and l_name != "" and email != "" and p_1 != "" ):
			print("Test")
			new_user = User.objects.create(username=email, first_name=f_name, last_name=l_name, password=p_1)
			new_user.save()
			new_user.set_password(p_1)
			new_user.is_active = True
			new_user.save()
			new_driver = Driver(user=new_user)
			new_driver.phone_number = number
			new_driver.save()
			auth = authenticate(username=email, password=p_1)
			if auth:
				new_user.save()
				login(request, auth)
				return HttpResponseRedirect("/home")
		else:
			context["Empty_Input"] = "Please fill in all required form fields"
		if (p_1 != p_2):
			context["PWord_Error"] = "Passwords don't match"
	return render(request, "Create_Profile_Frame.html", context)

def Ref_Dict(user):
	output = {}
	if Driver.objects.filter(user=user).exists():
		driver = Driver.objects.get(user=user)
		for i in driver.cars.all():
			# if i.id_num == driver.current_car_id:
			# 	output["Current Car"] = i 
			if i.selected == True:
				output["Current Car"] = i
		# for i in Service.objects.all():
		# 	print(i.id_num)
		# print("Driver current service key: " + str(driver.current_service_key))
		output["Current Service"] = Service.objects.get(id_num = driver.current_service_key)
		output["Cars"] = driver.cars.all()
		output["Driver"] = driver
		output["Requests"] = driver.requests.all()
	return output

@user_passes_test(Driver_Check)
def Home(request):	
	tow_truck = Service.objects.get(id_num = 1)
	# tow_truck = Service(id_num=1, name="Tow Service", cost=50, estimated_time="30 minutes")
	tow_truck.description = "Description for Tow Truck service"
	tow_truck.save()

	flat_tire = Service.objects.get(id_num = 2)
	# flat_tire = Service(id_num=2, name="Flat Tire", cost=30, estimated_time="20 minutes")
	flat_tire.description = "Description for Flat Tire service"
	flat_tire.save()

	lockout = Service.objects.get(id_num = 3)
	# lockout = Service(id_num=3, name="Lockout", cost=15, estimated_time="10 minutes")
	lockout.description = "Description for Lockout Service"
	lockout.save()

	jump_start = Service.objects.get(id_num = 4)
	# jump_start = Service(id_num=4, name="Jump Start", cost=40, estimated_time="20 minutes")
	jump_start.description = "Description for Jump Start service"	
	jump_start.save()

	gas_service = Service.objects.get(id_num = 5)
	# gas_service = Service(id_num=5, name="Gas Service", cost=20, estimated_time="30 minutes")
	gas_service.description = "Description for Gas Service"
	gas_service.save()

	context = {}
	context["Car_Names"] = []
	user = request.user	
	ref_dict = Ref_Dict(user)
	if (user.is_anonymous() == False):
		driver = Driver.objects.get(user=user)
	driver = ref_dict["Driver"]	
	for i in Service.objects.all():
		print(i.id_num)
	current_service = ref_dict["Current Service"]
	requests = ref_dict["Requests"]

	if driver.cars.count() == 0:
		context["No_Cars"] = ["You have no cars associated with this account"]

	for i in driver.cars.all():
		if i.temporary == True:
			driver.cars.remove(i)
			driver.save()
			i.delete()
		else:
			if i.selected == True:
				i.selected == False
			row = []
			row.append(i.name) #0 is name
			row.append(i.pk) #1 is pkid
			context["Car_Names"].append(row)

	for i in driver.requests.all():
		if i.confirmed == False:
			driver.requests.remove(i)
			driver.save()
			i.delete()

	if request.GET.get("Tow_select_car") or request.GET.get("Tow_info_car"):
		driver.current_service_key = 1 #1 is Oil Change
		driver.save()
		current_service = Service.objects.get(id_num = 1)
		if request.GET.get("Tow_select_car"):
			print("Test")
			selected_id = request.REQUEST.get("selected_car_tow")
			print(selected_id)
			
			if (selected_id == "no_cars"):
				context["No_Car_Error"] = "You need to select a car or add your car information!"
				return render(request, "E_Home_Frame.html", context)

			for i in driver.cars.all():
				print(str(i.pk) + " " + str(selected_id))			
				print(i.pk == selected_id)
				if str(i.pk) == str(selected_id):
					driver.current_car_id = selected_id
					i.selected = True
					i.save()
					driver.current_car_id = i.pk
#					NEW REQUEST			
					new_request = Request(requester=driver.user.username, service=current_service.name, cost=current_service.cost)
					new_request.save()
					driver.requests.add(new_request)
					driver.save()

		if request.GET.get("Tow_info_car"):
			driver.current_service_key = 1 #2 is Flat Tire
			print(driver.current_service_key)
			driver.save()
			temp_car_make = request.REQUEST.get("make")
			temp_car_model = request.REQUEST.get("model")
			temp_car_year = request.REQUEST.get("year")
			print(temp_car_make)
			print(temp_car_model)
			print(temp_car_year)			
# 			NEW TEMP CAR
			temp_car = Car(make=temp_car_make, model=temp_car_model, year=temp_car_year, id_num=0, name=temp_car_make + " " + temp_car_model)
			print(temp_car.name)
			temp_car.temporary = True;			
			temp_car.selected = True;
			temp_car.save()
			driver.cars.add(temp_car)
			driver.current_car_id = 0
			driver.save()
#			NEW REQUEST			
			new_request = Request(requester=driver.user.username, service=current_service.name, 
							cost=current_service.cost, time_created = datetime.datetime.now())
			new_request.save()
			driver.requests.add(new_request)
			driver.save()			
		return HttpResponseRedirect('/service-tow')

	if request.GET.get("FT_select_car") or request.GET.get("FT_info_car"):
		print("Flat Tire Selected")
		driver.current_service_key = 2 #2 is Flat Tire
		print(driver.current_service_key)
		driver.save()
		if request.GET.get("FT_select_car"):
			print("Test")
			selected_id = request.REQUEST.get("selected_car_FT")
			print(selected_id)
			if (selected_id == "no_cars"):
				context["No_Car_Error"] = "You need to select a car or add your car information!"
				return render(request, "E_Home_Frame.html", context)			
			for i in driver.cars.all():
				print(str(i.pk) + " " + str(selected_id))			
				print(i.pk == selected_id)
				if str(i.pk) == str(selected_id):
					driver.current_car_id = selected_id
					i.selected = True
					i.save()
					driver.current_car_id = i.pk
#					NEW REQUEST			
					new_request = Request(requester=driver.user.username, service=current_service.name, cost=current_service.cost)
					new_request.save()
					driver.requests.add(new_request)
					driver.save()
					print("success test")
		if request.GET.get("FT_info_car"):
			driver.current_service_key = 2 #2 is Flat Tire
			print(driver.current_service_key)
			driver.save()
			temp_car_make = request.REQUEST.get("make")
			temp_car_model = request.REQUEST.get("model")
			temp_car_year = request.REQUEST.get("year")
			print(temp_car_make)
			print(temp_car_model)
			print(temp_car_year)			
#			NEW TEMP CAR
			temp_car = Car(make=temp_car_make, model=temp_car_model, year=temp_car_year, id_num=0, name=temp_car_make + " " + temp_car_model)
			print(temp_car.name)
			temp_car.temporary = True;
			temp_car.selected = True;
			temp_car.save()
			driver.cars.add(temp_car)
			driver.current_car_id = 0
			driver.save()			
#			NEW REQUEST			
			new_request = Request(requester=driver.user.username, service=current_service.name, 
							cost=current_service.cost, time_created = datetime.datetime.now())
			new_request.save()
			driver.requests.add(new_request)
			driver.save()
		return HttpResponseRedirect('/service-flat')

	if request.GET.get("L_select_car") or request.GET.get("L_info_car"):
		driver.current_service_key = 3 #3 is Lockout
		driver.save()

		if request.GET.get("L_select_car"):
			selected_id = request.REQUEST.get("selected_car_L")
			if (selected_id == "no_cars"):
				context["No_Car_Error"] = "You need to select a car or add your car information!"
				return render(request, "E_Home_Frame.html", context)			
			for i in driver.cars.all():
				print(str(i.pk) + " " + str(selected_id))			
				print(i.pk == selected_id)
				if str(i.pk) == str(selected_id):
					driver.current_car_id = selected_id
					i.selected = True
					i.save()
					driver.current_car_id = i.pk
#					NEW REQUEST			
					new_request = Request(requester=driver.user.username, service=current_service.name, cost=current_service.cost)
					new_request.save()
					driver.requests.add(new_request)
					driver.save()

		if request.GET.get("L_info_car"):
			driver.current_service_key = 3 #3 is Flat Tire
			print(driver.current_service_key)
			driver.save()
			temp_car_make = request.REQUEST.get("make")
			temp_car_model = request.REQUEST.get("model")
			temp_car_year = request.REQUEST.get("year")
			print(temp_car_make)
			print(temp_car_model)
			print(temp_car_year)			
#			NEW TEMP CAR
			temp_car = Car(make=temp_car_make, model=temp_car_model, year=temp_car_year, id_num=0, name=temp_car_make + " " + temp_car_model)
			print(temp_car.name)
			temp_car.temporary = True;
			temp_car.selected = True;
			temp_car.save()
			driver.cars.add(temp_car)
			driver.current_car_id = 0
			driver.save()			
#			NEW REQUEST			
			new_request = Request(requester=driver.user.username, service=current_service.name, 
							cost=current_service.cost, time_created = datetime.datetime.now())
			new_request.save()
			driver.requests.add(new_request)
			driver.save()
		return HttpResponseRedirect('/service-details')

	if request.GET.get("JS_select_car") or request.GET.get("JS_info_car"):
		driver.current_service_key = 4 #4 is Jump Start
		driver.save()
		if request.GET.get("JS_select_car"):
			selected_id = request.REQUEST.get("selected_car_JS")
			if (selected_id == "no_cars"):
				context["No_Car_Error"] = "You need to select a car or add your car information!"
				return render(request, "E_Home_Frame.html", context)			
			for i in driver.cars.all():
				print(str(i.pk) + " " + str(selected_id))			
				print(i.pk == selected_id)
				if str(i.pk) == str(selected_id):
					driver.current_car_id = selected_id
					i.selected = True
					i.save()
					driver.current_car_id = i.pk
#					NEW REQUEST			
					new_request = Request(requester=driver.user.username, service=current_service.name, cost=current_service.cost)
					new_request.save()
					driver.requests.add(new_request)
					driver.save()

		if request.GET.get("JS_info_car"):
			print(driver.current_service_key)
			driver.save()
			temp_car_make = request.REQUEST.get("make")
			temp_car_model = request.REQUEST.get("model")
			temp_car_year = request.REQUEST.get("year")
			print(temp_car_make)
			print(temp_car_model)
			print(temp_car_year)			
#			NEW TEMP CAR 
			temp_car = Car(make=temp_car_make, model=temp_car_model, year=temp_car_year, id_num=0, name=temp_car_make + " " + temp_car_model)
			print(temp_car.name)
			temp_car.temporary = True;
			temp_car.selected = True;									
			temp_car.save()

			driver.cars.add(temp_car)
			driver.current_car_id = 0
			driver.save()

			new_request = Request(requester=driver.user.username, service=current_service.name, 
							cost=current_service.cost, time_created = datetime.datetime.now())
			new_request.save()
			driver.requests.add(new_request)
			driver.save()			
		return HttpResponseRedirect('/service-details')

	if request.GET.get("GS_select_car") or request.GET.get("GS_info_car"):
		driver.current_service_key = 5 #5 is Gas Service
		driver.save()
		if request.GET.get("GS_select_car"):
			selected_id = request.REQUEST.get("GS_car")
			if (selected_id == "no_cars"):
				context["No_Car_Error"] = "You need to select a car or add your car information!"
				return render(request, "E_Home_Frame.html", context)			
			for i in driver.cars.all():
				print(str(i.pk) + " " + str(selected_id))			
				print(i.pk == selected_id)
				if str(i.pk) == str(selected_id):
					driver.current_car_id = selected_id
					i.selected = True
					i.save()
					driver.current_car_id = i.pk
#					NEW REQUEST			
					new_request = Request(requester=driver.user.username, service=current_service.name, cost=current_service.cost)
					new_request.save()
					driver.requests.add(new_request)
					driver.save()
					
		if request.GET.get("GS_info_car"):
			print(driver.current_service_key)
			driver.save()
			temp_car_make = request.REQUEST.get("make")
			temp_car_model = request.REQUEST.get("model")
			temp_car_year = request.REQUEST.get("year")
			print(temp_car_make)
			print(temp_car_model)
			print(temp_car_year)			
#			NEW TEMP CAR 
			temp_car = Car(make=temp_car_make, model=temp_car_model, year=temp_car_year, id_num=0, name=temp_car_make + " " + temp_car_model)
			print(temp_car.name)
			temp_car.temporary = True;
			temp_car.selected = True;			
			temp_car.save()

			driver.cars.add(temp_car)
			driver.current_car_id = 0
			driver.save()

			new_request = Request(requester=driver.user.username, service=current_service.name, 
							cost=current_service.cost, time_created = datetime.datetime.now())
			new_request.save()
			driver.requests.add(new_request)
			driver.save()	
		return HttpResponseRedirect('/service-details')
	return render(request, "E_Home_Frame.html", context)

def ReturnHome(request):
	user = request.user
	ref_dict = Ref_Dict(user)
	driver = ref_dict["Driver"]
	current_car = ref_dict["Current Car"]
	if current_car.temporary == True:
		driver.cars.remove(current_car)
		driver.save()
		current_car.delete()
	return HttpResponseRedirect('/home')

@user_passes_test(Driver_Check)
def ServiceDetails(request):	
	context = {}
	user = request.user
	ref_dict = Ref_Dict(user)
	driver = ref_dict["Driver"]
	current_car = ref_dict["Current Car"]
	current_service = ref_dict["Current Service"]
	#Need: cost, ETA, provider
	#provider and ETA based on location and time, which will be collected from home and assigned to user
	context["Service_Name"] = current_service.name
	context["Cost"] = current_service.cost
	context["Car_Name"] = current_car.name
	context["ETA"] = current_service.estimated_time

	for i in driver.requests.all():
		if i.confirmed == False:
			current_request = i

	if request.GET.get("to_payment_btn"):
		print("payment button hit")
		current_request.time_created = datetime.datetime.now()
		current_request.confirmed = False
		current_request.save()
		driver.save()
		return HttpResponseRedirect("/service-payment")

	# if request.GET.get("service_payment_btn"):
	return render(request, "Service_Details_Frame.html", context)	

@user_passes_test(Driver_Check)
def ServiceTow (request):
	context = {}
	user = request.user
	ref_dict = Ref_Dict(user)
	driver = ref_dict["Driver"]
	current_car = ref_dict["Current Car"]
	current_service = ref_dict["Current Service"]

	for i in driver.requests.all():
		if i.confirmed == False:
			current_request = i

	if request.GET.get("to_details_btn"):
		ditch_answer = request.REQUEST.get("ditch")
		print("Ditch answer: " + ditch_answer)
		if (ditch_answer == "Yes"):
			current_request.in_ditch = True
			current_request.save()
		accident_answer = request.REQUEST.get("accident")
		print("Accident answer: " + accident_answer)
		if (accident_answer == "Yes"):
			current_request.accident = True
			current_request.save()
		#code to save information here
		return HttpResponseRedirect("/service-details")
	return render(request, "Tow_Service_Frame.html", context)

@user_passes_test(Driver_Check)
def ServiceFlat (request):
	context = {}
	user = request.user
	ref_dict = Ref_Dict(user)
	driver = ref_dict["Driver"]
	current_car = ref_dict["Current Car"]
	current_service = ref_dict["Current Service"]
	
	for i in driver.requests.all():
		if i.confirmed == False:
			current_request = i	

	if request.GET.get("to_details_btn"):
		ditch_answer = request.REQUEST.get("ditch")
		print("Ditch answer: " + ditch_answer)
		if (ditch_answer == "Yes"):
			current_request.in_ditch = True
			current_request.save()

		accident_answer = request.REQUEST.get("accident")
		print("Accident answer: " + accident_answer)
		if (accident_answer == "Yes"):
			current_request.accident = True
			current_request.save()

		tire_list = request.GET.getlist("select_tire")
		for i in tire_list:
			current_request.flat_tires = current_request.flat_tires + i + ", "
			current_request.save()
			#code to save information here
		return HttpResponseRedirect("/service-details")

	return render(request, "Flat_Tire_Frame.html", context)

@user_passes_test(Driver_Check)
def ServiceCar(request):
	context = {}
	user = request.user
	ref_dict = Ref_Dict(user)
	driver = ref_dict["Driver"]
	current_car = ref_dict["Current Car"]
	current_service = ref_dict["Current Service"]
	return render(request, "Service_Car_Frame.html")

@user_passes_test(Driver_Check)
def ServicePayment(request):
	context = {}
	user = request.user
	ref_dict = Ref_Dict(user)
	driver = ref_dict["Driver"]
	current_car = ref_dict["Current Car"]
	current_service = ref_dict["Current Service"]	
	for i in driver.requests.all():
		if i.confirmed == False:
			current_request = i
	# current_service.cost = 50.00
	context["Service_Name"] = current_service.name
	context["Cost"] = current_service.cost
	context["Car_Name"] = current_car.name
	context["ETA"] = current_service.estimated_time
	service_total = current_service.cost + 20 #arbitrary right now
	context["Total"] = service_total
	
	#if request.GET.get("save_car_btn"):
	#	current_car.temporary = false
	#	current_car.save()
	#	driver.save()
	if request.POST.get("payment_btn"):
		current_request.confirmed = True
		current_request.car_info = current_car.name + " " + str(current_car.year)
		current_request.save()

		cardholder_name = request.REQUEST.get("payment_name")
		billing_address = request.REQUEST.get("payment_address")
		city_state_zip = request.REQUEST.get("city_state_zip")
		card_number = request.REQUEST.get("card_number")
		expiry_date = request.REQUEST.get("expiry_date")
		security_code = request.REQUEST.get("security_code")

		if (cardholder_name == "" or billing_address == "" or city_state_zip == "" or 
			card_number == "" or expiry_date == "" or security_code == ""):
			context["Empty_Input"] = "Please fill in all required form fields"

		driver.requests.add(current_request)
		driver.current_request_id = current_request.pk
		driver.save()
		#add new PaymentInfo here
		#assign to current request
#		current_request.payment = newpaymentinfo
		return HttpResponseRedirect("/service-receipt")

	return render(request, "Service_Payment_Frame.html", context)	

@user_passes_test(Driver_Check)
def ServiceReceipt(request):
	context = {}
	user = request.user
	ref_dict = Ref_Dict(user)
	driver = ref_dict["Driver"]
	current_car = ref_dict["Current Car"]
	current_service = ref_dict["Current Service"]

	context["Service_Name"] = current_service.name
	context["Cost"] = current_service.cost
	context["Car_Name"] = current_car.name
	context["ETA"] = current_service.estimated_time
	context["Details"] = current_service.description 

	current_request = Request.objects.get(pk=driver.current_request_id)
	# need service details, provider details, eta and location for google maps
	# 	also contact information of two truck driver
	# 	delete current service after transaction is completed?
	if request.GET.get("add_message_btn"):
		message = request.REQUEST.get("message_text")
		print(message)
		current_request.message = current_request.message + " " + message
		current_request.save()
		if message != "":
			context["Message_Received"] = "Your message has been sent!"
		else:
			context["Message_Received"] = "Please include some text in your message body!"
		# return HttpResponseRedirect("/service-receipt")

	if request.GET.get("return_home_btn"):
		return HttpResponseRedirect("/home")
	return render(request, "Confirmation_Frame.html", context)	


def RequestDisplay(request):
	context = {}
	context["Requests"] = [["Service Type: ", 
	", Requester: ", 
	", In_Ditch: " + str(False), 
	", Accident: " + str(False), 
	", Message: " + str(False), 
	", Tires_Flat: " + str(False), 
	", ID_num: "]]
	for i in Request.objects.all():
		row = []
		row.append("Service Type: " + i.service)
		row.append(", Requester: " + i.requester)
		row.append(", Time_Created: " + str(i.time_created))
		row.append(", In_Ditch: " + str(i.in_ditch))
		row.append(", Accident: " + str(i.accident))
		row.append(", Message: " + i.message)
		row.append(", Tires_Flat: " + i.flat_tires)
		row.append(", ID_num: " + str(i.pk))
		context["Requests"].append(row)

	return render(request, "Request_Display.html", context)	

@user_passes_test(Driver_Check)
def AddCar(request):
	user = request.user	
	# driver = Driver.objects.get(user=user)
	ref_dict = Ref_Dict(user)
	driver = ref_dict["Driver"]
	current_service = ref_dict["Current Service"]
	context = {}
	# print("Car Count: " + str(driver.cars.all().count()))
	if request.GET.get("add_car_btn"):
		if driver.cars.count() == 3:
			context["Too_Many"] = "You already have 3 cars in your profile! Delete one before you add another"
			return render(request, "Add_Car_Frame.html", context)
		new_car_make = request.GET.get("make")
		new_car_model = request.GET.get("model")
		new_car_year = request.GET.get("year")
		if (new_car_make == "") or (new_car_model == "") or (new_car_year == ""):
			context["Empty_Input"] = "Please input something in all fields"
			return render(request, "Add_Car_Frame.html", context)

		new_car = Car(make = new_car_make, model=new_car_model, year=new_car_year, name=new_car_make + " " + new_car_model)
		new_car.save()
		context["car_added"] = "Car Added! You can store up to 3 cars in your profile."
		print("new car make: " + new_car.make)
		driver.cars.add(new_car)
		# new_car.id_num = driver.cars.all().index(new_car)
		new_car.save()
		driver.save()
		return HttpResponseRedirect('/add-car')
		# Driver.cars.add(new_car)
		# Driver.save()
	return render(request, "Add_Car_Frame.html", context)

@user_passes_test(Driver_Check)
def Profile(request):
	user = request.user
	ref_dict = Ref_Dict(user)
	# output["Current Car"] 
	# output["Current Service"] = Service.objects.get(id_num = driver.current_service_key)
	# output["Cars"] = driver.cars.all()
	driver = ref_dict["Driver"]

	context = {}
	context["First_Name"] = user.first_name	
	context["Last_Name"] = user.last_name
	context["Name"] = user.first_name + " " + user.last_name
	context["Email"] = user.username
	context["Address"] = "145 Test Street, Chicago IL 60615"
	context["Number"] = driver.phone_number
	context["Car_Names"] = []

	for i in driver.cars.all():
		row = []
		row.append(i.name) #0 is name
		row.append(i.pk) #1 is pkid
		context["Car_Names"].append(row)
	# output["Driver"] = driver
	cars = ref_dict["Cars"]
	context["Cars"] = []
	count = 0
	for i in cars:
		count = count + 1
		car_context = []
		car_context.append(i.make + " " + i.model) #0 is name
		car_context.append(i.make) #1 is make
		car_context.append(i.model) #2 is model
		car_context.append(i.year) #3 is year
		# car_context.append(cars.index(i)) #4 is index
		context["Cars"].append(car_context)

	if not (driver.cars.all()):
		context["No_Cars"] = ["No Cars Added"]

	if request.GET.get("remove_car_btn"):
		print("Test")
		selected_id = request.REQUEST.get("selected_car")
		print(selected_id)
		for i in driver.cars.all():
			print(str(i.pk) + " " + str(selected_id))			
			print(i.pk == selected_id)
			if str(i.pk) == str(selected_id):
				print("delete this car")
				driver.cars.remove(i)
				i.delete()
		return HttpResponseRedirect('/profile')		

	if request.GET.get("add_car_btn"):
		if driver.cars.count() == 3:
			context["Too_Many"] = "You already have 3 cars in your profile! Delete one before you add another"
			return render(request, "Profile_Frame.html", context)
		make = request.REQUEST.get("make")
		model = request.REQUEST.get("model")
		year = request.REQUEST.get("year")
		new_car = Car(make=make, model=model, year=year)
		new_car.name = make + " " + model
		new_car.save()
		driver.cars.add(new_car)
		driver.save()
		return HttpResponseRedirect('/profile')

	if request.GET.get("edit_profile_btn"):
		return HttpResponseRedirect('/profile-edit')

	if request.GET.get("profile_requests_btn"):
		return HttpResponseRedirect('/profile-requests')

	return render(request, "Profile_Frame.html", context)

@user_passes_test(Driver_Check)
def ProfileEdit(request):
	user = request.user
	ref_dict = Ref_Dict(user)
	driver = ref_dict["Driver"]
	cars = ref_dict["Cars"]
	context = {}
	context["Cars"] = []
	context["First_Name"] = user.first_name
	context["Last_Name"] = user.last_name
	context["Name"] = user.first_name + " " + user.last_name
	context["Email"] = user.username
	context["Number"] = driver.phone_number

	for i in cars:
		car_context = []
		car_context.append(i.name) #0 is name
		car_context.append(i.make) #1 is make
		car_context.append(i.model) #2 is model
		car_context.append(i.year) #3 is year
		context["Cars"].append(car_context)

	if request.POST.get("edit_profile_btn"):
		print("test")
		print(request.REQUEST.get("new_email"))
		if request.REQUEST.get("new_email") != "":
			new_username = request.REQUEST.get("new_email")
			user.username = new_username
			user.save()
			print(new_username)
		if request.REQUEST.get("first_name") != "":
			new_fname = request.REQUEST.get("first_name")
			user.first_name = new_fname
			user.save()
		if request.REQUEST.get("last_name") != "":
			new_lname = request.REQUEST.get("last_name")
			user.last_name = new_lname
			user.save()
		if request.REQUEST.get("new_number") != "":
			new_number = request.REQUEST.get("new_number")
			driver.phone_number = new_number
			driver.save()			
		if request.REQUEST.get("p_word_1") != "" and request.REQUEST.get("p_word_1") == request.REQUEST.get("p_word_2"):
			user.set_password(request.REQUEST.get("p_word_1"))
			user.save()
		return HttpResponseRedirect('/profile-edit')

	if request.GET.get("add_car_btn"):
		if driver.cars.count() == 3:
			context["Too_Many"] = "You already have 3 cars in your profile! Delete one before you add another"
			return render(request, "Edit_Profile_Frame.html", context)
		new_car_make = request.GET.get("make")
		new_car_model = request.GET.get("model")
		new_car_year = request.GET.get("year")
		if (new_car_make == "") or (new_car_model == "") or (new_car_year == ""):
			context["Empty_Input"] = "Please input something in all fields"
			return render(request, "Edit_Profile_Frame.html", context)

		new_car = Car(make = new_car_make, model=new_car_model, year=new_car_year)
		new_car.save()
		driver.cars.add(new_car)
		driver.save()
		context["car_added"] = "Car Added! You can store up to 3 cars in your profile."
		print("new car make: " + new_car.make)

	if request.GET.get("remove_car_btn"):
		remove_car_id = request.GET.get("car_id") #item 4 in car context row (index of car in cars list)
		remove_car = driver.cars.all()[remove_car_id] #Link car_id to index in context
		driver.cars.remove(remove_car)
		driver.save()

	return render(request, "Edit_Profile_Frame.html", context)

@user_passes_test(Driver_Check)
def ProfileRequests(request):
	user = request.user
	ref_dict = Ref_Dict(user)
	driver = ref_dict["Driver"]
	cars = ref_dict["Cars"]
	context = {}
	context["Requests"] = []
	for i in driver.requests.all():
		row = []
		row.append(i.time_created) #0 is time
		row.append(i.service) #1 is service name
		row.append(i.cost) #2 is cost
		context["Requests"].append(row)
#FOR REFERENCE:
# if request.GET.get("to_payment_btn"):
# 		new_request = Request(requester=driver, service=current_service.name, cost=current_service.cost, time_created = datetime.datetime.now())
# 		new_request.save()
# 		driver.requests.add(new_request)
# 		driver.save()

	return render(request, "Profile_Requests_Frame.html", context)

@user_passes_test(Driver_Check)
def About(request):
	user = request.user
	print(Driver_Check(user))
	return render(request, "About_Frame.html")

@user_passes_test(Driver_Check)
def Support(request):
	return render(request, "Support_Frame.html")

#EMERGENCY MODE/ROADSIDE ASSISTANCE STARTS HERE
def E_Home(request):
	context = {}
	if ("Request_PK" in request.session):
		check_request = Request.objects.get(pk=request.session["Request_PK"])
		if check_request.confirmed == False:
			check_request.delete()
		request.session.pop("Request_PK")
	if ("Car_PK" in request.session):
		check_car = Car.objects.get(pk=request.session["Car_PK"])
		if check_car.temporary == True:
			check_car.delete()
		request.session.pop("Car_PK")

	if request.GET.get("Tow_info_car"):
		request.session["Service_Key"] = 1 #2 is Flat Tire
		current_service = Service.objects.get(id_num = 1)
		temp_car_make = request.REQUEST.get("make")
		temp_car_model = request.REQUEST.get("model")
		temp_car_year = request.REQUEST.get("year")
		if (temp_car_make == "" or temp_car_model == "" or temp_car_year == ""):
			context["Empty_Input"] = "Please fill in all required fields!"			
# 		NEW TEMP CAR
		temp_car = Car(make=temp_car_make, model=temp_car_model, year=temp_car_year, id_num=0, name=temp_car_make + " " + temp_car_model)
		print(temp_car.name)
		temp_car.temporary = True;			
		temp_car.selected = True;
		temp_car.save()
		request.session["Car_PK"] = temp_car.pk
		request.session["Car_Make"] = temp_car_make
		request.session["Car_Model"] = temp_car_model
		request.session["Car_Year"] = temp_car_year
#		NEW REQUEST			
		new_request = Request(service=current_service.name, cost=current_service.cost, time_created = datetime.datetime.now())
		new_request.car = temp_car
		new_request.save()
		request.session["Request_PK"] = new_request.pk
		return HttpResponseRedirect('/emergency-service-tow')

	if request.GET.get("FT_info_car"):
		request.session["Service_Key"] = 2 #2 is Flat Tire
		current_service = Service.objects.get(id_num = 2)
		temp_car_make = request.REQUEST.get("make")
		temp_car_model = request.REQUEST.get("model")
		temp_car_year = request.REQUEST.get("year")
		print(temp_car_make)
		print(temp_car_model)
		print(temp_car_year)			
# 		NEW TEMP CAR
		temp_car = Car(make=temp_car_make, model=temp_car_model, year=temp_car_year, id_num=0, name=temp_car_make + " " + temp_car_model)
		print(temp_car.name)
		temp_car.temporary = True;			
		temp_car.selected = True;
		temp_car.save()
		request.session["Car_Make"] = temp_car_make
		request.session["Car_Model"] = temp_car_model
		request.session["Car_Year"] = temp_car_year
#		NEW REQUEST			
		new_request = Request(service=current_service.name, cost=current_service.cost, time_created = datetime.datetime.now())
		new_request.car = temp_car
		new_request.save()
		request.session["Request_PK"] = new_request.pk
		return HttpResponseRedirect('/emergency-service-flat')

	if request.GET.get("L_info_car"):
		request.session["Service_Key"] = 3 #3 is Lockout
		current_service = Service.objects.get(id_num = 3)
		temp_car_make = request.REQUEST.get("make")
		temp_car_model = request.REQUEST.get("model")
		temp_car_year = request.REQUEST.get("year")
# 		NEW TEMP CAR
		temp_car = Car(make=temp_car_make, model=temp_car_model, year=temp_car_year, id_num=0, name=temp_car_make + " " + temp_car_model)
		print(temp_car.name)
		temp_car.temporary = True;			
		temp_car.selected = True;
		temp_car.save()
		request.session["Car_Make"] = temp_car_make
		request.session["Car_Model"] = temp_car_model
		request.session["Car_Year"] = temp_car_year
#		NEW REQUEST			
		new_request = Request(service=current_service.name, cost=current_service.cost, time_created = datetime.datetime.now())
		new_request.car = temp_car
		new_request.save()
		request.session["Request_PK"] = new_request.pk
		return HttpResponseRedirect('/emergency-service-details')

	if request.GET.get("JS_info_car"):
		request.session["Service_Key"] = 4 #4 is Jump Start
		current_service = Service.objects.get(id_num = 4)
		temp_car_make = request.REQUEST.get("make")
		temp_car_model = request.REQUEST.get("model")
		temp_car_year = request.REQUEST.get("year")
# 		NEW TEMP CAR
		temp_car = Car(make=temp_car_make, model=temp_car_model, year=temp_car_year, id_num=0, name=temp_car_make + " " + temp_car_model)
		print(temp_car.name)
		temp_car.temporary = True;			
		temp_car.selected = True;
		temp_car.save()
		request.session["Car_Make"] = temp_car_make
		request.session["Car_Model"] = temp_car_model
		request.session["Car_Year"] = temp_car_year
#		NEW REQUEST			
		new_request = Request(service=current_service.name, cost=current_service.cost, time_created = datetime.datetime.now())
		new_request.car = temp_car
		new_request.save()
		request.session["Request_PK"] = new_request.pk
		return HttpResponseRedirect('/emergency-service-details')

	if request.GET.get("GS_info_car"):
		request.session["Service_Key"] = 5 #5 is Gas Service
		current_service = Service.objects.get(id_num = 5)
		temp_car_make = request.REQUEST.get("make")
		temp_car_model = request.REQUEST.get("model")
		temp_car_year = request.REQUEST.get("year")
# 		NEW TEMP CAR
		temp_car = Car(make=temp_car_make, model=temp_car_model, year=temp_car_year, id_num=0, name=temp_car_make + " " + temp_car_model)
		print(temp_car.name)
		temp_car.temporary = True;			
		temp_car.selected = True;
		temp_car.save()
		request.session["Car_Make"] = temp_car_make
		request.session["Car_Model"] = temp_car_model
		request.session["Car_Year"] = temp_car_year
#		NEW REQUEST			
		new_request = Request(service=current_service.name, cost=current_service.cost, time_created = datetime.datetime.now())
		new_request.car = temp_car
		new_request.save()
		request.session["Request_PK"] = new_request.pk
		return HttpResponseRedirect('/emergency-service-details')
	return render(request, "Roadside_Home.html", context)

def E_ServiceTow(request):
	service_key = request.session["Service_Key"]
	request_pk = request.session["Request_PK"]
	context = {}
	car_name = request.session["Car_Make"] + " " + request.session["Car_Model"]
	current_service = Service.objects.get(id_num = service_key)
	current_request = Request.objects.get(pk=request_pk)

	context["Service_Name"] = current_service.name
	context["Cost"] = current_service.cost
	context["Car_Name"] = car_name
	context["ETA"] = current_service.estimated_time
	service_total = current_service.cost + 20 #arbitrary right now
	context["Total"] = service_total

	if request.GET.get("to_details_btn"):
		ditch_answer = request.REQUEST.get("ditch")
		print("Ditch answer: " + ditch_answer)
		if (ditch_answer == "Yes"):
			current_request.in_ditch = True
			current_request.save()
		accident_answer = request.REQUEST.get("accident")
		print("Accident answer: " + accident_answer)
		if (accident_answer == "Yes"):
			current_request.accident = True
			current_request.save()
		message = request.REQUEST.get("message_body")
		current_request.message = current_request.message + " " + message
		current_request.save()
		#code to save information here
		return HttpResponseRedirect("/emergency-service-details")
	return render(request, "Roadside_Tow_Service.html", context)

def E_ServiceFlat(request):
	context = {}
	service_key = request.session["Service_Key"]
	request_pk = request.session["Request_PK"]
	car_name = request.session["Car_Make"] + " " + request.session["Car_Model"]
	current_service = Service.objects.get(id_num = service_key)
	current_request = Request.objects.get(pk=request_pk)

	context["Service_Name"] = current_service.name
	context["Cost"] = current_service.cost
	context["Car_Name"] = car_name
	context["ETA"] = current_service.estimated_time
	service_total = current_service.cost + 20 #arbitrary right now
	context["Total"] = service_total

	if request.GET.get("to_details_btn"):
		ditch_answer = request.REQUEST.get("ditch")
		print("Ditch answer: " + ditch_answer)
		if (ditch_answer == "Yes"):
			current_request.in_ditch = True
			current_request.save()
		accident_answer = request.REQUEST.get("accident")
		print("Accident answer: " + accident_answer)
		if (accident_answer == "Yes"):
			current_request.accident = True
			current_request.save()
		tire_list = request.GET.getlist("select_tire")

		message = request.REQUEST.get("message_body")
		current_request.message = current_request.message + " " + message
		current_request.save()

 		for i in tire_list:
			print(i)
			current_request.flat_tires = current_request.flat_tires + i + ", "
			current_request.save()
		if len(tire_list) > 1:
			request.session["Service_Key"] = 1
			current_service = Service.objects.get(id_num = 1)
			print(current_service.name)
			current_request.service = current_service.name
			current_request.save()
			request.session["From_Flat"] = True
			return HttpResponseRedirect("/emergency-service-details")
			#code to save information here
		return HttpResponseRedirect("/emergency-service-details")
	return render(request, "Roadside_Flat_Tire.html", context)

def E_ServiceDetails(request):
	# if ("From_Flat" in request.session) and (request.session[From_Flat] == True):
	# 	
	service_key = request.session["Service_Key"]
	car_name = request.session["Car_Make"] + " " + request.session["Car_Model"]
	current_service = Service.objects.get(id_num = service_key)
	context = {}
	context["Service_Name"] = current_service.name
	context["Cost"] = current_service.cost
	context["Car_Name"] = car_name
	context["ETA"] = current_service.estimated_time

	if request.GET.get("to_payment_btn"):
		print("payment button hit")
		return HttpResponseRedirect("/emergency-service-payment")
	return render(request, "Roadside_Details.html", context)

def E_ServicePayment(request):
	context = {}
	service_key = request.session["Service_Key"]
	request_pk = request.session["Request_PK"]
	car_name = request.session["Car_Make"] + " " + request.session["Car_Model"]
	current_service = Service.objects.get(id_num = service_key)
	current_request = Request.objects.get(pk=request_pk)
	car_year = request.session["Car_Year"]
	context["Service_Name"] = current_service.name
	context["Cost"] = current_service.cost
	context["Car_Name"] = car_name
	context["ETA"] = current_service.estimated_time
	context["Travel_Fee"] = 20.00
	context["Tax"] = round(current_service.cost*0.13, 2)
	context["Total"] = current_service.cost + 20.00 + round(current_service.cost*0.13, 2)
	
	if request.POST.get("payment_btn"):
		cardholder_name = request.REQUEST.get("payment_name")
		billing_address = request.REQUEST.get("payment_address")
		city_state_zip = request.REQUEST.get("city_state_zip")
		card_number = request.REQUEST.get("card_number")
		expiry_date = request.REQUEST.get("expiry_date")
		security_code = request.REQUEST.get("security_code")
		phone_num = request.REQUEST.get("phone_num")
		print(phone_num)
		email = request.REQUEST.get("email")
		# DO EMPTY/NULL CHECK IN JAVASCRIPT LATER
			# if (cardholder_name == "" or billing_address == "" or city_state_zip == "" or 
			# 	card_number == "" or expiry_date == "" or security_code == ""):
			# 	context["Empty_Input"] = "Please fill in all required form fields"
		new_contact = Contact(phone_number = str(phone_num), email = email, phone_num = phone_num)
		new_contact.save()

		current_request.contact = new_contact
		current_request.confirmed = True
		current_request.save()			
		return HttpResponseRedirect("/emergency-service-receipt")
	return render(request, "Roadside_Payment.html", context)

def E_ServiceReceipt(request):
	context = {}
	request_pk = request.session["Request_PK"]
	service_key = request.session["Service_Key"]
	car_name = request.session["Car_Make"] + " " + request.session["Car_Model"]
	current_service = Service.objects.get(id_num = service_key)
	current_request = Request.objects.get(pk=request_pk)
	context["Service_Name"] = current_service.name
	context["Cost"] = current_service.cost
	context["Car_Name"] = car_name
	context["ETA"] = current_service.estimated_time
	service_total = current_service.cost + 20 #arbitrary right now
	context["Total"] = service_total

	if request.GET.get("add_message_btn"):
		print(request.session["Request_PK"])
		message = request.REQUEST.get("message_text")
		print(message)
		current_request.message = current_request.message + " " + message
		current_request.save()
		if message != "":
			context["Message_Received"] = "Your message has been sent!"
		else:
			context["Message_Received"] = "Please include some text in your message body!"
		# return HttpResponseRedirect("/service-receipt")		
	if request.GET.get("return_services"):
		return HttpResponseRedirect("/emergency-service")
	if request.GET.get("create_account"):
		return HttpResponseRedirect("/signup")

	return render(request, "Roadside_Confirmation.html", context)

#DISPATCH STARTS HERE
#DISPATCH STARTS HERE
def Dispatch_Check(user):
	if (user.is_active):
		return Dispatch.objects.filter(user=user).exists()
	else:
		return False

def Dispatch_Ref_Dict(user):
	output = {}
	if Dispatch.objects.filter(user=user).exists():
		dispatcher = Dispatch.objects.get(user=user)
		output["Dispatcher"] = dispatcher
		output["Requests"] = dispatcher.requests.all()
		output["Company"] = dispatcher.company
	return output

@user_passes_test(Dispatch_Check, "/dispatch-login")
def DispatchDisplay(request):
	user = request.user
	ref_dict = Dispatch_Ref_Dict(user)

	dispatcher = ref_dict["Dispatcher"]
	requests = ref_dict["Requests"]
	company = ref_dict["Company"]

	context = {}
	context["Requests"] = []
	if request.REQUEST.get("logout"):
		logout(request)
		return HttpResponseRedirect('/dispatch-login')

	for i in Request.objects.all():
		if (i.claimed == False):
			print("Request Contact email: " + i.contact.email)
			print("Request Contact phone: " + i.contact.phone_number)
			car_info = i.car.make + "/" + i.car.model + "/" + str(i.car.year)
			email = i.contact.email
			phone = i.contact.phone_number
			row = []
			row.append(i.service) #0 is service type
			row.append(email + " / " + str(phone)) #1 is contact info
			row.append(car_info) # 2 is car info
			row.append(str(i.time_created)) #3 is time created
			row.append(i.message) #4 is message
			if (i.in_ditch): #5 is whether in ditch or not
				row.append("Y")
			else:
				row.append("N")
			if (i.accident): #6 is whether in accident or not
				row.append("Y")
			else:
				row.append("N")
			row.append(i.flat_tires) #7 is flat tires
			row.append(str(i.pk)) #8 is id_number
			row.append("C" + str(i.pk)) #9 is button code
			context["Requests"].append(row)

	for i in Request.objects.all():
		if request.GET.get("C" + str(i.pk)):
			# if dispatcher.consecutive_requests >= 3:
			# 	if ((datetime.datetime.now() - dispatcher.last_request_time) > timedelta(hours = 1)):
			# 		dispatcher.last_request_time = datetime.now()
			# 		i.claimed = True
			# 		i.save()
			# 		dispatcher.requests.add(i)
			# 		dispatcher.save()
			# 		return HttpResponseRedirect('/dispatch-requests')					
			# 	else:
			# 		context["Consec_Error"] = "You have claimed too many requests in the last hour"
			# 		return HttpResponseRedirect('/dispatch-requests')
			# else:
			dispatcher.consecutive_requests += 1
			i.claimed = True
			i.save()
			dispatcher.requests.add(i)
			dispatcher.save()
			print("Request " + str(i.pk))
			return HttpResponseRedirect('/dispatch-requests')
		#delete the request and assign to dispatch	
	return render(request, "Dispatch_Portal_Requests.html", context)	

@user_passes_test(Dispatch_Check, "/dispatch-login")
def DispatchAccountRequests(request):
	user = request.user
	ref_dict = Dispatch_Ref_Dict(user)
	dispatcher = ref_dict["Dispatcher"]
	requests = ref_dict["Requests"]
	company = ref_dict["Company"]
	context = {}

	context["Requests"] = []
	context["Requests_Completed"] = []

	if request.REQUEST.get("logout"):
		logout(request)
		return HttpResponseRedirect('/dispatch-login')

	for i in dispatcher.requests.all():
		if (i.completed == False):
			car_info = i.car.make + "/" + i.car.model + "/" + str(i.car.year)
			email = i.contact.email
			phone = i.contact.phone_number
			row = []
			row.append(i.service) #0 is service type
			row.append(email + " / " + phone) #1 is contact info
			row.append(car_info) # 2 is car info
			row.append(str(i.time_created)) #3 is time created
			row.append(i.message) #4 is message
			if (i.in_ditch):
				row.append("Y")
			else:
				row.append("N")
	#		row.append(str(i.in_ditch)) #5 is whether in ditch or not
			if (i.accident):
				row.append("Y")
			else:
				row.append("N")
	#		row.append(str(i.accident)) #6 is in accident or not
			row.append(i.flat_tires) #7 is flat tires
			row.append(str(i.pk)) #8 is id_number
			row.append("C" + str(i.pk)) #9 is button code
			context["Requests"].append(row)
		if (i.completed):
			car_info = i.car.make + "/" + i.car.model + "/" + str(i.car.year)
			email = i.contact.email
			phone = i.contact.phone_number
			row = []
			row.append(i.service) #0 is service type
			row.append(email + " / " + phone) #1 is contact info
			row.append(car_info) # 2 is car info
			row.append(str(i.time_created)) #3 is time created
			row.append(i.message) #4 is message
			if (i.in_ditch):
				row.append("Y")
			else:
				row.append("N")
	#		row.append(str(i.in_ditch)) #5 is whether in ditch or not
			if (i.accident):
				row.append("Y")
			else:
				row.append("N")
	#		row.append(str(i.accident)) #6 is in accident or not
			row.append(i.flat_tires) #7 is flat tires
			row.append(str(i.pk)) #8 is id_number
			row.append("C" + str(i.pk)) #9 is button code
			context["Requests_Completed"].append(row)
	#Claimed requests
	if request.GET.get("delete"):
		for i in dispatcher.requests.all():
			i.completed = True
			i.save()
		return HttpResponseRedirect('/dispatch-claimed-requests/')
	if request.GET.get("update"):
		return HttpResponseRedirect('/dispatch-claimed-requests/')

	for i in dispatcher.requests.all():
		if request.GET.get("C" + str(i.pk)):
			print(i.pk)
			i.completed = True
			i.save()
			return HttpResponseRedirect('/dispatch-claimed-requests/')
	return render(request, "Dispatch_Account_Requests.html", context)	

@user_passes_test(Dispatch_Check, "/dispatch-login")
def DispatchSetting(request):
	user = request.user
	ref_dict = Dispatch_Ref_Dict(user)
	dispatcher = ref_dict["Dispatcher"]
	requests = ref_dict["Requests"]
	company = ref_dict["Company"]

	context = {}
	context["Company"] = company

	password_check = False	
	if request.REQUEST.get("logout"):
		logout(request)
		return HttpResponseRedirect('/dispatch-login')

	if request.POST.get("passwordchange"):
		#ALSO CHECK THAT PASSWORDS MATCH
		p_1 = request.REQUEST.get("password")
		p_2 = request.REQUEST.get("password_2")
		check_1 = (user.check_password(p_1))
		check_2 = (user.check_password(p_2))
		if new_password != "":
			user.set_password(request.REQUEST.get("newpassword"))
			user.save()
		new_password = request.REQUEST.get("newpassword")
		user.set_password(new_password)
		user.save()
		return HttpResponseRedirect("/dispatch-edit-profile")

	if request.POST.get("usernamechange"):
		p_1 = request.REQUEST.get("password")
		p_2 = request.REQUEST.get("password_2")
		check_1 = (user.check_password(p_1))
		check_2 = (user.check_password(p_2))
		if check_1 and check_2:
			new_username = request.REQUEST.get("newusername")
			new_username = request.REQUEST.get("newusername")
			user.username = new_username
			user.save()
		return HttpResponseRedirect("/dispatch-edit-profile")	
	#Change profile
	return render(request, "Dispatch_Setting.html", context)

def DispatchLogin(request):
	#Dispatch Login
	user = request.user
	print(user.username)
	context = {}
	if(request.POST.get("login_btn")):
		print("login button pressed")
		u_name = request.REQUEST.get("username")
		p_word = request.REQUEST.get("password")

		if (u_name == "") or (p_word == ""):
			context["Empty_Input"] = "Please fill in all required form fields"
		if User.objects.filter(username=u_name).exists():
			print("user exists")
			user = User.objects.get(username=u_name)
			user.is_active = True
			user.save()
			print("user is active")
			auth = authenticate(username=u_name, password=p_word)
			print(auth)
			if auth:
				print("authenticated")
				user.save()
				if(Dispatch_Check(user)):
					login(request, auth)
					print("LOGIN SUCCESS")
					print(request.user.username)
					username = request.user.username
					user = User.objects.get(username=username)
					return HttpResponseRedirect('/dispatch-requests/')
		return HttpResponseRedirect('/dispatch-login/')

	if request.POST.get("create_account"):
		return HttpResponseRedirect('/dispatch-signup/')
	return render(request, "Dispatch_Login.html", context)

def DispatchSignUp(request):
	context = {}

	if request.POST.get("create_account"):
		c_name = request.REQUEST.get("companyname")
		username = request.REQUEST.get("username")
		email = request.REQUEST.get("email")
		p_1 = request.REQUEST.get("password_1")
		p_2 = request.REQUEST.get("password_2")

		if (User.objects.filter(username = username).exists()):
			context["Already_Exists"] = "Username already exists! Please use another one"
			return HttpResponseRedirect("/dispatch-signup")

		print("Create Account Button Pressed")
		if (p_1 == p_2 and username != "" and c_name != "" and p_1 != "" ):
			print("Test create account")
			new_user = User.objects.create(username=username, email=email, password=p_1)
			new_user.save()
			new_user.set_password(p_1)
			new_user.is_active = True
			new_user.save()

			new_dispatch = Dispatch(user=new_user)
			new_dispatch.company = c_name
			new_dispatch.save()

			auth = authenticate(username=username, password=p_1)
			new_user.save()
			login(request, auth)			
			return HttpResponseRedirect('/dispatch-requests/')
		else:
			context["Empty_Input"] = "Please fill in all required form fields"
		if (p_1 != p_2):
			context["PWord_Error"] = "Passwords don't match"
	return render(request, "Dispatch_Create_Account.html", context)	
