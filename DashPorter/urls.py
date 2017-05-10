from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'DashPorter.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^login/', 'Driver.views.Login', name='Login'),

    url(r'^signup/', 'Driver.views.SignUp', name='SignUp'),
    url(r'^home/', 'Driver.views.Home', name='Home'),
    url(r'^add-car/', 'Driver.views.AddCar', name='Add-Car'),
    url(r'^profile/', 'Driver.views.Profile', name='Profile'),
    url(r'^profile-edit/', 'Driver.views.ProfileEdit', name='ProfileEdit'),
    url(r'^about/', 'Driver.views.About', name='About'),
    url(r'^support/', 'Driver.views.Support', name='Support'),
    url(r'^car-service/', 'Driver.views.ServiceCar', name='Service-Car'),
    url(r'^service-details/', 'Driver.views.ServiceDetails', name='Service-Details'),

    url(r'^service-tow/', 'Driver.views.ServiceTow', name='Service-Tow'),
    url(r'^service-flat/', 'Driver.views.ServiceFlat', name='Service-Flat'),
    url(r'^service-payment/', 'Driver.views.ServicePayment', name='Service-Payment'),
    url(r'^service-receipt/', 'Driver.views.ServiceReceipt', name='Service-Receipt'),

    url(r'^return-home/', 'Driver.views.ReturnHome', name='Return-Home'),
    url(r'^profile-requests/', 'Driver.views.ProfileRequests', name='Profile-Requests'),
    url(r'^logout/', 'Driver.views.Logout', name='Logout'),

    url(r'^requests-display/', 'Driver.views.RequestDisplay', name='Request-Display'),

    url(r'^dispatch-requests/', 'Driver.views.DispatchDisplay', name='Dispatch-Display'),
    url(r'^dispatch-login/', 'Driver.views.DispatchLogin', name='Dispatch-Display'),
    url(r'^dispatch-signup/', 'Driver.views.DispatchSignUp', name='Dispatch-Display'),
    url(r'^dispatch-claimed-requests/', 'Driver.views.DispatchAccountRequests', name='Dispatch-Display'),
    url(r'^dispatch-edit-profile/', 'Driver.views.DispatchSetting', name='Dispatch-Display'),

    url(r'^emergency-service/', 'Driver.views.E_Home', name='Request-Display'),

    url(r'^emergency-service-flat/', 'Driver.views.E_ServiceFlat', name='Request-Display'),
    url(r'^emergency-service-tow/', 'Driver.views.E_ServiceTow', name='Request-Display'),
    url(r'^emergency-service-details/', 'Driver.views.E_ServiceDetails', name='Request-Display'),
    url(r'^emergency-service-payment/', 'Driver.views.E_ServicePayment', name='Request-Display'),
    url(r'^emergency-service-receipt/', 'Driver.views.E_ServiceReceipt', name='Request-Display'),

    url(r"^$", 'Driver.views.E_Home', name='First-Page'),

]

