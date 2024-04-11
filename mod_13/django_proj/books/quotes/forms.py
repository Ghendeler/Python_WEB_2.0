from .models import Tag, Quote, Author
from django.forms import (
    ModelForm,
    CharField,
    TextInput,
    MultiValueField,
    Textarea,
    ModelChoiceField,
    Select,
)


class TagForm(ModelForm):

    name = CharField(min_length=3, max_length=45, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ["name"]


class AddAuthorForm(ModelForm):

    fullname = CharField(
        min_length=3, max_length=120, required=True, widget=TextInput()
    )
    born_date = CharField(min_length=3, max_length=50, widget=TextInput())
    born_location = CharField(min_length=3, max_length=150, widget=TextInput())
    description = CharField(min_length=3, required=True, widget=Textarea())

    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class AddQuoteForm(ModelForm):
    quote = CharField(
        min_length=3, required=True, widget=Textarea(attrs={"class": "form-control"})
    )
    author = ModelChoiceField(
        queryset=(Author.objects.order_by("fullname").all()),
        required=True,
        widget=Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Quote
        fields = ["quote", "author"]
        exclude = ["tags"]
