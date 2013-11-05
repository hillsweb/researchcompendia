from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Hidden, Layout, Submit
from crispy_forms.bootstrap import PrependedText

from .models import Article


class DoiForm(forms.Form):

    doi = forms.CharField(required=False, label='')

    def __init__(self, *args, **kwargs):
        super(DoiForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'doiref'
        self.helper.layout = Layout(
            PrependedText('doi', 'doi:'),
        )


class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'id-creation'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.attrs = {'enctype': 'multipart/form-data'}
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.layout = Layout(
            Hidden('doi', ''),
            Hidden('site_owner', '{{ user }}'),
            'title',
            'code_data_abstract',
            'code_archive_file',
            'data_archive_file',
            'notes_for_staff',
            'primary_research_field',
            'secondary_research_field',
            'tags',
            Field('authorship', type='hidden'),
            Field('related_urls', type='hidden'),
            Field('paper_abstract', type='hidden'),
        )

    class Meta:
        model = Article
        # TODO I wonder if exclude is redundant since I don't list these in the layout?
        exclude = ['legacy_id', 'status_changed', ]
        widgets = {
            # TODO this is not DRY but I'm not sure how to include placeholder attr in the crispy layout
            'title': forms.TextInput(attrs={'placeholder': 'Title your compendium.'}),
            'code_data_abstract': forms.Textarea(attrs={'placeholder': 'does not need to match paper abstract'}),
        }
