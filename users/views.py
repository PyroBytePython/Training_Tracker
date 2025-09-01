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

    def get_initial(self):
        """Заполняем форму старыми данными из сессии, если они есть"""
        initial = super().get_initial()
        pending = self.request.session.get("pending_user")
        if pending:
            initial["username"] = pending.get("username", "")
            initial["email"] = pending.get("email", "")
        return initial

    def form_valid(self, form):
        # сохраняем данные во временную сессию
        self.request.session['pending_user'] = {
            'username': form.cleaned_data['username'],
            'email': form.cleaned_data['email'],
            'password': form.cleaned_data['password1'],
        }

        # создаем код
        code = VerificationCode.generate_raw_code()
        self.request.session['pending_code'] = code

        # отправляем письмо
        send_verification_email(
            form.cleaned_data['email'],
            form.cleaned_data['username'],
            code
        )
        return redirect(self.success_url)


class VerifyView(View):
    template_name = 'users/verify.html'

    def get(self, request):
        pending = request.session.get('pending_user')
        if not pending:
            return redirect('users:register')
        return render(request, self.template_name, {"email": pending["email"]})

    def post(self, request):
        pending = request.session.get('pending_user')
        code = request.POST.get('code')

        if not pending or not code:
            return redirect('users:register')

        # сверяем с сохранённым кодом
        if code == request.session.get('pending_code'):
            user = User.objects.create_user(
                username=pending['username'],
                email=pending['email'],
                password=pending['password']
            )
            user.is_verified = True
            user.save()

            # очищаем сессию
            request.session.pop('pending_user', None)
            request.session.pop('pending_code', None)

            login(request, user)
            messages.success(request, 'Email успешно подтвержден!')
            return redirect('tracker:menu')

        messages.error(request, 'Неверный код подтверждения')
        return render(request, self.template_name, {"email": pending["email"]})


class ResendCodeView(View):
    def get(self, request):
        pending = request.session.get('pending_user')
        if not pending:
            return redirect('users:register')

        # обновляем код
        new_code = VerificationCode.generate_raw_code()
        request.session['pending_code'] = new_code

        # отправляем на email
        send_verification_email(
            pending['email'],
            pending['username'],
            new_code
        )
        messages.success(request, 'Новый код отправлен на ваш email')

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
