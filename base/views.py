from django.shortcuts import render, redirect
from .models import User, Event, Submission
from .forms import SubmissionForm

# Create your views here.


def home_page(request):
    users = User.objects.filter(hackthon_participant=True)
    events = Event.objects.all()
    context = {"users": users, "events": events}
    return render(request, "home.html", context)


def user_page(request, pk):
    user = User.objects.get(id=pk)
    return render(request, "profile.html", {"user": user})


def account_page(request):
    return render(request, "account.html", {"user": request.user})


def event_page(request, pk):
    event = Event.objects.get(id=pk)
    
    registered = False
    submitted = False
    
    if request.user.is_authenticated:
        registered = request.user.event_set.filter(id=event.id).exists()
        submitted = Submission.objects.filter(participant=request.user, event=event).exists()

    return render(request, "event.html", {"event": event, 'registered':registered, 'submitted':submitted})


def registration_confirmation(request, pk):
    event = Event.objects.get(id=pk)
    try:
        event.participants.add(request.user)
        return redirect("event", pk=event.id)
    except:
        return render(request, "event_confirmation.html", {"event": event})


def project_submission(request, pk):
    event = Event.objects.get(id=pk)
    form = SubmissionForm()
    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.participant = request.user
            submission.event = event
            submission.save()
            return redirect("account")
    return render(request, "submit_form.html", {"event": event, "form": form})
