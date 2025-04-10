from django.db import models
from django.db import transaction
import uuid

class Candidate(models.Model):
    POSITION_CHOICES = [
        ('Web Developer', 'Web Developer'),
        ('Software Engineer', 'Software Engineer'),
        ('Digital Marketing Executive', 'Digital Marketing Executive'),
        ('Cyber Security Analyst', 'Cyber Security Analyst'),
        ('HR Executive', 'HR Executive'),
        ('Graphic Designer', 'Graphic Designer'),
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    institution = models.CharField(max_length=100)
    year_passing = models.CharField(max_length=4)
    specialization = models.CharField(max_length=100)
    skills = models.TextField(null=True, blank=True)
    resume = models.FileField(upload_to='resumes/')
    certifications = models.FileField(upload_to='certifications/', null=True, blank=True)
    candidate_code = models.CharField(max_length=10, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.candidate_code:
            with transaction.atomic():
                last_candidate = Candidate.objects.select_for_update().order_by('-id').first()
                number = (last_candidate.id + 1) if last_candidate else 1
                self.candidate_code = f'RBS{number}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.candidate_code

class CustomCandidateForm(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=Candidate.GENDER_CHOICES, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=50, choices=Candidate.POSITION_CHOICES, blank=True, null=True)
    institution = models.CharField(max_length=100, blank=True, null=True)
    year_passing = models.CharField(max_length=4, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Custom Form - {self.token}"

class GroupDiscussion(models.Model):
    STATUS_CHOICES = [
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('On Hold', 'On Hold'),
    ]
    
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    interview_date = models.DateTimeField()
    interviewer_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    marks = models.IntegerField()

    def __str__(self):
        return f"GD - {self.candidate.candidate_code}"

class TechnicalRound(models.Model):
    STATUS_CHOICES = [
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('On Hold', 'On Hold'),
    ]
    
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    interview_date = models.DateTimeField()
    interviewer_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    marks = models.IntegerField()

    def __str__(self):
        return f"TR - {self.candidate.candidate_code}"

class HRRound(models.Model):
    STATUS_CHOICES = [
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('On Hold', 'On Hold'),
    ]
    
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    interview_date = models.DateTimeField()
    interviewer_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    marks = models.IntegerField()

    def __str__(self):
        return f"HR - {self.candidate.candidate_code}"