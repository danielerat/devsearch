from django.forms import ModelForm
from django import forms
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'featured_image', 'demo_link', 'source_link', 'tags']
        # Frist Way we can override a form
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

        # Overiding from using init

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        # The Slow Way of adding attributes , simply repreat this whole thing for
        # all your text field or
        # self.fields['title'].widget.attrs.update({'class': 'input'})

        # The fast way
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Place Your Vote',
            'body': 'Add A commnet with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        # The fast way
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
