from django import forms
from django.utils.safestring import mark_safe
import unicodedata
from .models import Card


class CsvUploadForm(forms.Form):
    file = forms.FileField(label="CSV-Datei (UTF-8)", help_text="Format: front,back[,category] (ohne Überschrift)")

def _normalize(s:str) -> str:
    s = (s or "").strip().lower()
    s = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn")  # Akzente raus

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Passwort wiederholen")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Die Passwörter stimmen nicht überein.")
        return cleaned_data

    def save(self, commit=True):
        from django.contrib.auth.models import User
        user = User(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"]
        )
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ("question","answer","category")
        labels = {
            "question": "Frage/Front (z.B. Spanisch oder Frage)",
            "answer": "Antwort/Back (z.B. Deutsch oder Lösung)",
            "category": "Kategorie/Thema"
        }

class AnswerForm(forms.Form):
    card_id = forms.IntegerField(widget=forms.HiddenInput)
    direction = forms.ChoiceField(choices=[("question->answer","Frage → Antwort"),("answer->question","Antwort → Frage")], widget=forms.HiddenInput)
    answer = forms.CharField(label="Deine Antwort", widget=forms.TextInput(attrs={"autofocus":"autofocus"}))
