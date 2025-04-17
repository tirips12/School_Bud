from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Question, Course, ProjectDiscussion

class ProjectDiscussionForm(forms.ModelForm):
    projects = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        help_text="Enter one project name or link per line."
    )

    class Meta:
        model = ProjectDiscussion
        fields = ['group_name', 'course', 'projects']
        widgets = {
            'group_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', None)
        super().__init__(*args, **kwargs)
        if course:
            self.fields['course'].initial = course
            self.fields['course'].widget = forms.HiddenInput()
        # If editing, show projects as lines
        if self.instance and self.instance.pk:
            if isinstance(self.instance.projects, list):
                self.fields['projects'].initial = '\n'.join(self.instance.projects)

    def clean_projects(self):
        data = self.cleaned_data['projects']
        # Split by lines, ignore empty lines
        projects_list = [line.strip() for line in data.splitlines() if line.strip()]
        return projects_list


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'course']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        } 


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'