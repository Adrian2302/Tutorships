from django.shortcuts import render, redirect
from Payment import models
from Payment.forms import AddPaymentForm
from django.views import generic
# noinspection PyUnresolvedReferences
from UserAuthentication.models import User


def create_context(form):
    return {'form': form}

class AddPayment(generic.View):
    """This is the view for the add payment admin page."""
    def get(self, request):

        user: User = User.objects.get(pk=request.user.id)

        if user.is_admin():
            form = AddPaymentForm
            context = create_context(form)

            return render(request, 'adminCrudForm.html', context)

        else:
            return redirect('index')

    def post(self, request):

        user: User = User.objects.get(pk=request.user.id)

        if user.is_admin():
            form: AddPaymentForm = AddPaymentForm(request.POST or None)

            if form.is_valid():
                payment: models.Payment = models.Payment(
                    name=form.cleaned_data['name'],
                    description=form.cleaned_data['description'],
                )
                payment.save()
            
            context = create_context(form)

            return render(request, 'adminCrudForm.html', context)

        else:
            return render(request, 'UserAuthentication/index.html')