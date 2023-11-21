from django import forms
from myappF23.models import Order


class InterestForm(forms.Form):
    CHOICES = [(1, 'Yes'), (0, 'No')]
    interested = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-input'}),choices=CHOICES, required=True)
    level=forms.IntegerField(min_value=1,max_value=5,initial=1)
    additional_comments=forms.CharField(label='Additional Comments',widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),required=False)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["student", "course", "levels", "order_date"]

        widget={
            'student': forms.RadioSelect(),
            'order_date': forms.SelectDateWidget(),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)