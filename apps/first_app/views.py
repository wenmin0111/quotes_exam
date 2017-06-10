from django.shortcuts import render, redirect
from .models import User, Quote
from django.contrib import messages

def index(request):
    # User.objects.all().delete()

    return render(request, 'first_app/index.html')

def regist(request):
    if request.method == "POST":
        name = request.POST['name']
        alios = request.POST['alios']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']
        date_birth = request.POST['date_birth']

    postData = {
        'name': name,
        'alios': alios,
        'email': email,
        'password': password,
        'confirm': confirm,
        'date_birth': date_birth,
    }

    model_resp = User.objects.reg_fn_validation(postData)
    if model_resp[0] == True:
        # print "User successfully created, should add flash message!"
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['name'] = postData['name']
        # print "SESSION: "+ request.session['name']
        return redirect('/quotes')
    else:
        for i in range(0, len(model_resp)):
            messages.warning(request, model_resp[i])
        return redirect('/')

def login(request):
    postData = {
        'email': request.POST['email'],
        'password': request.POST['password']
    }
    model_resp = User.objects.login_check(postData)
    if User.objects.login_check(postData) == True:
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['name'] = User.objects.filter(email=postData['email'])[0].name
        return redirect('/quotes')
    else:
        for i in range(0, len(model_resp)):
            messages.warning(request, model_resp[i])
        return redirect('/')
def quotes(request):
    if request.method == "POST":
        Quote.objects.create(user=User.objects.get(id = request.session['id']), text = request.POST['messages'])

    print Quote.objects.all()
    postData = {
        'user': User.objects.get(id=request.session['id']),
        'quotes': Quote.objects.exclude(user_who_quoted = User.objects.get(id=request.session['id'])),
        'favorites' : Quote.objects.filter(user_who_quoted = User.objects.get(id=request.session['id']))
    }
    return render(request, 'first_app/quotes.html', postData)


def create_page(request):
    return render(request, 'first_app/create.html')

def add_list(request, quote_id):
    # below is log in user
    quote = Quote.objects.get(id = quote_id )
    User.objects.get( id = request.session['id'] ).favorites.add(quote)

    return redirect('/quotes')

def remove(request, quote_id):
    quote = Quote.objects.get(id = quote_id )
    User.objects.get( id = request.session['id'] ).favorites.remove(quote)

    return redirect('/quotes')

def show(request, user_id):
    context = {
        'name' : User.objects.get(id = request.session['id']).alios,
        'count' : User.objects.get(id = request.session['id']).favorites.all().count(),
        'favs' : User.objects.get(id = request.session['id']).favorites.all()
    }

    return render(request, 'first_app/users.html', context)
def logout(request):
    request.session.clear()
    return render(request, 'first_app/index.html')

def dashboard(request):
    return redirect('/quotes')
