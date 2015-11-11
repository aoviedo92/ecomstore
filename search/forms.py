from models import SearchTerm
from django import forms


class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchTerm

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        default_placeholder_text = 'Search'
        self.fields['q'].widget.attrs['placeholder'] = default_placeholder_text

    include = ('q',)
