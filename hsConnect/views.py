from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse

from django.core.mail import send_mail

from django.conf import settings

from .models import User, Subject, Tutor, TutorSubject, Request

# Create your views here.

def index(request):
    return render(request, "hsConnect/layout.html")

def home(request):
    return render(request, "hsConnect/home.html")

def findTutor(request):
    return render(request, "hsConnect/findTutor.html")

def editrequest(request):
    if request.method == "POST":
        username = request.POST["username"]
        requestid = request.POST["requestid"]
        req_rec = Request.objects.get(id=requestid)
        requestor = req_rec.requestor
        tutorname = req_rec.tutorname
        req_type = req_rec.type

        #req_email = req_rec.req_email
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
            #recipient_list.append(req_email)
            if req_type == 'Become a Tutor':
                tutor_rec = Tutor.objects.get(userstamp=requestor)
                tutor_rec.status = 'Active'
                tutor_rec.save()
                email_subject = "Your request to become a tutor has been approved"
                email_message = "Request ID: " + requestid + " for " + requestor + " has been approved."
                ack_message = "Become a tutor for " + requestor + " has been approved."

        if request.POST.get("rejectreq-btn"):
            req_rec.status = 'Rejected'
            req_rec.save()
            recipient_list.append(tutor_email)
            recipient_list.append(admin_email)
            if req_type == 'Become a Tutor':
                email_subject = "Your request to become a tutor has been rejected"
                email_message = "Request ID: " + requestid + " for " + requestor + " has been rejected."
                ack_message = "Become a tutor for " + requestor + " has been rejected."

        if email_subject != '':
            send_mail(email_subject, email_message, email_from, recipient_list)

        requests = Request.objects.all()

        return render(request, "hsConnect/requests.html", {
            "request": requests,
            "message": ack_message
        })
            
    else:
        return render(request, "hsConnect/requests.html")

def requests(request):
    y = request.user.id
    print(y)
    print(type(y))
    if y == 7:
        print("i am here")
        requests = Request.objects.all().order_by('-createdDate')
        title = "Requests"
    else:
        print("here i am")
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
    
        admin_email = User.objects.values_list('email', flat=True).get(username='Admin')
    
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
            tutor = Tutor(status = 'Requested', image=image, availability=availability, firstName=firstname, lastName=lastname, email=req_email, about=about, grades=grades, userstamp=userstamp)
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


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "hsConnect/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "hsConnect/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "hsConnect/register.html")
