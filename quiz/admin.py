from django.contrib import admin
from .models import QuizSet, Question, Choice, Pair, StudentSession, Student, ProblemInteraction


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
