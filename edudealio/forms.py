from django import forms
from .models import *
from django.forms import formset_factory

class SubjectPercentageForm(forms.ModelForm):
    class Meta:
        model = StudentSubjectModel
        fields = ['subject', 'percentage']

class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentModel
        fields = [
            'roll_number', 
            'semester',
            'student_class', 
            'subjects', 
            'exam_certificate', 
            'school']

class CustomSchoolForm(forms.ModelForm):
    class Meta:
        model = StudentModel
        fields = ['custom_school_name']

SubjectPercentageFormSet = formset_factory(SubjectPercentageForm, extra=0)

class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = QuestionnaireModel
        fields = ['question_class','topic']
        widgets = {
            'question_class': forms.Select(attrs={'id': 'question_class'}),
            'topic': forms.Select(attrs={'id': 'topic'}),
        }

class StudentCurriculumForm(forms.ModelForm):
    new_activity = forms.CharField(
        max_length=100,
        required=False,
        label='New Activity Name',
        widget=forms.TextInput(attrs={'class': 'new-activity-field'}))

    class Meta:
        model = StudentCurriculumModel
        fields = ['activity','description','certificate']

class StandardizeTestForm(forms.ModelForm):
    add_test_name = forms.CharField(
        max_length=100,
        required=False,
        label='Add Test Name',
        widget=forms.TextInput(attrs={'class': 'new-test-field'}))

    class Meta:
        model =  StandardizeTestAchievementModel
        fields = ['test_name','score','certificate']
