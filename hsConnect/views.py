from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse

from django.core.mail import send_mail

from django.conf import settings

from .models import User, Subject, Tutor, TutorSubject, Request
from .models import Product, CartItem, Order, LineItem

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from .forms import CartForm, CheckoutForm
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import get_object_or_404, reverse
from . import cart

from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def index(request):
    return render(request, "hsConnect/layout.html")

def home(request):
    return render(request, "hsConnect/home.html")

def service(request):
    products = Product.objects.all()
    return render(request, "hsConnect/service.html", {
        "products": products
    })

def myprofile(request):
    userstamp = request.user
    user_rec = User.objects.get(username=userstamp)

    return render(request, "hsConnect/profile.html",{
        "user": user_rec,
    })

def edittutor(request):
    
    if request.method == "POST":
        tutorid = request.POST["tutorid"]
        tutor = Tutor.objects.get(id=tutorid)
        status = tutor.status
        firstname = tutor.firstName
        lastname = tutor.lastName

        tutor_email = tutor.email
        recipient_list = []
        admin_email = User.objects.values_list('email', flat=True).get(username='admin1')
        email_from = settings.EMAIL_HOST_USER
        email_subject = ''
        email_message = ''

        availability = request.POST["availability"]
        
        if request.POST.get("findtutorrequest-btn"):
            subject = request.POST["subject"]
            grade = request.POST["grade"]
            description = request.POST["description"]

            type = 'Find a Tutor'
            requestor = request.user
            req_email = User.objects.values_list('email', flat=True).get(username=request.user)
            tutorname = tutor.userstamp
            userstamp = request.user

            request_row = Request(status='Requested', description = description, subject = subject, grade=grade, type=type, requestor=requestor, availability=availability, tutorname=tutorname, req_email=req_email)
            request_row.save()

            recipient_list.append(tutor_email)
            recipient_list.append(admin_email)
            recipient_list.append(req_email)

            email_subject = 'Tutoring Request from ' + req_email + ' to ' + tutor_email
            email_message = "Description: " + description
            ack_message = "Your request has been sent to " + tutor_email

            send_mail(email_subject, email_message, email_from, recipient_list)

            allsubjects = Subject.objects.filter(active='Y').order_by('subject')
            
            

            return render(request, "hsConnect/tutor.html", {
                "tutor": tutor,
                "allsubjects": allsubjects,
                "message": ack_message,
            })



def tutor(request, id):
    tutor = Tutor.objects.get(pk=id)
    allsubjects = Subject.objects.filter(active='Y').order_by('subject')

    return render(request, "hsConnect/tutor.html", {
        "tutor": tutor,
        "allsubjects": allsubjects
    })

def findTutor(request, subject="None"):
    tutors = Tutor.objects.all().filter(status='Active').order_by('-createdDate')
    allsubjects = Subject.objects.filter(active='Y').order_by('subject')
    
    if request.method == "POST":
        subject = request.POST["q"]
    
    y = request.user.id
    if y == 10:
        if subject == "None":
            tutors = Tutor.objects.all()
        else:
            tutor = Tutor.objects.filter(subject__contains=subject)
    else:
        if subject == "None":
            tutors = Tutor.objects.filter(status='Active') #, subject__contains=subject)
        else:
            print("here")
            tutors = Tutor.objects.filter(status='Active', subject__contains=subject)
    
    return render(request, "hsConnect/findTutor.html", {
        "tutors": tutors,
        "allsubjects": allsubjects
    })

