from rest_framework import serializers
from .models import Question, SummarizeSpokenText, SSTAudioFile, ReorderParagraph, ReorderParagraphQuestion, ReadingMultipleChoiceQuestion, RMMCQOption
from .models import SSTAnswer, ROAnswer, RMMCQAnswer

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



class SubmitAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    # question_type = serializers.ChoiceField(choices=["SST", "RO", "RMMCQ"])
    answer = serializers.JSONField() 

    def validate(self, data):
        # Validate based on question type
        if Question.objects.filter(id=data['question_id']).exists() == False:
            raise serializers.ValidationError("Question not found.")

        question = Question.objects.get(id=data['question_id'])
        question_type = question.question_type

        if question_type == 'SST':
            if not isinstance(data['answer'], str):
                raise serializers.ValidationError("Answer for SST must be a text-based summary.")
            
        elif question_type == 'RO':
            if not isinstance(data['answer'], list) or not all(isinstance(x, int) for x in data['answer']):
                raise serializers.ValidationError("Answer for RO must be a list of paragraph IDs.")
            
            # Get the corresponding ReorderParagraphQuestion
            ro_question = ReorderParagraphQuestion.objects.filter(question=question).first()
            if not ro_question:
                raise serializers.ValidationError("Reorder Paragraph Question not found.")

            # Get the total number of paragraphs for this question
            total_paragraphs = ro_question.paragraphs.count()

            # Check if the length of the answer list matches the total paragraphs
            if len(data['answer']) != total_paragraphs:
                raise serializers.ValidationError(f"The answer must contain exactly {total_paragraphs} paragraph IDs.")

            # Check if all integers are in the range [1, total_paragraphs]
            if not all(1 <= x <= total_paragraphs for x in data['answer']):
                raise serializers.ValidationError(
                    f"All paragraph IDs must be between 1 and {total_paragraphs}."
                )

            # Check for duplicate integers
            if len(data['answer']) != len(set(data['answer'])):
                raise serializers.ValidationError("Invalid answer.")

        elif question_type == 'RMMCQ':
            if not isinstance(data['answer'], list) or not all(isinstance(x, int) for x in data['answer']):
                raise serializers.ValidationError("Answer for RMMCQ must be a list of selected option IDs.")
            
            # Get the corresponding ReadingMultipleChoiceQuestion
            rmmcq_question = ReadingMultipleChoiceQuestion.objects.filter(question=question).first()
            if not rmmcq_question:
                raise serializers.ValidationError("Reading Multiple Choice Question not found.")

            # Get all valid option IDs for this RMMCQ question
            valid_option_ids = list(rmmcq_question.options.values_list('id', flat=True))

            # Check if all selected option IDs exist in this specific RMMCQ question
            if not all(option_id in valid_option_ids for option_id in data['answer']):
                raise serializers.ValidationError("Invalid answer.")

            # Check for duplicate integers
            if len(data['answer']) != len(set(data['answer'])):
                raise serializers.ValidationError("Invalid answer.")
            
        return data

    def create(self, validated_data):
        # question_type = validated_data['question_type']
        question_id = validated_data['question_id']
        answer_data = validated_data['answer']

        question = Question.objects.get(id=question_id)
        question_type = question.question_type

        if question_type == 'SST':
            sst_question = SummarizeSpokenText.objects.get(question=question)
            answer = SSTAnswer.objects.create(
                user=self.context['request'].user,
                question=sst_question,
                text=answer_data
            )
            answer.calculate_score()
            return answer
        
        elif question_type == 'RO':
            ro_question = ReorderParagraphQuestion.objects.get(question=question)
            answer = ROAnswer.objects.create(
                user=self.context['request'].user,
                question=ro_question,
                paragraph_order=answer_data
            )
            answer.calculate_score()
            return answer
        
        elif question_type == 'RMMCQ':
            rmmcq_question = ReadingMultipleChoiceQuestion.objects.get(question=question)
            selected_options = RMMCQOption.objects.filter(id__in=answer_data)
            answer = RMMCQAnswer.objects.create(
                user=self.context['request'].user,
                question=rmmcq_question
            )
            answer.selected_options.set(selected_options)
            answer.calculate_score()
            return answer