from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import EntryForm, TopicForm
from .models import Entry, Topic


def index(request) -> str:
    """The home page for Learning Log."""
    return render(request, "learning_logs/index.html")


@login_required
def topics(request) -> str:
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)


def check_topic_owner(topic, user):
    if topic.owner != user:
        raise Http404


@login_required
def topic(request, topic_id) -> str:
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user.
    check_topic_owner(topic, request.user)
    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != "POST":
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            n_topic = form.save(commit=False)
            n_topic.owner = request.user
            n_topic.save()
            return redirect("learning_logs:topics")
    # Display a blank or invalid form.
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request.user)

    if request.method != "POST":
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            n_entry = form.save(commit=False)
            n_entry.topic = topic
            n_entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)

    # Display a blank or invalid form.
    context = {"form": form, "topic": topic}
    return render(request, "learning_logs/new_entry.html", context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic, request.user)

    if request.method != "POST":
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=topic.id)

    # Display a blank or invalid form.
    context = {"form": form, "topic": topic, "entry": entry}
    return render(request, "learning_logs/edit_entry.html", context)
