from django.contrib import admin
from .models import Question, SummarizeSpokenText, SSTAudioFile, ReorderParagraphQuestion, ReorderParagraph, ReadingMultipleChoiceQuestion, RMMCQOption

# admin.site.register(Question)
# admin.site.register(SummarizeSpokenText)
# admin.site.register(SSTAudioFile)
# admin.site.register(ReorderParagraphQuestion)
# admin.site.register(ReorderParagraph)
# admin.site.register(ReadingMultipleChoiceQuestion)
# admin.site.register(RMMCQOption)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'question_type')
    list_filter = ('question_type',)
    search_fields = ('title',)


class SSTAudioFileInline(admin.TabularInline):
    model = SSTAudioFile
    extra = 1  # Number of empty forms to display by default


@admin.register(SummarizeSpokenText)
class SummarizeSpokenTextAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer_time_limit')
    inlines = [SSTAudioFileInline]


class ReorderParagraphInline(admin.TabularInline):
    model = ReorderParagraph
    extra = 1  # Number of empty forms to display by default


@admin.register(ReorderParagraphQuestion)
class ReorderParagraphQuestionAdmin(admin.ModelAdmin):
    list_display = ('question',)
    inlines = [ReorderParagraphInline]


class RMMCQOptionInline(admin.TabularInline):
    model = RMMCQOption
    extra = 2  # Number of empty option forms to display


@admin.register(ReadingMultipleChoiceQuestion)
class ReadingMultipleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('question',)
    inlines = [RMMCQOptionInline]



