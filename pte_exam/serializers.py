from rest_framework import serializers
from .models import Question, SummarizeSpokenText, SSTAudioFile, ReorderParagraph, ReadingMultipleChoiceQuestion, RMMCQOption

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'question_type']  # Only include the ID, title, and question_type


class SSTAudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSTAudioFile
        fields = ['id', 'file', 'speaker_name']


class ReorderParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReorderParagraph
        fields = ['id', 'content']


class RMMCQOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMMCQOption
        fields = ['id', 'content']


class QuestionDetailSerializer(serializers.ModelSerializer):
    answer_time_limit = serializers.SerializerMethodField()  # Added field for SST
    audios = serializers.SerializerMethodField()
    paragraphs = serializers.SerializerMethodField()
    passage = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'title', 'question_type', 'answer_time_limit', 'audios', 'paragraphs', 'passage', 'options']

    def get_answer_time_limit(self, obj):
        if obj.question_type == 'SST':
            sst = SummarizeSpokenText.objects.filter(question=obj).first()
            if sst:
                return sst.answer_time_limit
        return None
    
    def get_audios(self, obj):
        if obj.question_type == 'SST':
            sst = SummarizeSpokenText.objects.filter(question=obj).first()
            if sst:
                return SSTAudioFileSerializer(sst.audio_files.all(), many=True).data
        return None

    def get_paragraphs(self, obj):
        if obj.question_type == 'RO':
            ro = ReorderParagraph.objects.filter(reorder_question__question=obj)
            return ReorderParagraphSerializer(ro, many=True).data
        return None

    def get_passage(self, obj):
        if obj.question_type == 'RMMCQ':
            rmmcq = ReadingMultipleChoiceQuestion.objects.filter(question=obj).first()
            if rmmcq:
                return rmmcq.passage
        return None

    def get_options(self, obj):
        if obj.question_type == 'RMMCQ':
            rmmcq = ReadingMultipleChoiceQuestion.objects.filter(question=obj).first()
            if rmmcq:
                return RMMCQOptionSerializer(rmmcq.options.all(), many=True).data
        return None
