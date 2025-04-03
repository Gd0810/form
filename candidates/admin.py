from django.contrib import admin
from .models import Candidate, GroupDiscussion, TechnicalRound, HRRound

class GroupDiscussionAdmin(admin.ModelAdmin):
    list_display = ('candidate_code', 'interview_date', 'interviewer_name', 'status', 'marks')
    list_filter = ('status',)
    search_fields = ('candidate__full_name', 'candidate__candidate_code', 'candidate__email')
    
    def candidate_code(self, obj):
        return obj.candidate.candidate_code
    candidate_code.short_description = 'Candidate Code'

class TechnicalRoundAdmin(admin.ModelAdmin):
    list_display = ('candidate_code', 'interview_date', 'interviewer_name', 'status', 'marks')
    list_filter = ('status',)
    search_fields = ('candidate__full_name', 'candidate__candidate_code', 'candidate__email')
    
    def candidate_code(self, obj):
        return obj.candidate.candidate_code
    candidate_code.short_description = 'Candidate Code'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        shortlisted_candidates = GroupDiscussion.objects.filter(status='Shortlisted').values_list('candidate_id', flat=True)
        return qs.filter(candidate_id__in=shortlisted_candidates)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "candidate":
            shortlisted_candidates = GroupDiscussion.objects.filter(status='Shortlisted').values_list('candidate_id', flat=True)
            kwargs["queryset"] = Candidate.objects.filter(id__in=shortlisted_candidates)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class HRRoundAdmin(admin.ModelAdmin):
    list_display = ('candidate_code', 'interview_date', 'interviewer_name', 'status', 'marks')
    list_filter = ('status',)
    search_fields = ('candidate__full_name', 'candidate__candidate_code', 'candidate__email')
    
    def candidate_code(self, obj):
        return obj.candidate.candidate_code
    candidate_code.short_description = 'Candidate Code'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        shortlisted_candidates = TechnicalRound.objects.filter(status='Shortlisted').values_list('candidate_id', flat=True)
        return qs.filter(candidate_id__in=shortlisted_candidates)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "candidate":
            shortlisted_candidates = TechnicalRound.objects.filter(status='Shortlisted').values_list('candidate_id', flat=True)
            kwargs["queryset"] = Candidate.objects.filter(id__in=shortlisted_candidates)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'candidate_code', 'email', 'position', 'current_stage', 'current_status')
    search_fields = ('full_name', 'candidate_code', 'email')
    
    def current_stage(self, obj):
        if obj.hrround_set.exists():
            return 'HR Round'
        elif obj.technicalround_set.exists():
            return 'Technical Round'
        elif obj.groupdiscussion_set.exists():
            return 'Group Discussion'
        return 'Not Started'
    
    def current_status(self, obj):
        if obj.hrround_set.exists():
            return obj.hrround_set.last().status
        elif obj.technicalround_set.exists():
            return obj.technicalround_set.last().status
        elif obj.groupdiscussion_set.exists():
            return obj.groupdiscussion_set.last().status
        return 'Pending'

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(GroupDiscussion, GroupDiscussionAdmin)
admin.site.register(TechnicalRound, TechnicalRoundAdmin)
admin.site.register(HRRound, HRRoundAdmin)