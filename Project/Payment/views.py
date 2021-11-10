from django.shortcuts import render
from . import forms
from .forms import AddPaymentForm
from .models import Payment
# noinspection PyUnresolvedReferences
from UserAuthentication.models import User


def add_payment(request):
    """This is the view for the add payment admin page."""
    user: User = User.objects.get(pk=request.user.id)

    if user.is_admin():
        form: AddPaymentForm = forms.AddPaymentForm(request.POST or None)

        if form.is_valid():
            payment: Payment = Payment(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
            )
            payment.save()

        context = {
            'form': form
        }
        return render(request, 'adminCrudForm.html', context)

    else:
        return render(request, 'UserAuthentication/index.html')
