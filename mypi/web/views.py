from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .forms import SignUpForm , kerjaForm, UserForm, ProfileForm
from django.utils import timezone
from django.contrib.auth import logout
from web.models import kerja, Profile
from django.db.models import Q
from django.contrib import messages

def index(request):
    if request.user.is_authenticated():
        work = kerja.objects.filter(user=request.user)
        return render(request,'web/index.html',{'kerja': work})
    return render(request, 'web/index.html',)

def delete_kerja(request, kerja_id):
    work = kerja.objects.get(pk=kerja_id)
    work.delete()
    kerjas = kerja.objects.filter(user=request.user)
    return render(request, 'web/index.html', {'kerja': kerjas})

def detail(request, kerja_id):
    user = request.user
    work = get_object_or_404(kerja, pk=kerja_id)
    return render(request, 'web/detail.html', {'kerja': work, 'user': user})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return render(request, 'web/index.html')
    else:
        form = SignUpForm()
    return render(request, 'web/signup.html', {'form': form})

def create_job(request):
    if not request.user.is_authenticated():
        return render(request, 'web/login.html')
    else:
        form = kerjaForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                kerja = form.save(commit=False)
                kerja.user = request.user
                kerja.pub_date = timezone.now()
                kerja.save()
                return HttpResponseRedirect('/web/')
        else :
            form : kerjaForm()
        return render(request, 'web/create_kerja.html', {'form' : form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                kerjas = kerja.objects.filter(user=request.user)
                return render(request, 'web/index.html', {'kerja': kerjas})
            else:
                return render(request, 'web/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'web/login.html', {'error_message': 'Invalid login'})
    return render(request, 'web/login.html')

def logout_user(request):
    logout(request)
    form = SignUpForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'web/index.html', context)

def search(request) :
    data = kerja.objects.all()
    query = request.GET.get("q")
    if query:
        results = data.filter(
            Q(nama_kerja__startswith=query)|
            Q(kota__icontains=query))
        return render(request,'web/search.html', {'query': query,'results': results, })
    return render(request, 'web/search.html')

def update_profile(request):
    if not request.user.is_authenticated():
        return render(request, 'web/login.html')
    else:
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Profile details has been successfully updated.')
            else:
                return render(request, 'web/update.html', {'error_message': 'Please correct the errors below!'})
        else:
            user_form = UserForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'web/update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

