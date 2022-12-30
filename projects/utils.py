from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def custom_paginator(request, query_set, results):
    page = request.GET.get('page')  # start from the first Page
    paginator = Paginator(query_set, results)
    try:
        query_set = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        query_set = paginator.page(page)
    except EmptyPage:
        # Tell us how many pages we have
        page = paginator.num_pages
        # Go to that page
        query_set = paginator.page(page)
    leftIndex = (int(page) - 4)  # represent the left side of the paginator
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)  # represent the right index of the page
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)
    return custom_range, query_set


def searchProject(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query').strip()
    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__first_name__icontains=search_query) |
        Q(owner__last_name__icontains=search_query) |
        Q(tags__in=tags)
    )

    return projects, search_query
