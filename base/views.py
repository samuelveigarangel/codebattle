from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


from .models import User, Event, Submission
from .forms import SubmissionForm, CustomUserCreateForm

# Create your views here.


def login_page(request):
    page = "login"
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "login_register.html", {"page": page})


def register_page(request):
    page = "register"
    form = CustomUserCreateForm()

    if request.method == "POST":
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect("home")
    return render(request, "login_register.html", {"page": page, "form": form})


def logout_page(request):
    logout(request)
    return redirect("login")


def home_page(request):
    users = User.objects.filter(hackthon_participant=True)
    events = Event.objects.all()
    context = {"users": users, "events": events}
    return render(request, "home.html", context)


def user_page(request, pk):
    user = User.objects.get(id=pk)
    return render(request, "profile.html", {"user": user})


@login_required(login_url="/login")
def account_page(request):
    return render(request, "account.html", {"user": request.user})


def event_page(request, pk):
    event = Event.objects.get(id=pk)

    registered = False
    submitted = False

    if request.user.is_authenticated:
        registered = request.user.event_set.filter(id=event.id).exists()
        submitted = Submission.objects.filter(
            participant=request.user, event=event
        ).exists()

    return render(
        request,
        "event.html",
        {"event": event, "registered": registered, "submitted": submitted},
    )


@login_required(login_url="/login")
def registration_confirmation(request, pk):
    event = Event.objects.get(id=pk)
    try:
        event.participants.add(request.user)
        return redirect("event", pk=event.id)
    except:
        return render(request, "event_confirmation.html", {"event": event})


@login_required(login_url="/login")
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


@login_required(login_url="/login")
def update_submission(request, pk):
    submission = Submission.objects.get(id=pk)
    event = submission.event
    form = SubmissionForm(instance=submission)
    if request.method == "POST":
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect("account")
    return render(request, "submit_form.html", {"form": form, "event": event})
