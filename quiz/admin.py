from django.contrib import admin
from .models import (QuizSet, Question, Choice, Pair, StudentSession, Student, ProblemInteraction,
                     SkillDomain, Skill)


# ── Skill taxonomy ───────────────────────────────────────────────────────────

class SkillInline(admin.TabularInline):
    model = Skill
    fields = ['order', 'slug', 'name_en', 'name_fr', 'answer_type', 'is_active']
    extra = 0
    show_change_link = True
    ordering = ['order', 'id']


@admin.register(SkillDomain)
class SkillDomainAdmin(admin.ModelAdmin):
    list_display  = ['icon', 'name_en', 'name_fr', 'grade', 'order', 'skill_count']
    list_display_links = ['name_en']
    list_editable = ['order']
    list_filter   = ['grade']
    search_fields = ['name_en', 'name_fr', 'slug']
    inlines       = [SkillInline]

    @admin.display(description='Skills')
    def skill_count(self, obj):
        return obj.skills.count()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display  = ['slug', 'name_en', 'name_fr', 'domain', 'answer_type', 'has_description', 'is_active']
    list_filter   = ['domain__grade', 'domain', 'answer_type', 'is_active']
    search_fields = ['slug', 'name_en', 'name_fr', 'description_en', 'description_fr', 'keywords_en', 'keywords_fr']
    autocomplete_fields = ['prereq', 'next_skill', 'mastery_next', 'downgrade']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        (None, {'fields': ['slug', 'domain', 'order', 'is_active', ('name_en', 'name_fr')]}),
        ('What the exercise looks like (used by AI search & classification)', {
            'fields': ['description_en', 'description_fr', 'keywords_en', 'keywords_fr', 'curriculum_ref']}),
        ('Answers & generation', {'fields': ['answer_type', 'generator_slug']}),
        ('Learning path', {'fields': ['prereq', 'next_skill', 'mastery_next', 'downgrade', 'level_sequence']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at'], 'classes': ['collapse']}),
    ]

    @admin.display(boolean=True, description='Described')
    def has_description(self, obj):
        return bool(obj.description_en or obj.description_fr)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class PairInline(admin.TabularInline):
    model = Pair
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display  = ['order', 'q_type', 'prompt_en', 'points', 'time_limit']
    list_filter   = ['q_type', 'quiz_set']
    inlines       = [ChoiceInline, PairInline]


class QuestionInline(admin.StackedInline):
    model  = Question
    extra  = 1
    show_change_link = True


@admin.register(QuizSet)
class QuizSetAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'created_at']
    inlines      = [QuestionInline]


@admin.register(StudentSession)
class StudentSessionAdmin(admin.ModelAdmin):
    list_display = ['quiz_set', 'started_at', 'score', 'max_score', 'language']
    readonly_fields = ['answers']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display  = ['user', 'avatar_slug', 'total_stars', 'created_at']
    readonly_fields = ['skill_ratings', 'created_at']


@admin.register(ProblemInteraction)
class ProblemInteractionAdmin(admin.ModelAdmin):
    list_display  = ['user', 'topic', 'level', 'is_correct', 'points_earned', 'created_at']
    list_filter   = ['topic', 'level', 'is_correct']
    readonly_fields = ['created_at']
