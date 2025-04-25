from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Activity
from .forms import ActivityForm
from collections import defaultdict
from django.http import JsonResponse
from .models import Activity

def test_db(request):
    try:
        count = Activity.objects.count()
        return JsonResponse({'status': 'success', 'activity_count': count})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})



@login_required
def home(request):
    activities = Activity.objects.filter(user=request.user).order_by('-date')
    total_carbon = sum(a.carbon_kg for a in activities)

    category_data = defaultdict(float)
    for act in activities:
        category_data[act.category] += act.carbon_kg
    labels = list(category_data.keys())
    values = list(category_data.values())

    # Chart 2: Emissions by date
    date_data = defaultdict(float)
    for act in activities:
        date_str = act.date.strftime('%Y-%m-%d')
        date_data[date_str] += act.carbon_kg
    date_labels = list(date_data.keys())
    date_values = list(date_data.values())

    # Prepare category data for the chart
    category_data = defaultdict(float)
    for act in activities:
        category_data[act.category] += act.carbon_kg

    labels = list(category_data.keys())
    values = list(category_data.values())

    return render(request, 'tracker/home.html', {
        'activities': activities,
        'total_carbon': total_carbon,
        'labels': labels,
        'values': values,
        'date_labels': date_labels,
        'date_values': date_values,
    })
from django.shortcuts import get_object_or_404

@login_required
def delete_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    activity.delete()
    return redirect('home')

@login_required
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            return redirect('home')
    else:
        form = ActivityForm()
    return render(request, 'tracker/add.html', {'form': form})
