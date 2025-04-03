from django.shortcuts import render, redirect
from .forms import CandidateForm
from .models import Candidate
from django.core.mail import send_mail
from django.conf import settings

def candidate_form(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            # Send email
            subject = 'Your Candidate Code'
            message = f'Hi {candidate.full_name},\n\nYour candidate code is: {candidate.candidate_code}\nPlease save it.'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [candidate.email])
            return redirect('welcome', candidate_code=candidate.candidate_code)
    else:
        form = CandidateForm()
    return render(request, 'form.html', {'form': form})

def welcome(request, candidate_code):
    candidate = Candidate.objects.get(candidate_code=candidate_code)
    return render(request, 'welcome.html', {'candidate': candidate})