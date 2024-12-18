# from celery import shared_task
# import time

# @shared_task
# def add(x, y):
#     try:
#         time.sleep(5)  # Simulate a long-running task
#         return x + y 
#     except Exception as e:
#         print(f"Error in task: {e}")
#         raise

# from .models import SSTAnswer
# import random

# @shared_task
# def calculate_sst_score(answer_id):
#     try:
#         # Fetch the SSTAnswer instance by ID
#         answer = SSTAnswer.objects.get(id=answer_id)
        
#         # Calculate scores (simulated for now)
#         # answer.content_score = random.randint(0, 2)
#         # answer.form_score = random.randint(0, 2)
#         # answer.grammar_score = random.randint(0, 2)
#         # answer.vocabulary_score = random.randint(0, 2)
#         # answer.spelling_score = random.randint(0, 2)
#         # answer.total_score = (
#         #     answer.content_score +
#         #     answer.form_score +
#         #     answer.grammar_score +
#         #     answer.vocabulary_score +
#         #     answer.spelling_score
#         # )
        
#         # Save the updated scores
#         # answer.save()

#         answer.calculate_score()

#         return f"Scoring completed for SSTAnswer ID {answer_id} with total score {answer.total_score}"
    
#     except SSTAnswer.DoesNotExist:
#         return f"SSTAnswer ID {answer_id} does not exist"


import threading
import time

class CalculateScoreThread(threading.Thread):
    def __init__(self, sst_answer_id):
        self.sst_answer_id = sst_answer_id
        super().__init__()

    def run(self):
        from .models import SSTAnswer  # Import inside the thread to avoid circular imports
        # time.sleep(5)  # Delay for 5 seconds
        # print("the sleep is over")
        sst_answer = SSTAnswer.objects.get(id=self.sst_answer_id)
        sst_answer.calculate_score()


