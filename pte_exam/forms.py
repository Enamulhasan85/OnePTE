# from django import forms
# from .models import ReorderParagraph


# class ReorderParagraphAdminForm(forms.ModelForm):
#     class Meta:
#         model = ReorderParagraph
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         # Check if reorder_question is set, and filter correct_next accordingly
#         if self.instance.reorder_question:
#             self.fields['correct_next'].queryset = ReorderParagraph.objects.filter(
#                 reorder_question=self.instance.reorder_question
#             )
#         else:
#             self.fields['correct_next'].queryset = ReorderParagraph.objects.none()

