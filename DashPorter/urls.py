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
    url(r'^logout/', 'Driver.views.Logout', name='Logout'),
    url(r'^return-home/', 'Driver.views.ReturnHome', name='Return-Home'),
    url(r'^profile-requests/', 'Driver.views.ProfileRequests', name='Profile-Requests'),

    url(r'^requests-display/', 'Driver.views.RequestDisplay', name='Request-Display'),

]

