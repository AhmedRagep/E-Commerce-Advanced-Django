from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('register', views.register, name='register'),

    # email_verification

    # لارسال التشفير والتوكن في الرابط
    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email_verification'),

    path('email-verification-sent', views.email_verification_sent, name='email_verification_sent'),

    path('email-verification-success', views.email_verification_success, name='email_verification_success'),

    path('email-verification-failed', views.email_verification_failed, name='email_verification_failed'),

    
    path('my-login', views.my_login, name='my_login'),

    path('user-logout', views.user_logout, name='user_logout'),


    path('dashboard', views.dashboard, name='dashboard'),

    # profile management

    path('profile-management', views.profile_management, name='profile_management'),

    path('delete-account', views.delete_account, name='delete_account'),

    # password reseat management

    # 1 ) اعادة تعيين كلمة المرور
    path('reset_password', auth_views.PasswordResetView.as_view(template_name='account/password/password-reset.html'), name='reset_password'),

    # 2 ) صفحة لعرض انه تم ارسال التحقق للبريد الالكتروني
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='account/password/password-reset-sent.html'), name='password_reset_done'),

    # 3 ) رابط التحقق
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password/password-reset-form.html'), name='password_reset_confirm'),
    
    # 4 ) تم تغيير الباسورد
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='account/password/password-reset-complete.html'), name='password_reset_complete'),


    # manage shipping
    path("manage-shipping", views.manage_shipping, name="manage-shipping"),

    # Track order
    path('track_order', views.track_order, name='track_order'),

]



