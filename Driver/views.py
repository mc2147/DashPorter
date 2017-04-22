import datetime
from django.shortcuts import render
from .models import Car, Driver, Service, Request, Repair_Shop
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import logout, login, authenticate

def Login(request):
	user = request.user
	print(user.username)
	if(request.GET.get("login_btn")):
		print("login button pressed")
		u_name = request.REQUEST.get("username")
		p_word = request.REQUEST.get("password")
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
				login(request, auth)
				print("LOGIN SUCCESS")
				print(request.user.username)
				username = request.user.username
				user = User.objects.get(username=username)
				return HttpResponseRedirect('/home/')
	if request.GET.get("go_to_create_account"):
		return SignUp(request)
	return render(request, "Login_Frame.html")

def Logout(request):
	logout(request)
	return HttpResponseRedirect("/login")

def SignUp(request):
	context = {}
	if request.GET.get("create_account"):
		f_name = request.REQUEST.get("first_name")
		l_name = request.REQUEST.get("last_name")
		email = request.REQUEST.get("email")
		number = request.REQUEST.get("number")
		p_1 = request.REQUEST.get("p_word")
		p_2 = request.REQUEST.get("p_word_2")
		print("Create Account Button Pressed")
		if (p_1 == p_2 and f_name != "" and l_name != "" and email != "" and p_1 != "" ):
			new_user = User.objects.create(username=email, first_name=f_name, last_name=l_name, password=p_1)
			new_user.save()
			new_user.set_password(p_1)
			new_user.is_active = True
			new_user.save()
			new_driver = Driver(user=new_user)
			new_driver.phone_number = number
			new_driver.save()
			auth = authenticate(username=email, password=p_1)
			new_user.save()
			login(request, auth)
			return Home(request)
		elif (p_1 != p_2):
			context["PWord_Error"] = "Passwords don't match"
	return render(request, "Create_Profile_Frame.html", context)

service = ""

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


def Home(request):	
	tow_truck = Service.objects.get(id_num = 1)
	tow_truck.description = "Description for Tow Truck service"
	tow_truck.save()

	flat_tire = Service.objects.get(id_num = 2)
	flat_tire.description = "Description for Flat Tire service"
	flat_tire.save()

	lockout = Service.objects.get(id_num = 3)
	lockout.description = "Description for Lockout Service"
	lockout.save()

	jump_start = Service.objects.get(id_num = 4)
	jump_start.description = "Description for Jump Start service"	
	jump_start.save()

	gas_service = Service.objects.get(id_num = 5)
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
			row = []
			row.append(i.name) #0 is name
			row.append(i.pk) #1 is pkid
			context["Car_Names"].append(row)

	for i in driver.requests.all():
		if i.confirmed == False:
			driver.requests.remove(i)
			driver.save()
			i.delete()

	# if len(requests) != 0 and requests[len(requests)-1].confirmed == False:
	# 	driver.requests.remove(requests[len(requests)-1]) #deletes unfinished service requests
	# 	driver.save()

	if request.GET.get("Tow_select_car") or request.GET.get("Tow_info_car"):
		driver.current_service_key = 1 #1 is Oil Change
		driver.save()
		current_service = Service.objects.get(id_num = 1)
		if request.GET.get("Tow_select_car"):
			print("Test")
			selected_id = request.REQUEST.get("selected_car_tow")
			print(selected_id)
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
			temp_car_make = request.REQUEST.get("T_make")
			temp_car_model = request.REQUEST.get("T_model")
			temp_car_year = request.REQUEST.get("T_year")
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
			new_request = Request(requester=driver.user.username, service=current_service.name, cost=current_service.cost)
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
			temp_car_make = request.REQUEST.get("FT_make")
			temp_car_model = request.REQUEST.get("FT_model")
			temp_car_year = request.REQUEST.get("FT_year")
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
			new_request = Request(requester=driver.user.username, service=current_service.name, cost=current_service.cost)
			new_request.save()
			driver.requests.add(new_request)
			driver.save()
		return HttpResponseRedirect('/service-flat')

	if request.GET.get("L_select_car") or request.GET.get("L_info_car"):
		driver.current_service_key = 3 #3 is Lockout
		driver.save()

		if request.GET.get("L_select_car"):
			selected_id = request.REQUEST.get("selected_car_L")
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
			temp_car_make = request.REQUEST.get("L_make")
			temp_car_model = request.REQUEST.get("L_model")
			temp_car_year = request.REQUEST.get("L_year")
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
			new_request = Request(requester=driver.user.username, service=current_service.name, cost=current_service.cost)
			new_request.save()
			driver.requests.add(new_request)
			driver.save()
		return HttpResponseRedirect('/service-details')

	if request.GET.get("JS_select_car") or request.GET.get("JS_info_car"):
		driver.current_service_key = 4 #4 is Jump Start
		driver.save()
		if request.GET.get("JS_select_car"):
			selected_id = request.REQUEST.get("selected_car_JS")
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
			temp_car_make = request.REQUEST.get("JS_make")
			temp_car_model = request.REQUEST.get("JS_model")
			temp_car_year = request.REQUEST.get("JS_year")
			print(temp_car_make)
			print(temp_car_model)
			print(temp_car_year)			
