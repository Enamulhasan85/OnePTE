from rest_framework import generics, status
from .models import Question
from .serializers import *
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
# from .tasks import add

class QuestionListView(generics.ListAPIView):
    # print(add.delay(3, 5))

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
            message = ""
            data = {
                "id": answer.answer.id,
                "question_id": answer.question.question.id,
                "question_type": answer.question.question.question_type,
                "question_type_display": answer.question.question.get_question_type_display(),
            }
            if answer.question.question.question_type != "SST":
                data["score_components"] = answer.get_score_components()
                message =  "Answer submitted successfully."
            else:
                message =  "Answer submitted successfully. Your score will be available soon."

            return Response({
                "message": message,
                "data": data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PracticeHistoryView(APIView):

    class CustomPagination(PageNumberPagination):
        page_size = 10  # Number of items per page
        page_size_query_param = 'page_size'  # Optional: Allow the client to set the page size
        max_page_size = 50  # Optional: Limit the max page size for large queries


    def get(self, request):
        """
        Retrieve the practice history of a specific user.
        """

        # Retrieve all answers submitted by the user
        answers = Answer.objects.filter(user=request.user)
        question_type = request.query_params.get('question_type', None)
        if question_type is not None:
            answers = answers.filter(question__question_type=question_type)
        answers = answers.order_by("-created_at")

        # Apply pagination
        paginator = self.CustomPagination()
        answers = paginator.paginate_queryset(answers, request)

        history = []

        # Iterate through each answer to build the response
        for answer in answers:
            answer_details = {
                "id": answer.id,
                "question_id": answer.question.id,
                "question_title": answer.question.title,
                "question_type": answer.question.question_type,
                "question_type_display": answer.question.get_question_type_display(),
                "submitted_at": answer.created_at,
            }

            if answer.question.question_type == "SST":
                answer_details["score"] = answer.sst_answer_details.get_score_components()
                # sst_answer = SSTAnswer.objects.filter(answer=answer).first()
                # if sst_answer:
                    # answer_details["submitted_answer"] = sst_answer.text

            elif answer.question.question_type == "RO":
                answer_details["score"] = answer.ro_answer_details.get_score_components()

            elif answer.question.question_type == "RMMCQ":                
                answer_details["score"] = answer.rmmcq_answer_details.get_score_components()
                # rmmcq_answer = RMMCQAnswer.objects.filter(answer=answer).first()
                # if rmmcq_answer:
                #     selected_options = rmmcq_answer.selected_options.values_list("id", flat=True)
                #     answer_details["submitted_answer"] = list(selected_options)
                #     answer_details["score"] = rmmcq_answer.get_score_components()

            history.append(answer_details)

        history = paginator.get_paginated_response(history)

        return history
