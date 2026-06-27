from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['loan', 'amount', 'date', 'notes']
        widgets = {
            'loan':   forms.Select(attrs={'class': 'form-input'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '1500',
                'step': '0.01',
            }),
            'date':   forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
            'notes':  forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. June payment',
            }),
        }
        labels = {
            'loan':   'Loan',
            'amount': 'Amount (TJS)',
            'date':   'Payment Date',
            'notes':  'Notes (optional)',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['loan'].queryset = user.loans.all()