def editrequest(request):
    ack_message = ''
    if request.method == "POST":
        username = request.POST["username"]
        requestid = request.POST["requestid"]
        req_rec = Request.objects.get(id=requestid)
        requestor = req_rec.requestor
        tutorname = req_rec.tutorname
        req_type = req_rec.type

        req_email = req_rec.req_email
        tutor_email = req_rec.req_email
        admin_email = User.objects.values_list('email', flat=True).get(username='admin1')
        email_from = settings.EMAIL_HOST_USER
        email_subject = ''
        email_message = ''
        recipient_list = []

        if request.POST.get("approvereq-btn"):
            req_rec.status = 'Approved'
            req_rec.save()
            recipient_list.append(tutor_email)
            recipient_list.append(admin_email)
            recipient_list.append(req_email)
            if req_type == 'Become a Tutor':
                tutor_rec = Tutor.objects.get(userstamp=requestor)
                tutor_rec.status = 'Active'
                tutor_rec.save()
                email_subject = "Your request to become a tutor has been approved"
                email_message = "Request ID: " + requestid + " for " + requestor + " has been approved."
                ack_message = "Become a tutor for " + requestor + " has been approved."
            if req_type == 'Find a Tutor':
                email_subject = "Your Find a Tutor Request has been approved"
                email_message = "Request ID: " + requestid + " for " + requestor + " to work with tutor, " + tutorname + " has been approved."
                ack_message = "Find a Tutor request for " + requestor + " has been approved."

        if request.POST.get("rejectreq-btn"):
            req_rec.status = 'Rejected'
            req_rec.save()
            recipient_list.append(tutor_email)
            recipient_list.append(admin_email)
            recipient_list.append(req_email)
            if req_type == 'Become a Tutor':
                email_subject = "Your request to become a tutor has been rejected"
                email_message = "Request ID: " + requestid + " for " + requestor + " has been rejected."
                ack_message = "Become a tutor for " + requestor + " has been rejected."
            if req_type == 'Find a Tutor':
                email_subject = "Your Find a Tutor Request has been rejected"
                email_message = "Request ID: " + requestid + " for " + requestor + " to work with tutor, " + tutorname + " has been rejected."
                ack_message = "Find a Tutor request for " + requestor + " has been rejected."

        if email_subject != '':
            send_mail(email_subject, email_message, email_from, recipient_list)

        requests = Request.objects.all()
        
        y = request.user.id
        if y == 10:
            requests = Request.objects.all().order_by('-createdDate')
            title="Requests"
        else:
            requests = Request.objects.filter(requestor=request.user).order_by('-createdDate')
            title="My Requests"

        return render(request, "hsConnect/requests.html", {
            "requests": requests,
            "message": ack_message,
            "title": title
        })
            
    else:
        return render(request, "hsConnect/requests.html")

def requests(request):
    y = request.user.id
    #print(y)
    if y == 10:
        requests = Request.objects.all().order_by('-createdDate')
        title="Requests"
    else:
        requests = Request.objects.filter(requestor=request.user).order_by('-createdDate')
        title="My Requests"
    
    return render(request, "hsConnect/requests.html", {
        "requests": requests,
        "title": title
    })

def becomeTutor(request):
    if request.method == "POST":
        image = request.POST["photo"]
        about = request.POST["about"]
        subjects = request.POST.getlist('subjects')
        availability = request.POST["availability"]
        grades = request.POST.getlist('grades')
        userstamp = request.POST["userstamp"]
    
        user_rec = User.objects.get(username=userstamp)
        req_email = user_rec.email
        firstname = user_rec.first_name
        lastname = user_rec.last_name
    
        admin_email = User.objects.values_list('email', flat=True).get(username='admin1')
    
        recipient_list = []
        recipient_list.append(req_email)
        recipient_list.append(admin_email)
        subject = 'Thank you'
        message = 'Thanks for applying'
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, recipient_list)
    
        count = Tutor.objects.filter(userstamp=userstamp).count()
        if count is None:
            count = 0
        if count == 0:
            tutor = Tutor(status = 'Requested', image=image, availability=availability, firstName=firstname, lastName=lastname, email=req_email, about=about, grades=grades, subject=subjects, userstamp=userstamp)
            tutor.save()
            tutorid = Tutor.objects.values_list('id', flat=True).get(userstamp=userstamp)
        else:
            return render(request, "hsConnect/becomeTutor.html", {
                "message": "Tutor already existed"
            })
                
        for subj in subjects:
            subj_row = TutorSubject(tutorid=tutorid, subject=subj)
            subj_row.save()
        
        requestor = request.user
        userstamp = requestor
        request_row = Request(status='Requested', description='Become a Tutor', subject=subjects, grade=grades, type='Become a Tutor', requestor=requestor, availability=availability, req_email=req_email, userstamp=userstamp)
        request_row.save()
        return render(request, "hsConnect/becomeTutor.html", {
            "message": "Request has been submitted and is pending approval."
        })
        
    allsubjects = Subject.objects.filter(active='Y').order_by('subject')
    return render(request, "hsConnect/becomeTutor.html", {
        "allsubjects": allsubjects
    })


