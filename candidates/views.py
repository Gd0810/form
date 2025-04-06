from django.shortcuts import render, redirect, get_object_or_404
from .forms import CandidateForm, CustomPrefilledCandidateForm
from .models import Candidate, CustomCandidateForm
from django.core.mail import send_mail
from django.conf import settings

def candidate_form(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            # Send email synchronously
            subject = 'Your Candidate Code'
            message = f'Hi {candidate.full_name},\n\nYour candidate code is: {candidate.candidate_code}\nPlease save it.'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [candidate.email])
            return redirect('welcome', candidate_code=candidate.candidate_code)
    else:
        form = CandidateForm()
    return render(request, 'form.html', {'form': form})

def custom_prefilled_form(request, token):
    custom_form = get_object_or_404(CustomCandidateForm, token=token)
    if request.method == 'POST':
        form = CustomPrefilledCandidateForm(custom_form, request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            # Send email synchronously
            subject = 'Your Candidate Code'
            message = f'Hi {candidate.full_name},\n\nYour candidate code is: {candidate.candidate_code}\nPlease save it.'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [candidate.email])
            return redirect('welcome', candidate_code=candidate.candidate_code)
    else:
        form = CustomPrefilledCandidateForm(custom_form)  # Pass custom_form for initial values
    return render(request, 'form.html', {'form': form})

def welcome(request, candidate_code):
    candidate = Candidate.objects.get(candidate_code=candidate_code)
    return render(request, 'welcome.html', {'candidate': candidate})