from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from projects.models import Project, Tag
from django.contrib import messages
from .utils import searchProject, custom_paginator


def projects(request):
    projects, search_query = searchProject(request)

    custom_range, projects = custom_paginator(request, projects, 6)

    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, "projects/projects.html", context)


def project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tags = project.tags.all()
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = project
            review.owner = request.user.profile
            review.save()
            messages.success(request, 'Your Review Was submitted')
            project.get_vote_count
            return redirect('projects:project', pk=project.id)


    context = {'project': project, 'tags': tags, 'form': form}
    return render(request, "projects/single_project.html", context)


@login_required(login_url='users:login')
def createProject(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            created = form.save(commit=False)
            created.owner = request.user.profile
            created.save()
            return redirect("projects:project", created.id)

    context = {'form': form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url='users:login')
def updateProject(request, pk):
    profile = request.user.profile

    # Only Get projects that belong to a specific user,
    # starts by getting all projects and then get an id of a given project
    data = profile.project_set.get(id=pk)
    form = ProjectForm(instance=data)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            created = form.save()
            return redirect("projects:project", created.id)

    context = {'form': form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url='users:login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Hey %s, Your Project was Deleted Successfully" % request.user.profile.first_name)
        return redirect("users:account")
    context = {'object': project}
    return render(request, "projects/delete_template.html", context)
