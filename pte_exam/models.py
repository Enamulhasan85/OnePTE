from django.db import models
from django.contrib.auth.models import User
from random import randint


class Question(models.Model):
    QUESTION_TYPES = (
        ('SST', 'Summarize Spoken Text'),
        ('RO', 'Re-Order Paragraph'),
        ('RMMCQ', 'Reading Multiple Choice (Multiple)'),
    )
    title = models.CharField(max_length=255)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)

    def __str__(self):
        return f"{self.get_question_type_display()}: {self.title}"


class SummarizeSpokenText(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='sst_details')
    answer_time_limit = models.PositiveIntegerField(help_text="Time limit in seconds")

    def __str__(self):
        return self.question.title


class SSTAudioFile(models.Model):
    sst_question = models.ForeignKey(SummarizeSpokenText, on_delete=models.CASCADE, related_name='audio_files')
    file = models.FileField(upload_to='audio_files/')
    speaker_name = models.CharField(max_length=255)

    def __str__(self):
        return self.speaker_name


class ReorderParagraphQuestion(models.Model): 
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='reorder_paragraph_details')

    def __str__(self):
        return self.question.title


class ReorderParagraph(models.Model):  
    reorder_question = models.ForeignKey(ReorderParagraphQuestion, on_delete=models.CASCADE, related_name='paragraphs')
    content = models.TextField(help_text="Content of the paragraph")
    correct_next_order = models.PositiveIntegerField(null=True, blank=True, help_text="Order of the correct next paragraph")

    def __str__(self):
        return f"{self.content[:50]}..."  # Show only the first 50 chars


class ReadingMultipleChoiceQuestion(models.Model): 
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='rmmcq_details')
    passage = models.TextField(help_text="Passage for the RMMCQ question")

    def __str__(self):
        return self.question.title


class RMMCQOption(models.Model):  
    rmmcq_question = models.ForeignKey(ReadingMultipleChoiceQuestion, on_delete=models.CASCADE, related_name='options')
    content = models.TextField(help_text="Option text")
    is_correct = models.BooleanField(default=False, help_text="Indicates if this option is correct")

    def __str__(self):
        return f"Option: {self.content[:50]} (Correct: {self.is_correct})"


