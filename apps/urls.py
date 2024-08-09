from django.contrib.auth.views import LoginView
from django.urls import path

from apps.views import ProductListView, RegisterCreateView, LogoutView, VerifyEmailConfirm, \
    ProductDetailView, UserProfileTemplateView, UserSettingsUpdateView

urlpatterns = [

    # path('', MainTemplateView.as_view(), name='main_page'),
    path('', ProductListView.as_view(), name='product_list_page'),
    path('product-detail/<int:pk>', ProductDetailView.as_view(), name='product_detail_page'),
    path('login', LoginView.as_view(template_name='apps/auth/login/login_page.html',
                                    redirect_authenticated_user=True,
                                    next_page='product_list_page'), name='login_page'),
    path('logout', LogoutView.as_view(), name="logout_page"),
    path('user-profile', UserProfileTemplateView.as_view(), name="user_profile_page"),
    path('user-settings', UserSettingsUpdateView.as_view(), name="user_settings_page"),
    path('user-update-photo', UserSettingsUpdateView.as_view(), name="user_update_photo_page"),
    path('register', RegisterCreateView.as_view(), name='register_page'),
    path('verify-email-confirm/<uidb64>/<token>/', VerifyEmailConfirm.as_view(), name='verify-email-confirm'),

]

# path('email', send_message_to_email, name='email_page')
# path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
# path('verify-email/done/', VerifyEmailDone.as_view(), name='verify-email-done'),
# path('verify-email/complete/', VerifyEmailComplete.as_view(), name='verify-email-complete'),
