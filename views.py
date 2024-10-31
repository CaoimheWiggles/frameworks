
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm, ContactForm  
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from .models import Project, Message, UserProfile, Feedback, User
from .forms import ProjectForm, MessageForm, UserProfileForm
from cryptography.fernet import Fernet
from django.conf import settings



poll_results = {
    "Keeping a consistent routine": 0,
    "Using positive reinforcement": 0,
    "Setting clear boundaries": 0,
    "Distracting with activities": 0
}

poll_options = list(poll_results.keys())

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('core/login')  
    else:
        form = UserRegistrationForm()
    
    return render(request, 'core/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('index')  
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('index')  

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
        
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            
            send_mail(
                subject=f'Contact Form Submission from {name}',
                message=message,
                from_email=email,
                recipient_list=['caoimhew@hotmail.com'], 
                fail_silently=False,
            )

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('index')  
    else:
        form = ContactForm()  
        
    return render(request, 'core/contact.html', {'form': form}) 

@login_required  
def contact_view(request):
    if request.method == 'POST':
        feedback_message = request.POST.get('feedback_message') 
        user_id = request.user.id  

        new_feedback = Feedback(user_id=user_id, message=feedback_message)
        new_feedback.save()

        messages.success(request, 'Feedback submitted successfully!')
        return redirect('thanks_feedback', username=request.user.username)

    return render(request, 'contact.html')

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('project_list')  
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})


def profile_view(request, username):
    user = User.objects.get(username=username)
    profile = UserProfile.objects.get(user=user)
    return render(request, 'profile.html', {'profile': profile})

def edit_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

def base_view(request):
    messages = Message.objects.filter(recipient=request.user, is_archived=False)
    return render(request, 'base.html', {'messages': messages})

def unread_messages(request):
    if request.user.is_authenticated:
        unread_messages = Message.objects.filter(recipient=request.user, is_read=False)
        messages_data = [{
            'sender': message.sender.username,
            'subject': message.subject,
            'content': message.content
        } for message in unread_messages]
        
        unread_messages.update(is_read=True)
        
        return JsonResponse({'new_messages': messages_data})
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=403)


@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user  
            message.save()
            return redirect('inbox')  
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form})

@login_required
def archive_message(request, message_id):
    message = Message.objects.get(id=message_id, recipient=request.user)
    if message:
        message.is_archived = True
        message.save()
    return redirect('inbox')  

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user, is_archived=False)
    return render(request, 'inbox.html', {'messages': messages})

def about(request):
    return render(request, 'core/about.html')

def base(request):
    return render(request, 'core/base.html')

def blogs(request):
    return render(request, 'core/blogs.html')

def featured_post(request):
    return render(request, 'core/featured_post.html')

def forgot_password(request):
    return render(request, 'core/forgot_password.html')

def post1(request):
    return render(request, 'core/post1.html')

def post2(request):
    return render(request, 'core/post2.html')

def post3(request):
    return render(request, 'core/post3.html')

def post4(request):
    return render(request, 'core/post4.html')

def post5(request):
    return render(request, 'core/post5.html')

def post6(request):
    return render(request, 'core/post6.html')

def reset_password(request):
    return render(request, 'core/reset_password.html')

def update_password(request):
    return render(request, 'core/update_password.html')

def verify_email(request):
    return render(request, 'core/verify_email.html')

def verify_email_sent(request):
    return render(request, 'core/verify_email_sent.html')

def thanks_feedback(request):
    return render(request, 'core/thanks_feedback.html')

def thank_you(request):
    return render(request, 'core/thank_you.html')

def index(request):
    return render(request, 'core/index.html')

def verify_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        send_mail(
            'Email Verification',
            'Click the link to verify your email: verify',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return redirect('verify_email_sent')
    
    return render(request, 'core/verify_email.html')

def verify_email_sent(request):
    return render(request, 'core/verify_email_sent.html')

def poll_view(request):
    return render(request, 'poll.html', {'poll_results': poll_results})

@csrf_exempt  
def vote(request):
    if request.method == 'POST':
        data = json.loads(request.body)  
        choice = data.get('choice')

        if choice in poll_results:
            poll_results[choice] += 1

        response_data = {option: poll_results.get(option, 0) for option in poll_options}
        return JsonResponse(response_data)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

