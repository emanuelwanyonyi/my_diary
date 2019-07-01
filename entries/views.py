# Views file

from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from entries.models import Entry
from entries.forms import EntryForm


def home_page(request):
    """
    A functon to render the home page
    """
    home_page_title = "My Diary: Our Happy moments"
    return render(request, "index.html", {"home_page_title": home_page_title})


@login_required
def create_entry(request):
    """
    Create a new entry in the database
    """
    if request.method == 'POST':
        form = EntryForm(request.POST or None)
        if form.is_valid():
            # Validate form inputs
            title = form.cleaned_data['title']
            event = form.cleaned_data['event']

            """
            prevent autosaving of data before appending the authour and date posted info.
            """
            post = form.save(commit=False)
            post.authour = request.user
            post.published_date = timezone.now()
            post.save()

        return redirect("/entries/")
    else:
        form = EntryForm()
        return render(request, "create_entry.html", {"form": form})


@login_required
def get_entries(request):
    """
    Return all entries.
    """
    if request.user.is_authenticated:
        entries = Entry.objects.order_by('-date_posted')  # Get all entries
        return render(request, 'entries.html', {'entries': entries})
    else:
        return "Kindly login to access these contents"


@login_required
def entry_details(request, id):
    """
    Display more details about an entry
    """
    try:
        entry = Entry.objects.get(id=id)
        return render(request, 'entry_details.html', {'entry': entry})
    except ValueError:
        raise Http404
    except:
        raise Http404


@login_required
def update_entry(request, id):
    """
    Updates an entry in the database
    """
    entry = get_object_or_404(Entry, id=id)
    form = EntryForm(request.POST or None, instance=entry)
    if form.is_valid():
        form.save()
        return redirect('entries')
    return render(request, 'create_entry.html', {'form': form})


@login_required
def delete_entry(request, id):
    """
    Deletes an entry in the database
    """
    entry = get_object_or_404(Entry, id=id)
    form = EntryForm(request.POST or None, instance=entry)
    if request.method == 'POST':
        entry.delete()
        return redirect('entries')
    return render(request, 'confirm_delete.html', {'entry': entry})
