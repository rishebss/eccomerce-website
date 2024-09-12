
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render,redirect
from pathlib import Path
from .forms import DesignForm
from .models import Design

@login_required
def uploaddesign(request):
    if request.method == "POST":
        form = DesignForm(request.POST, request.FILES)
        if form.is_valid():
            design = form.save(commit=False)
            design.user = request.user
            design.save()
            return redirect('credentials:home')

    else:
        form = DesignForm()

    return render(request, 'uploaddesign.html', {'form': form})


def view_designs(request):
    designs = Design.objects.all().order_by('-created_at')
    return render(request, 'designrequest.html', {'designs': designs})


