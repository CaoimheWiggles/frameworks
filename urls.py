
from django.urls import path, include
from . import views
from .views import register, user_login, user_logout, poll_view, vote, create_project, profile_view, edit_profile, send_message, inbox, contact_view, feedback_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),    
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('base/', views.base, name='base'),
    path('blogs/', views.blogs, name='blogs'),
    path('featured-post/', views.featured_post, name='featured_post'),  
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('post1/', views.post1, name='post1'),
    path('post2/', views.post2, name='post2'),
    path('post3/', views.post3, name='post3'),
    path('post4/', views.post4, name='post4'),
    path('post5/', views.post5, name='post5'),
    path('post6/', views.post6, name='post6'),
    path('poll/', poll_view, name='poll'),  
    path('vote/', vote, name='vote'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('verify_email_sent/', views.verify_email_sent, name='verify_email_sent'),
    path('thanks_feedback/', views.thanks_feedback, name='thanks_feedback'),
    path('thank-you/', views.thank_you, name='thank_you'),  
    path('', views.index, name='index'), 
    path('feedback/', feedback_view, name='feedback'),
    path('contact/', contact_view, name='contact'),  
    path('thanks/<str:username>/', views.thanks_feedback, name='thanks_feedback'),
    path('create_project/', create_project, name='create_project'),
    path('send_message/', send_message, name='send_message'),
    path('inbox/', inbox, name='inbox'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('messages/unread', views.unread_messages, name='unread_messages'),
]
