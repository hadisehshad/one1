from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name', 'family', 'phone_number', 'role_type', 'work_experience')

    def clean_password2(self):    #Comparing the equality of password2 with password1
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match')
        return cd['password2']

    def save(self, commit=True):    #First, we hash the passwords and then save them
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="you can change password using <a href=\"../password/\">this form</a>.")

    class Meta:
        model = User
        fields = ('email', 'name', 'family', 'phone_number', 'password', 'last_login', 'role_type', 'work_experience')


class RegisterForm(forms.Form):
    name = forms.CharField(label="نام", widget=forms.TextInput(attrs={'class': 'form-control _p_dir_ltr'}))
    family = forms.CharField(label="نام خانوادگی", widget=forms.TextInput(attrs={'class': 'form-control _p_dir_ltr'}))

    phone = forms.CharField(max_length=11, label="شماره تلفن",
                            widget=forms.TextInput(attrs={'class': 'form-control _p_dir_ltr'}))

    email = forms.EmailField(label="آدرس ایمیل" ,
                             widget=forms.EmailInput(attrs={'class': 'form-control _p_dir_ltr', 'type': 'email',
                                                            'placeholder': 'test@gmail.com'}))

    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={
                            'type': 'password', 'class': 'form-control _p_dir_ltr'}))

    #role_type = forms.IntegerField(label="نوع کاربر", initial=3,  widget=forms.NumberInput(attrs={
                                      #'class': 'form-control _p_dir_ltr'}))

    #work_experience = forms.CharField(max_length=100, label="سابقه کاری", initial='REGULAR_USER',
                                      #help_text='این فیلد به کاربران ویژه اختصاص دارد', widget=forms.TextInput
                                      #(attrs={'class': 'form-control _p_dir_ltr'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user1 = User.objects.filter(email=email).exists()
        if user1:
            raise ValidationError('this email already exists')
        return email


class LoginForm(forms.Form):
   email = forms.EmailField(label='آدرس ایمیل', widget=forms.EmailInput(
                        attrs={'class': 'form-control _p_dir_ltr', 'placeholder': 'test@gmail.com'}))

   # phone = forms.CharField(label='شماره تلفن', widget=forms.TextInput(
        #attrs={'class': 'form-control _p_dir_ltr'}))

   password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(
                        attrs={'class': 'form-control _p_dir_ltr'}))