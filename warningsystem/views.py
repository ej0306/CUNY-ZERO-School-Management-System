from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from .models import Warnings
from .forms import IssueWarningForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from users.models import Registrar
from datetime import datetime


# Create your views here.
@login_required
def issue_warning(request):
    if not request.user.is_registrar:
        raise PermissionDenied()

    if request.method == 'POST':
        form = IssueWarningForm(request.POST)

        # do something if form is completed successfully
        if form.is_valid():
            w = form.save(commit=False)
            w.registrar = Registrar.objects.filter(user=request.user).first()
            w.issue_date = datetime.now()
            w.save()

            return redirect(reverse('warnings_list'))
    else:
        form = IssueWarningForm()

    return render(request, 'warningsystem/issue_warning_form.html', {'form': form})


@login_required
def issued_warnings_list(request):
    if not request.user.is_registrar:
        raise PermissionDenied()

    context = {
        'warnings': Warnings.objects.all().order_by('-issue_date')
    }

    return render(request, 'warningsystem/issued_warnings_list.html', context)


@login_required
def issued_warning_details(request, pk):
    if not request.user.is_registrar:
        raise PermissionDenied()

    context = {
        'warning': Warnings.objects.filter(id=pk).first()
    }

    return render(request, 'warningsystem/issued_warning_details.html', context)


class RemoveWarning(View, AccessMixin):
    def get(self, request, pk):
        if not request.user.is_registrar:
            raise PermissionDenied()
        w = get_object_or_404(Warnings, id__iexact=pk)
        return render(request, 'warningsystem/remove_warning.html', context={'warning': w})

    def post(self, request, pk):
        if  not request.user.is_registrar:
            raise PermissionDenied()
        w = get_object_or_404(Warnings, id__iexact=pk)
        w_id = w.id
        w.delete()
        msg = "Warning has been removed. #" + str(w_id)
        messages.success(request, msg)
        return redirect(reverse('warnings_list'))
