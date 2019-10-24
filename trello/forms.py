from django.forms import ModelForm,CharField
from django import forms
from .models import Board,BoardList, ListCard,BoardInvite,CardAttatchments,CardCheckList,CommentSection
from .models import TrelloUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from celery import shared_task

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['title']


class ListForm(ModelForm):
    class Meta:
        model = BoardList
        fields = ['title']


class CardForm(ModelForm):
    description = CharField(required=False)
    class Meta:
        model = ListCard
        fields = ['title','description']

class CardMemberForm(ModelForm):
    description = CharField(required=False)
    class Meta:
        model = ListCard
        fields = ['card_member']

class BoardInviteForm(ModelForm):
    class Meta:
        model = BoardInvite
        fields = ['email']
    

class CardAttatchmentForm(ModelForm):
    class Meta:
        model = CardAttatchments
        fields = ['file']


class CardCheckListForm(ModelForm):    
    class Meta:
        model = CardCheckList
        fields = ['checklist']


class CommentSectionForm(ModelForm):    
    class Meta:
        model = CommentSection
        fields = ['text']


class UserCreationForm(ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = TrelloUser
        fields = ('email', 'name', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
       
        
        if commit:
            user.save()
            
        return user

class UserChangeForm(ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = TrelloUser
        fields = ('name','email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

