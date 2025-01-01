from django.shortcuts import render, redirect
from .forms import *
from .models import Account, CustomPasswordException
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required


# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



def home(request):

    return render(request, 'base/index.html')



def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                phone_number = form.cleaned_data['phone_number']
                username = email.split("@")[0]
                user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                                  username=username, password=password)
                user.phone_number = phone_number
                user.save()
                messages.success(request, 'You have Been Registered, Check Your Email to Confirm Registration')
                return redirect('login')
            except CustomPasswordException as e:
                messages.error(request, str(e))
                return redirect('register')
        else:
            messages.error(request, str(form.errors))
            return redirect('register')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'base/register_new.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request=request, user=user)
            messages.success(request, 'You Logged In Succesfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials!')
            return redirect('login')
    return render(request, 'base/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')



def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('base/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'base/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'base/resetPassword.html')
    



    
# ===================== FIXME (FOR FUTURE USES) ===========================

# @login_required(login_url='login')
# def view_profile(request):
#     user = Account.objects.get(id=request.user.id)
#     return render(request, 'base/profile.html', {'user': user})


# @login_required(login_url='login')
# def edit_profile(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST,request.FILES, instance=request.user)
#         if user_form.is_valid():
#             user_form.save()
#             messages.success(request, 'Your profile has been updated.')
#             return redirect('edit_profile')
#     else:
#         user_form = UserForm(instance=request.user)
#     context = {
#         'form': user_form,
#     }
#     return render(request, 'base/edit_profile.html', context)


# @login_required(login_url='login')
# def change_password(request):
#     if request.method == 'POST':
#         current_password = request.POST['current_password']
#         new_password = request.POST['new_password']
#         confirm_password = request.POST['confirm_password']

#         user = Account.objects.get(username__exact=request.user.username)

#         if new_password == confirm_password:
#             success = user.check_password(current_password)
#             if success:
#                 user.set_password(new_password)
#                 user.save()
#                 messages.success(request, 'Password updated successfully.')
#                 return redirect('change_password')
#             else:
#                 messages.error(request, 'Please enter valid current password')
#                 return redirect('change_password')
#         else:
#             messages.error(request, 'Password does not match!')
#             return redirect('change_password')
#     return render(request, 'base/change_password.html')

