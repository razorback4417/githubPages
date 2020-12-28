from django.urls import path
from . import views

from django.conf.urls import include
from django.conf.urls import url

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
               
    path("home", views.home, name="home"),
    path("becomeTutor", views.becomeTutor, name="becomeTutor"),
    path("findTutor", views.findTutor, name="findTutor"),
    path("findTutor/<str:subject>", views.findTutor, name="findTutor"),
    path("requests", views.requests, name="requests"),
    path("editrequest", views.editrequest, name="editrequest"),
    path("tutor/<int:id>/", views.tutor, name="tutor"),
    path("edittutor", views.edittutor, name="edittutor"),
    path("myprofile", views.myprofile, name="myprofile"),
    path("changepassword", views.changepassword, name="changepassword"),
               
    path("service", views.service, name="service"),
               
    path("product_detail/<int:product_id>/<slug:product_slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.show_cart, name="show_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("paypal/", include('paypal.standard.ipn.urls')),
    path("process_payment/", views.process_payment, name="process_payment"),
    path("payment_done/", views.payment_done, name="payment_done"),
    path("payment_cancelled/", views.payment_cancelled, name="payment_cancelled")
]
