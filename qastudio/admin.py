from django.contrib import admin

from .models import AuditEntry, CertificationEvent, QuestionSample, ReviewerProfile, SkillCertification


@admin.register(ReviewerProfile)
class ReviewerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'all_skills', 'grades')
    list_filter = ('role', 'all_skills')
    filter_horizontal = ('skills', 'domains')


@admin.register(SkillCertification)
class SkillCertificationAdmin(admin.ModelAdmin):
    list_display = ('skill', 'state', 'approved_count', 'threshold', 'override', 'certified_at')
    list_filter = ('state', 'override')
    search_fields = ('skill__slug', 'skill__name_fr')
    readonly_fields = ('approved_count', 'state', 'certified_at')


class AuditInline(admin.TabularInline):
    model = AuditEntry
    extra = 0
    readonly_fields = ('user', 'action', 'note', 'created_at')


@admin.register(QuestionSample)
class QuestionSampleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'stale', 'reviewed_by', 'reviewed_at')
    list_filter = ('status', 'stale', 'level', 'skill__domain__grade')
    search_fields = ('skill__slug',)
    readonly_fields = ('payload', 'fingerprint', 'lint')
    inlines = [AuditInline]


@admin.register(CertificationEvent)
class CertificationEventAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'skill', 'event', 'from_state', 'to_state', 'approved', 'threshold', 'webhook_status')
    list_filter = ('event',)
