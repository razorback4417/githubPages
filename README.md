# Final Project - HS Connect

For my final project, I designed and implemented a tutoring website. It allows users to register an account as a tutor or student. As a tutor, one can submit a request to an admin account, providing info such as experience, subject, avaliability, grades they want to teach, etc. The admin has the option to accept or reject the user's request to become a tutor. Students can Find Tutors by subject, and send a request to be taught by a tutor.

This project combines knowledge accumalted from past projects, and extends upon them. 
- In addition to a real-world applicable payment system, I've coded so that requests send actual emails to users, if provided with a valid email. 
- I implemented a Services section that allows user to pay for services (e.g. 1 hour of Math tutoring) that connects with Paypal (note that for demonstration purposes, and proof of concept, the developer mode is used).
- Adding on to past account management, I added a Change Password feature (using a form from django.contrib.auth.forms)
- I utilized Bootstrap to create a clean and userfriendly UI.

# Main files

models.py- User, Tutor, TutorSubject, Request, Product, CartItem, Order and LineItem

cart.py- contains functions that only deal with the Services (buying a service) section of the website.
forms.py- functions for checkout

urls.py- paths for the website

static- js file for frontend of requests page and NoImage.png which displays if a user (who is a tutor) doesnt provide a profile picture

templates folder- all the html files for the website. Info/purpose demonstrated in the video.

#Youtube Link for Demonstration
Note that names/emails were created for testing purposes only.
