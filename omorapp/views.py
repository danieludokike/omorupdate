from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import Http404

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from .models import (
    BlogPost, Comment,
    UserContact, YoutubeVideo,
    AboutOmorUpdate, MembersDetails,
)
from .forms.forms import UserContactForm, LoginForm, SignupForm, CommentForm
from .decorators.decorators import un_authenticated_users
from .utils.utils import is_email_taken, is_field_empty, is_username_taken

import re


class HomeView(ListView):
    """RENDERS THE HOME PAGE OF THE OMOR APP BLOG PAGE"""
    queryset = BlogPost.objects.all()[:4]
    context_object_name = 'posts'
    template_name = "omorapp/index.html"
    print(context_object_name)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['featured'] = BlogPost.objects.all()[3:6]
        context['popular'] = BlogPost.objects.all()[6:9]
        context['most_viewed'] = BlogPost.objects.all()[9:11]
        context['most_read'] = BlogPost.objects.all()[11:14]
        context['most_recent'] = BlogPost.objects.all()[14:17]
        context['omor_tube_videos'] = YoutubeVideo.objects.all()[:6]

        return context


@method_decorator(un_authenticated_users, name='get')
@method_decorator(un_authenticated_users, name='post')
class UserSignupView(FormView):
    """FORM FOR USER REGISTRATION"""
    template_name = 'account/signup.html'
    form_class = SignupForm
    initial = {'key': 'value'}
    success_url = reverse_lazy('omorapp:login')

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = request.POST.get('username', None)
            email = request.POST.get('email', None)
            first_name = request.POST.get('first_name', None)
            last_name = request.POST.get('last_name', None)
            password = request.POST.get('password', None)
            password2 = request.POST.get('password2', None)

            if is_field_empty(username, email, first_name, last_name, password, password2):
                messages.error(request, "Please fill-out all fields")
                return redirect('omorapp:signup')

            if password != password2:
                messages.error(request, "Passwords don't match. Try again..")
                return redirect('omorapp:signup')

            if len(password) < 8 or len(password) > 15:
                messages.error(request, "Passwords must be between the range of 8 characters to 15")
                return redirect('omorapp:signup')

            if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
                messages.error(request, f"'{email}' is invalid. Please enter a valid email address")
                return redirect('omorapp:signup')

            if is_email_taken(email):
                messages.error(request, f"'{email}' is already taken. Seems you are registered already?")
                return redirect('omorapp:signup')

            if not re.search(r"^\w+$", username):
                messages.error(request, f"'{username}' is invalid. Can only contain letters and numbers")
                return redirect('omorapp:signup')

            if is_username_taken(username):
                messages.error(request, f"'{username}' is already taken. Seems you are registered already?")
                return redirect('omorapp:signup')

            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                            last_name=last_name)
            user.save()
            messages.info(request, "Registration was successful. Proceed to login")
            return redirect("omorapp:registration_success")

        messages.error(request, "All fields are required!!")
        return render(request, self.template_name, {'form': self.form_class(initial=self.initial)})


def registration_success_view(request):
    """DISPLAYS ON SUCCESSFUL REGISTRATION"""
    return render(request, 'account/registration_success.html')


class UserLoginView(FormView):
    """FORM FOR USER LOGIN"""
    template_name = 'account/login.html'
    form_class = LoginForm
    initial = {'key': 'value'}
    success_url = reverse_lazy('/')

    @method_decorator(un_authenticated_users)
    def get(self, request, *args, **kwargs):
        """HANDLES GET REQUEST"""
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    @method_decorator(un_authenticated_users)
    def post(self, request, *args, **kwargs):
        """HANDLES POST REQUEST"""
        form = self.form_class(request.POST)
        if form.is_valid():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)

            # CHECKING FOR EMPTY FIELD
            if is_field_empty(username, password):
                messages.info(request, 'Please fill-out all fields!!')
                return redirect('omorapp:login')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Successfully logged in as '{username}'!")
                return redirect("omorapp:home")
            messages.error(request, 'Invalid username or password!! Hope you are registered?')
            return redirect("omorapp:login")
        messages.error(request, "Invalid input!! Username and password are required!")
        return redirect("omorapp:login")