#			NEW TEMP CAR 
			temp_car = Car(make=temp_car_make, model=temp_car_model, year=temp_car_year, id_num=0, name=temp_car_make + " " + temp_car_model)
			print(temp_car.name)
			temp_car.temporary = True;			
			temp_car.save()

			driver.cars.add(temp_car)
			driver.current_car_id = 0
			driver.save()

			new_request = Request(requester=driver.user.username, service=current_service.name, cost=current_service.cost)
			new_request.save()
			driver.requests.add(new_request)
			driver.save()			
		return HttpResponseRedirect('/service-details')

	if request.GET.get("GS_select_car") or request.GET.get("GS_info_car"):
		driver.current_service_key = 5 #5 is Gas Service
		driver.save()
		if request.GET.get("GS_select_car"):
			selected_id = request.REQUEST.get("GS_car")
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
			temp_car_make = request.REQUEST.get("GS_make")
			temp_car_model = request.REQUEST.get("GS_model")
			temp_car_year = request.REQUEST.get("GS_year")
			print(temp_car_make)
			print(temp_car_model)
			print(temp_car_year)			
#			NEW TEMP CAR 
			temp_car = Car(make=temp_car_make, model=temp_car_model, year=temp_car_year, id_num=0, name=temp_car_make + " " + temp_car_model)
			print(temp_car.name)
			temp_car.temporary = True;			
			temp_car.save()

			driver.cars.add(temp_car)
			driver.current_car_id = 0
			driver.save()

			new_request = Request(requester=driver.user.username, service=current_service.name, cost=current_service.cost)
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


		current_request.flat_tires = current_request.flat_tires + ditch_answer + " " + accident_answer
		#code to save information here
		return HttpResponseRedirect("/service-details")
	return render(request, "Tow_Service_Frame.html", context)

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

def ServiceCar(request):
	context = {}
	user = request.user
	ref_dict = Ref_Dict(user)
	driver = ref_dict["Driver"]
	current_car = ref_dict["Current Car"]
	current_service = ref_dict["Current Service"]
	return render(request, "Service_Car_Frame.html")
	
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
		current_request.save()
		driver.requests.add(current_request)
		driver.current_request_id = current_request.pk
		driver.save()
		return HttpResponseRedirect("/service-receipt")

	return render(request, "Service_Payment_Frame.html", context)	

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
		row.append(", ID_num: " + str(i.id_num))
		context["Requests"].append(row)

		# request_string = ""
		# request_string = i.requester + " " + i.service + " " + str(i.cost) + " " + str(i.time_created)
		# context["Requests"].append(request_string)

	# user = request.user
	# ref_dict = Ref_Dict(user)
	# driver = ref_dict["Driver"]
	# current_car = ref_dict["Current Car"]
	# current_service = ref_dict["Current Service"]
	# #need service details, provider details, eta and location for google maps
		#also contact information of two truck driver
		#delete current service after transaction is completed?
	return render(request, "Request_Display.html", context)	


def AddCar(request):
	user = request.user	
	# driver = Driver.objects.get(user=user)
	ref_dict = Ref_Dict(user)
	driver = ref_dict["Driver"]
	if (driver.cars.all()):
		current_car = ref_dict["Current Car"]
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
		new_car = Car(make = new_car_make, model=new_car_model, year=new_car_year, name=new_car_make + " " + new_car_model)
		new_car.save()
		context["car_added"] = "Car Added! You can store up to 3 cars in your profile."
		print("new car make: " + new_car.make)
		driver.cars.add(new_car)
		# new_car.id_num = driver.cars.all().index(new_car)
		new_car.save()
		driver.save()
		# Driver.cars.add(new_car)
		# Driver.save()
	return render(request, "Add_Car_Frame.html", context)

def Profile(request):
	user = request.user
	ref_dict = Ref_Dict(user)
	# output["Current Car"] 
	# output["Current Service"] = Service.objects.get(id_num = driver.current_service_key)
	# output["Cars"] = driver.cars.all()
	driver = ref_dict["Driver"]
	context = {}
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

def About(request):
	
	return render(request, "About_Frame.html")

def Support(request):
	
	return render(request, "Support_Frame.html")

