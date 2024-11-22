from django.db import models
from django.contrib.auth.models import User
from random import randint
from django.utils import timezone


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


class Answer(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="answers")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Answer by {self.user} for Question {self.question.title}"


class SSTAnswer(models.Model):
    """
    Model for storing answers to Summarize Spoken Text (SST) questions.
    """
    answer = models.OneToOneField("Answer", on_delete=models.CASCADE, related_name="sst_answer_details")
    question = models.ForeignKey("SummarizeSpokenText", on_delete=models.CASCADE, related_name="answers")
    text = models.TextField(help_text="Student's text-based summary.")
    content_score = models.IntegerField(default=0, help_text="Score for content (max 2).")
    form_score = models.IntegerField(default=0, help_text="Score for form (max 2).")
    grammar_score = models.IntegerField(default=0, help_text="Score for grammar (max 2).")
    vocabulary_score = models.IntegerField(default=0, help_text="Score for vocabulary (max 2).")
    spelling_score = models.IntegerField(default=0, help_text="Score for spelling (max 2).")
    total_score = models.IntegerField(default=0, help_text="Total score out of 10.")

    def calculate_score(self):
        """
        Fake scoring logic for SST. Generate random scores for components.
        """
        self.content_score = randint(0, 2)
        self.form_score = randint(0, 2)
        self.grammar_score = randint(0, 2)
        self.vocabulary_score = randint(0, 2)
        self.spelling_score = randint(0, 2)
        self.total_score = (
            self.content_score + self.form_score +
            self.grammar_score + self.vocabulary_score +
            self.spelling_score
        )
        self.save()

    def get_score_components(self):
        return {
            "Content": {"score": self.content_score, "max_score": 2},
            "Form": {"score": self.form_score, "max_score": 2},
            "Grammar": {"score": self.grammar_score, "max_score": 2},
            "Vocabulary": {"score": self.vocabulary_score, "max_score": 2},
            "Spelling": {"score": self.spelling_score, "max_score": 2},
            "Total": {"score": self.total_score, "max_score": 10},
        }

    def __str__(self):
        return f"Answer by {self.answer.user} for SST {self.question.question.title}"

class ROAnswer(models.Model):
    """
    Model for storing answers to Re-Order Paragraph (RO) questions.
    """
    answer = models.OneToOneField("Answer", on_delete=models.CASCADE, related_name="ro_answer_details")
    question = models.ForeignKey("ReorderParagraphQuestion", on_delete=models.CASCADE, related_name="answers")
    paragraph_order = models.JSONField(help_text="Submitted order of paragraphs.")
    total_score = models.IntegerField(default=0, help_text="Total score based on correct adjacent pairs.")

    def calculate_score(self):
        """
        Scoring logic for RO. Score based on the number of correct adjacent pairs.
        """
        next_correct_order = list(
            self.question.paragraphs.order_by("id").values_list("correct_next_order", flat=True)
        )
        submitted_order = self.paragraph_order
        correct_pairs = 0

        # Count the number of correct adjacent pairs
        for i in range(len(submitted_order) - 1):
            if (next_correct_order[submitted_order[i] - 1] == submitted_order[i + 1]):
                correct_pairs += 1

        self.total_score = correct_pairs
        self.save()

    def get_score_components(self):
        return {
            "Blank": {"score": self.total_score, "max_score": len(self.paragraph_order) - 1}
        }

    def __str__(self):
        return f"Answer by {self.answer.user} for RO {self.question.question.title}"


class RMMCQAnswer(models.Model):
    """
    Model for storing answers to Reading Multiple Choice (RMMCQ) questions.
    """
    answer = models.OneToOneField("Answer", on_delete=models.CASCADE, related_name="rmmcq_answer_details")
    question = models.ForeignKey("ReadingMultipleChoiceQuestion", on_delete=models.CASCADE, related_name="answers")
    selected_options = models.ManyToManyField("RMMCQOption", related_name="answers", help_text="Selected options by the user.")
    total_score = models.IntegerField(default=0, help_text="Total score for the question.")

    def calculate_score(self):
        """
        Scoring logic for RMMCQ. Add 1 for each correct option and subtract 1 for incorrect ones.
        """
        correct_options = self.question.options.filter(is_correct=True).values_list("id", flat=True)
        selected_options = self.selected_options.values_list("id", flat=True)
        
        score = 0
        for option in selected_options:
            if option in correct_options:
                score += 1
            else:
                score -= 1

        self.total_score = max(0, score)  # Ensure minimum score is 0
        self.save()

    def get_score_components(self):
        correct_count = self.question.options.filter(is_correct=True).count()
        return {
            "Choice": {"score": self.total_score, "max_score": correct_count},
        }

    def __str__(self):
        return f"Answer by {self.answer.user} for RMMCQ {self.question.question.title}"