def changepassword(request):
    ack_message = ""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your request was successfully updated.")
            ack_message = "Your request was successfully updated."
        else:
            messages.error(request, "Please correct the error below")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "hsConnect/changepassword.html", {
        "form": form,
        "message": ack_message
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "hsConnect/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "hsConnect/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "hsConnect/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password, first_name=firstname, last_name=lastname)
            user.save()
        except IntegrityError:
            return render(request, "hsConnect/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "hsConnect/register.html")

#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

#PAYPAL:

def product_detail(request, product_id, product_slug):
    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        form = CartForm(request, request.POST)
        if form.is_valid():
            request.form_data = form.cleaned_data
            cart.add_item_to_cart(request)
            return redirect("show_cart")
        else:
            print("Error: Bad Form")
                            
    form = CartForm(request, initial={"product_id": product_id})
    return render(request, "hsConnect/product_detail.html", {
        "product": product,
        "form": form,
    })

def show_cart(request):
    if request.method == "POST":
        if request.POST.get('submit') == 'Update':
            cart.update_item(request)
        
        if request.POST.get('submit') == 'Remove':
            cart.remove_item(request)

    cart_items = cart.get_all_cart_items(request)
    print(cart_items)
    cart_subtotal = cart.subtotal(request)
    return render(request, "hsConnect/cart.html", {
        "cart_items": cart_items,
        "cart_subtotal": cart_subtotal
    })

def checkout(request):
    print('checkout')
    if request.method == 'POST':
        print('step1')
        form = CheckoutForm(request.POST)
        print('step2')
        if form.is_valid():
            print('step3')
            cleaned_data = form.cleaned_data
            print('step4')
            o = Order(
                name = cleaned_data.get('name'),
                email = cleaned_data.get('email'),
                postal_code = cleaned_data.get('postal_code'),
                address = cleaned_data.get('address'),
            )
            o.save()
            print('step5')

            all_items = cart.get_all_cart_items(request)
            print('step6')
            for cart_item in all_items:
                li = LineItem(
                    product_id = cart_item.product_id,
                    price = cart_item.price,
                    quantity = cart_item.quantity,
                    order_id = o.id
                )

                li.save()

            print('step7')
            cart.clear(request)
            print('step8')
            print('o.id=',o.id)
            request.session['order_id'] = o.id
            print('step9')
            return redirect('process_payment')

            messages.add_message(request, messages.INFO, 'Order Placed!')
            return redirect('checkout')
    else:
        print('step2')
        form = CheckoutForm()
        print('form=', form)
        return render(request, "hsConnect/checkout.html", {
            "form": form
        })

def process_payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.total_cost(),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, "hsConnect/process_payment.html", {
        "order": order,
        "form": form
    })

@csrf_exempt
def payment_done(request):
    order_id = request.session.get('order_id')
    order_rec = Order.objects.get(id=order_id)
    order_rec.paid = True
    order_rec.save()
    return render(request, "hsConnect/payment_done.html")


@csrf_exempt
def payment_cancelled(request):
    order_id = request.session.get('order_id')
    order_rec = Order.objects.filter(id=order_id)
    order_rec.delete()
    return render(request, "hsConnect/payment_cancelled.html")
