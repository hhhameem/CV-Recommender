from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
import datetime
from .forms import JobPostForm, EditJobForm
from .models import Job
from custom_decorators.custom_decorator import allowed_users
from custom_scripts.dictionary_sort import sort_dict_and_return


# Create your views here.

def home(request):
    category_dict = {}
    job_number = 0
    latest_jobs = Job.published.all().order_by('-publish')[:8]

    for job in Job.objects.all():
        category_dict[job.job_category] = category_dict\
            .get(job.job_category, 0)+1
        job_number += 1

    sorted_sliced_category, top_3 = sort_dict_and_return(category_dict)

    context = {'job_number': job_number, 'latest_jobs': latest_jobs,
               'sorted_sliced_category': sorted_sliced_category, 'top_3': top_3}

    return render(request, 'index.html', context)


def jobCategory(request, job_cat):
    return HttpResponse('Thank you ' + job_cat)


@login_required(login_url='login')
@allowed_users(allowed_group=['recruiter'])
def postJob(request):
    if request.method == 'POST':
        job_form = JobPostForm(data=request.POST, files=request.FILES)
        if job_form.is_valid():
            job_form_obj = job_form.save(commit=False)
            job_form_obj.recruiter = request.user.recruiter
            job_form_obj.save()
            messages.success(request, 'Job Has Successfully Posted.')
            return redirect('recruiterdashboard')
        else:
            return render(request, 'add_job.html', {'job_form': job_form})
    else:
        job_form = JobPostForm()

    return render(request, 'add_job.html')


@login_required(login_url='login')
@allowed_users(allowed_group=['recruiter'])
def editjob(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        jobEditForm = EditJobForm(instance=job, data=request.POST)
        if jobEditForm.is_valid():
            jobEditForm.save()
            messages.success(request, 'You Job has been \
                            successfully edited and saved')
            return redirect('recruiterdashboard')
    else:
        jobEditForm = EditJobForm(instance=job)

    return render(request, 'edit_job.html', {'jobEditForm': jobEditForm, 'job': job})


@login_required(login_url='login')
@allowed_users(allowed_group=['recruiter'])
def currentOpeningJobs(request):
    opening_jobs = Job.published.filter(recruiter=request.user.recruiter)\
        .order_by('-publish')

    paginator = Paginator(opening_jobs, 3)
    page = request.GET.get('page')
    opening_jobs = paginator.get_page(page)
    return render(request, 'view_current_job.html', {'opening_jobs': opening_jobs})


@login_required(login_url='login')
@allowed_users(allowed_group=['recruiter'])
def allJobs(request):
    all_jobs = Job.objects.filter(recruiter=request.user.recruiter)\
        .order_by('-publish')
    today = datetime.datetime.now()

    paginator = Paginator(all_jobs, 10)
    page = request.GET.get('page')
    all_jobs = paginator.get_page(page)

    return render(request, 'view_all_job.html', {'all_jobs': all_jobs, 'today': today})


def jobDetail(request, job_slug):
    return HttpResponse('Okay')
