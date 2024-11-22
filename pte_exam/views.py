from rest_framework import generics, status
from .models import Question
from .serializers import QuestionSerializer, QuestionDetailSerializer, SubmitAnswerSerializer
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned questions to a given question type,
        by filtering against a `question_type` query parameter in the URL.
        """
        queryset = self.queryset
        question_type = self.request.query_params.get('question_type', None)
        if question_type is not None:
            queryset = queryset.filter(question_type=question_type)
        return queryset
    


class QuestionDetailView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer

    def get_object(self):
        question_id = self.kwargs.get('pk')
        try:
            return Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise NotFound("Question not found")



class SubmitAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Create the serializer with the request data
        serializer = SubmitAnswerSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # If the data is valid, save the answer and return the response
            answer = serializer.save()
            return Response({
                "message": "Answer submitted successfully.",
                "data": {
                    "id": answer.id,
                    "question_id": answer.question.id,
                    "question_type": answer.question.question.question_type,
                    "score_components": answer.get_score_components()
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
