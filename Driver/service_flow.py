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
