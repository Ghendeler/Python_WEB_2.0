from collections import Counter, defaultdict

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from .forms import AddAuthorForm, AddQuoteForm, TagForm
from .models import Author, Quote, Tag


def main(request, page=1):
    latest_quotes_list = Quote.objects.all()
    paginator = Paginator(latest_quotes_list, 5)
    cur_page = paginator.page(page)
    template = loader.get_template("quotes/quotes.html")
    context = {
        "latest_quotes_list": cur_page.object_list,
        "top10tags": top10tags(),
        "page": {
            "previous": cur_page.previous_page_number() if page > 1 else False,
            "next": cur_page.next_page_number() if cur_page.has_next() else False,
        },
    }
    return HttpResponse(template.render(context, request))


def author(request, question_id):
    template = loader.get_template("quotes/author.html")
    context = {}
    return HttpResponse(template.render(request=request))


def find_by_tag(request, tag_name, page=1):
    tag = Tag.objects.get(name=tag_name)
    quotes_by_tag = Quote.objects.filter(tags__id=tag.id)
    paginator = Paginator(quotes_by_tag, 5)
    cur_page = paginator.page(page)

    template = loader.get_template("quotes/quotes_by_tag.html")
    context = {
        "tag": tag,
        "latest_quotes_list": quotes_by_tag,
        "top10tags": top10tags(),
        "page": {
            "previous": cur_page.previous_page_number() if page > 1 else False,
            "next": cur_page.next_page_number() if cur_page.has_next() else False,
        },
    }
    return HttpResponse(template.render(context, request))


@login_required
def tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:main")
        else:
            return render(request, "quotes/tag.html", {"form": form})

    return render(request, "quotes/tag.html", {"form": TagForm()})


@login_required
def add_author(request):
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save()
            new_author.slug = get_slug(new_author.fullname)
            new_author.save()
            return redirect(to="quotes:main")
        else:
            return render(request, "quotes/add_author.html", {"form": form})

    return render(request, "quotes/add_author.html", {"form": AddAuthorForm()})


def get_slug(data):
    return data.strip().replace(" ", "-")


@login_required
def add_quote(request):
    authors = Author.objects.order_by("fullname").all()
    tags = Tag.objects.order_by("name").all()
    if request.method == "POST":
        form = AddQuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to="quotes:main")
        else:
            return render(
                request,
                "quotes/add_quote.html",
                {"authors": authors, "tags": tags, "form": form},
            )

    return render(
        request,
        "quotes/add_quote.html",
        {"authors": authors, "tags": tags, "form": AddQuoteForm()},
    )


def top10tags():
    font_siza = [28, 26, 24, 22, 20, 18, 16, 14, 12, 10]
    quotes = Quote.objects.all()
    tag_frequency = defaultdict(int)
    for quote in quotes:
        for tag in quote.tags.all():
            tag_frequency[tag.name] += 1

    top10tupl = Counter(tag_frequency).most_common()[:10]
    top10tags = [t[0] for t in top10tupl]
    zip(top10tags, font_siza)
    return [{"tag": t[0], "size": t[1]} for t in zip(top10tags, font_siza)]