def join_omor_update(request):
    """DISPLAYS THE GOOGLE FORM FOR USER CONTACTS"""
    if request.user.is_authenticated:
        return render(request, 'omorapp/join_omorupate.html')
    messages.error(request, "You must login to fill the team omor update form!!")
    return redirect("omorapp:login")


def blog_post_detail_view(request, pk=1):
    """CREATES A BLOG AND SAVE TO THE DATABASE TO BE PUBLISHED IN THE SITE"""
    post = get_object_or_404(BlogPost, id=pk)
    post.views += 1
    post.save()

    form = CommentForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            form = CommentForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.post = post
                obj.user = user
                obj.save()

                messages.success(request, "Your comment on this post has been saved successfully")
                return redirect(f"/blog/{pk}/details/")
            messages.error(request, "Please leave a comment")
            return redirect(f"/blog/{pk}/details/")
        else:
            messages.error(request, "Sorry you need to login to comment on this post")
            return redirect('omorapp:login')

    template = 'omorapp/blog_details.html'
    context = {
        'blog_details': get_object_or_404(BlogPost, id=pk),
        'featured': BlogPost.objects.all()[3:6],
        'popular': BlogPost.objects.all()[6:9],
        'most_viewed': BlogPost.objects.all()[9:11],
        'most_read': BlogPost.objects.all()[11:14],
        'most_recent': BlogPost.objects.all()[14:17],
        'omor_tube_videos': YoutubeVideo.objects.all()[:6],
        'comments': Comment.objects.all(),
        'form': form,
    }

    return render(request, template, context)


# ALL BLOG POST DISPLAY
def blog_post_display_view(request):
    if request.method == 'POST':
        return Http404("Sorry, you are not allowed to post any data on this url")
    featured = BlogPost.objects.all()[:3]
    popular = BlogPost.objects.all()[3:6]
    latest = BlogPost.objects.all()[6:9]
    most_recent = BlogPost.objects.all()[9:12]
    most_viewed = BlogPost.objects.all()[12:15]
    most_read = BlogPost.objects.all()[15:18]

    context = {
        'featured': featured,
        'popular': popular,
        'latest': latest,
        'most_recent': most_recent,
        'most_viewed': most_viewed,
        'most_read': most_read,
    }
    return render(request, 'omorapp/blog.html', context)


class UserContactView(FormView):
    """HANDLES THE USER CONTACT FORM DISPLAY AND SUBMISSION"""
    form_class = UserContactForm
    initial = {'key': 'value'}
    template_name = 'omorapp/contact.html'
    success_url = reverse_lazy('omorapp:home')
    failure_url = reverse_lazy("omorapp:contact")

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = request.POST.get('name', None)
            email = request.POST.get('email', None)
            subject = request.POST.get('subject', None).title()
            message = request.POST.get('message', None)

            if is_field_empty(name, email, subject, message):
                messages.error(request, "Please fill-out all field to send us an email!")
                return redirect(self.failure_url)

            if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
                messages.error(request, f"'{email}' is invalid. Please enter a valid email address")
                return redirect(self.failure_url)

            if not re.search(r"\w+$", name):
                messages.error(request, f"Sorry, is '{name}' your name?. Please enter a valid name")
                return redirect(self.failure_url)

            message = UserContact.objects.create(name=name, email=email, subject=subject, message=message)
            messages.info(request, 'Messages sent successfully. We will be in touch shortly')
            message.save()

            return redirect(self.success_url)

        messages.error(request, f"Sorry an error occurred. Please correct EMAIL ADDRESS fill-out all field")
        return redirect(self.failure_url)


# LOGOUT REQUEST
def logout_view(request):
    logout(request)
    return redirect('omorapp:login')


def about_omorupdate_view(request):
    """DISPLAYS ABOUT OMORUPDATE ON REQUEST"""
    template = "omorapp/about_omorupdate.html"
    about_omorupdate = AboutOmorUpdate.objects.all()

    return render(request, template, {'about_omorupdate': about_omorupdate})


def omorupdate_members(request):
    """DISPLAYS TEAMS OF OMOR UPDATE"""
    template = "omorapp/omorupdate_members.html"
    members = MembersDetails.objects.all()

    return render(request, template, {'members': members})
