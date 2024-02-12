from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import RegisterForm, LoginForm
from .models import User
from home.models import News, Category
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

# Create your views here.
a= 'abc'
print(a)
class UserRegisterView(View):
    form_class = RegisterForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'you are logged in and cannot access this page!', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = User.objects.create_user(
                name=form.cleaned_data.get('name'),
                family=form.cleaned_data.get('family'),
                phone_number=form.cleaned_data.get('phone'),
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password'),
               # role_type= form.cleaned_data.get('role_type'),
                #work_experience=form.cleaned_data.get('work_experience'),
            )
            user.save()
            messages.success(request, 'you registered successfully', 'success')
            return redirect('home:home')

        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    from_class = LoginForm
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'you already logged in!', 'warning')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.from_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.from_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    if user.is_admin:
                        login(request, user)
                        messages.success(request, 'احراز هویت با موفقیت انجام شد', 'success')
                        return redirect('home:index_page')  #home:index_page  #accounts:user_profile
                    else:
                        login(request, user)
                        messages.success(request, 'احراز هویت با موفقیت انجام شد', 'success')
                        return redirect('home:index2_page')
                else:
                    messages.error(request, 'حساب غیرفعال است', 'warning')
            else:
                messages.error(request, 'کاربری با این اطلاعات وجود ندارد', 'warning')

        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'logout was successfully', 'success')
        return redirect('home:home')


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'



class UserProfileView(View):
    def get(self, request, user_email):  # Because we didn't have the id field for the user class,
        user = User.objects.get(email=user_email)    # I used the email field, which is also the primary key
        news = News.objects.filter(register_user=user)
        #category = Category.objects.filter(news_group=category_slug)
        return render(request, 'accounts/profile.html', {'user':user, 'news':news})


