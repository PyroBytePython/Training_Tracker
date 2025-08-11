from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect

from users.forms import UserRegisterForm
from .models import User, VerificationCode
from .services import send_verification_email


class RegisterCreateView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:verify')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        code_obj = VerificationCode.generate_code(user)
        send_verification_email(user, code_obj.code)
        self.request.session['verify_user_id'] = user.id
        return response


class VerifyView(View):
    template_name = 'users/verify.html'

    def get(self, request):
        if not request.session.get('verify_user_id'):
            return redirect('users:register')
        return render(request, self.template_name)

    def post(self, request):
        user_id = request.session.get('verify_user_id')
        code = request.POST.get('code')

        if not user_id or not code:
            return redirect('users:register')

        try:
            user = User.objects.get(id=user_id)
            code_obj = VerificationCode.objects.filter(
                user=user,
                code=code,
                is_used=False
            ).latest('created_at')

            if code_obj:
                user.is_verified = True
                user.save()
                code_obj.is_used = True
                code_obj.save()
                del request.session['verify_user_id']
                login(request, user)
                messages.success(request, 'Email успешно подтвержден!')
                return redirect('tracker:menu')

        except (User.DoesNotExist, VerificationCode.DoesNotExist):
            pass

        messages.error(request, 'Неверный код подтверждения')
        return render(request, self.template_name)


class ResendCodeView(View):
    def get(self, request):
        user_id = request.session.get('verify_user_id')
        if not user_id:
            return redirect('users:register')

        try:
            user = User.objects.get(id=user_id)
            VerificationCode.objects.filter(user=user).update(is_used=True)
            code_obj = VerificationCode.generate_code(user)
            send_verification_email(user, code_obj.code)
            messages.success(request, 'Новый код отправлен на ваш email')
        except User.DoesNotExist:
            pass

        return redirect('users:verify')
