from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_str

success_url = reverse_lazy('login_page')
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView

from apps.forms import CustomUserCreationForm
from apps.models import User
from apps.models.products import Product, Review, Category
from apps.utils import generate_verification_link
from apps.tokens import account_activation_token


# class MainTemplateView(LoginRequiredMixin, TemplateView):
#     template_name = 'apps/dashboard/main.html'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     ctx = super().get_context_data(object_list=object_list, **kwargs)
    #     ctx['categories'] = Category.objects.all()
    #     return ctx


class ProductListView(LoginRequiredMixin, ListView):
    queryset = Product.objects.order_by('-id')
    template_name = 'apps/product/product_list.html'
    context_object_name = 'products'
    paginate_by = 3

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     return super().get_context_data(object_list=object_list, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['categories'] = Category.objects.filter(parent__isnull=True)
        return ctx


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product_detail.html'
    context_object_name = 'product'

    def post(self, request, *args, **kwargs):
        author_id = request.POST.get('author_id')
        product_id = request.POST.get('product_id')
        review_title = request.POST.get('review_title')
        review_text = request.POST.get('review_text')
        Review.objects.create(review_title=review_title, review_text=review_text, author_id=author_id,
                              product_id=product_id)
        return redirect('product_list_page')


class UserProfileTemplateView(TemplateView):
    template_name = 'apps/users/user_profile.html'


class UserSettingsUpdateView(UpdateView):
    model = User
    template_name = 'apps/users/user_settings.html'
    fields = 'first_name', 'last_name', 'email', 'phone', 'profession', 'intro'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('user_profile_page')


class UserPhotoUpdateView(UpdateView):
    model = User
    template_name = 'apps/users/user_settings.html'
    fields = 'photo',

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('user_profile_page')


# class ReviewCreateView(CreateView):
#     template_name = 'apps/product/product_detail.html'
#     queryset = Review.objects.all()
#     fields = 'first_name', 'email', 'title', 'product_id', 'author_id'
#     context_object_name = 'reviews'
#
#     # success_url = reverse_lazy('main_page')
#     def get_success_url(self):
#         return reverse('product_detail_page', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})
#
#     def form_invalid(self, form):
#         return super().form_invalid(form)


# class LoginView(View):
#     def get(self, request):
#         return render(request, 'apps/auth/login/login_page.html')
#
#     def post(self, request):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('main_page')
#         else:
#             return redirect('login_page')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login_page')


class RegisterCreateView(CreateView):
    template_name = 'apps/auth/register/register_page.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user = form.save()
        generate_verification_link(self.request, user)
        text = """
An email has been sent with instructions 
        to verify your email
        """
        messages.add_message(self.request, messages.SUCCESS, text)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


#  EXAMPLE for send message using celery
# def send_message_to_email(request):
#     email = request.GET.get('email')
#     message = 'Salom 21:14 dan'
#     start = time()
#     sent_to_email.delay(message, email)
#     end = time()
#     return JsonResponse({"status": "yuborildi", 'time': f"{end-start} seconds!"})


class VerifyEmailConfirm(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your email has been verified successfully!!!')
            return redirect('login_page')
        else:
            messages.warning(request, 'The link is invalid!!!')
        return redirect('register_page')
