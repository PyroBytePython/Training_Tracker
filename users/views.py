import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, UpdateView, DetailView
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect

from Tracker.models import Workout, Exercise
from users.forms import UserRegisterForm, ProfileForm
from .models import User, VerificationCode, UserProfile
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


class ProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Общее число тренировок пользователя
        total_workouts = Workout.objects.filter(user=self.request.user).count()

        # Считаем распределение по группам мышц из Exercise
        # (каждое упражнение относится к одной группе)
        exercises_qs = (
            Exercise.objects
            .filter(workout__user=self.request.user)
            .values('muscle_group')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # Преобразуем к "человеческим" названиям (choices)
        label_map = dict(Exercise.MUSCLE_GROUPS)  # {'chest': 'Грудь', ...}
        labels = [label_map.get(item['muscle_group'], 'Другое') for item in exercises_qs]
        counts = [item['count'] for item in exercises_qs]

        # Переводим в проценты (за всё время)
        total_exercises = sum(counts)
        if total_exercises > 0:
            percentages = [round(c * 100 / total_exercises, 1) for c in counts]
        else:
            percentages = []
            labels = []

        context.update({
            'total_workouts': total_workouts,
            'muscle_labels': json.dumps(labels, ensure_ascii=False),
            'muscle_percentages': json.dumps(percentages),
            'muscle_data': list(zip(labels, percentages)),
        })
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user.userprofile