from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile, Product, Question, Rating, ProgrammingQuestion, productResults, programmingResults, User
from django.shortcuts import get_object_or_404, render
from .forms import SignUpForm, ProfileForm
from django.db import transaction
from django.contrib import messages
from datetime import datetime
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
import csv
from django.http import HttpResponse
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import ColumnChart
from graphos.sources.model import ModelDataSource


def signup(request):
    
    if request.method == 'POST':
        
        form = SignUpForm(request.POST)
        
        if form.is_valid():
    
            form_email = form.cleaned_data.get('email')
        
            results = User.objects.filter(email = form_email)

            if results.count() == 0:


                form.save()
                
                username = form.cleaned_data.get('username')
                
                raw_password = form.cleaned_data.get('password1')

                user = authenticate(username=username, password=raw_password)
                

                login(request, user)
                
                profile = Profile.objects.get(user_id = user.id)
                
                profile.first_name = form.cleaned_data.get('first_name')
                
                profile.last_name = form.cleaned_data.get('last_name')
                
                profile.email =  form.cleaned_data.get('email')
                
                profile.password = raw_password
                    
                profile.save()

                return redirect('home')

            else:
                
                messages.error(request, 'Failed, your email has already been registed')

    else:
        
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})

@login_required
@transaction.atomic
def update_profile(request):
    
    if request.method == 'POST':
        
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        
        if profile_form.is_valid():
            
            profile_form.save()
            
            messages.success(request, 'Your profile was successfully updated!')

            return redirect('home')

        else:
            
            messages.error(request, 'Please correct the error below.')
    else:
        
        profile_form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'profiles/profile.html', {'profile_form': profile_form})


@login_required
def home(request):
    
    if request.user.is_superuser:
    
        return redirect('manage')
    
    else:

        product_list = Product.objects.order_by('-created_date')[:5]
        
        context = {'product_list': product_list}
        
        return render(request, 'home/startQuestion.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage(request):
    if request.method == 'POST':
        
        profiles = Profile.objects.all()
        
        product_list = Product.objects.order_by('-created_date')[:5]
                
        productquestions= Question.objects.all()
                    
        programmingquestions= ProgrammingQuestion.objects.all()
        
        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = 'attachment; filename="report.csv"; '
        
        writer = csv.DictWriter(response, fieldnames=engineerList())
            
        writer.writeheader()
        
        output = engineerList(1)
        
        if request.POST.get('select') == '1':

            productresults = productResults.objects.filter(update_date__gte=datetime.date(2017, 5, 1), update_date__lte=datetime.date(2017, 8, 31))
    
            programmingresults = programmingResults.objects.filter(update_date__gte=datetime.date(2017, 5, 1), update_date__lte=datetime.date(2017, 8, 31))
            
            for product in product_list:
            
                for question in product.question_set.all():
            
                    output['Product'] = product.product_name
        
                    output['Question'] = question.question_text

                    for profile in profiles:
                        
                        m = outputs()
                        
                        if not profile.user.is_superuser:

                            value = m.product(profile.user.id, question.id, productresults)
            
                            name = profile.user.first_name + '_' +profile.user.last_name+'_'+profile.user.email

                            output[name] = value
    
                    writer.writerow(output)
        
            for pq in programmingquestions:
            
                output['Product'] = "Programming"
                
                output['Question'] = pq.programming_question_text
                    
                for profile in profiles:
                        
                    m = outputs()
                    
                    if not profile.user.is_superuser:
                    
                        value = m.programming(profile.user.id, pq.id, programmingresults)
                        
                        name = profile.user.first_name + '_' +profile.user.last_name+'_'+profile.user.email
                        
                        output[name] = value
                
                writer.writerow(output)
        
            return response


    return render(request, 'manage/manage.html')


@login_required
def detail(request, product_id):
    
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
    
        if 'continue' in request.POST:
            
            #validation
            for question in product.question_set.all():

                if request.POST.get(str(question.id)) is None:
                    
                    return render(request, 'home/detail.html', {
                                  'product': product,
                                  'error_message': "Please make sure you selected all choices",
                                  })

            for question in product.question_set.all():
                
                record =  productResults.objects.filter(user_id_number=request.POST.get("user"), question_number=question.id, update_date__gte=datetime.date(2017, 5, 1), update_date__lte=datetime.date(2017, 8, 31))
                
                if record.exists():
                    
                    record.update(rating_number = request.POST.get(str(question.id)), update_date = timezone.now())
                
                else:
                    
                    newRecord = productResults(user_id_number=request.POST.get("user"), question_number=question.id, rating_number =request.POST.get(str(question.id)))
            
                    newRecord.save()

            return redirect('path')

        elif 'back' in request.POST:
    
            return redirect('home')
                
    return render(request, 'home/detail.html', {'product': product})

@login_required
def programming(request):
    
    programmingQuestion = ProgrammingQuestion.objects.all()
    
    for test in programmingQuestion:
    
        print test.programming_question_text
    
    if request.method == 'POST':

        for pgquestion in programmingQuestion:

            if request.POST.get(str(pgquestion.id)) is None:
    
                return render(request, 'home/programming.html', {
                              'programmingQuestion': programmingQuestion,
                              'error_message': "Please make sure you selected all choices",
                              })

        for pgquestion in programmingQuestion:
                        
            record =  programmingResults.objects.filter(user_id_number=request.POST.get("user"), question_number=pgquestion.id, update_date__gte=datetime.date(2017, 5, 1), update_date__lte=datetime.date(2017, 8, 31))
                            
            if record.exists():
                
                record.update(rating_number = request.POST.get(str(pgquestion.id)), update_date = timezone.now())
                                            
            else:
                                                
                newRecord = programmingResults(user_id_number=request.POST.get("user"), question_number=pgquestion.id, rating_number =request.POST.get(str(pgquestion.id)))
                                                    
                newRecord.save()

        return redirect('logoutandthankyou')

    return render(request, 'home/programming.html', {'programmingQuestion': programmingQuestion})


@login_required
def path(request):
    
    if request.method == 'POST':
        
        if request.POST.get('select') == '1':
            
            return redirect('home')

        else:
            
            return redirect('programming')

    return render(request, 'home/pathQuestion.html')


def thankyou(request):

    return render(request, 'home/thankyou.html')



@login_required
@user_passes_test(lambda u: u.is_superuser)
def report(request, report_id):
    if report_id == '1':
        
        productresults = productResults.objects.filter(update_date__gte=datetime.date(2017, 5, 1), update_date__lte=datetime.date(2017, 8, 31))
        
        programmingresults = programmingResults.objects.filter(update_date__gte=datetime.date(2017, 5, 1), update_date__lte=datetime.date(2017, 8, 31))
        
        report_title = "Welcome to the Summary Report (from 5-1 to 8-31)"

    
    if report_id == '2':

        productresults = productResults.objects.filter(update_date__gte=datetime.date(2017, 9, 1), update_date__lte=datetime.date(2017, 12, 31))
    
        programmingresults = programmingResults.objects.filter(update_date__gte=datetime.date(2017, 9, 1), update_date__lte=datetime.date(2017, 12, 31))
    
        report_title = "Welcome to the Summary Report (from 9-1 to 12-31)"

    else:

        productresults = productResults.objects.all()
    
        programmingresults = programmingResults.objects.all()
    
    profiles = Profile.objects.all()

    product_list = Product.objects.order_by('-created_date')[:5]

    productquestions= Question.objects.all()
    
    programmingquestions= ProgrammingQuestion.objects.all()
    
    if not productresults:
        
        chart = "No graph avaliable at this time because of data unavaliable"
    
    else:
    
        data = [['Product Questions', 'Rating']]
        
        for productquestion in productquestions:
            
            outputs =  productresults.filter(question_number=productquestion.id)
            
            total = 0.00
            
            count = 0.00
        
            if outputs:
            
                for output in outputs:
                
                    total += output.rating_number
                
                    count += 1
                
                info = [productquestion.question_text, round(total/count,2)]

                data.append(info)

        # DataSource object
        data_source = SimpleDataSource(data=data)

        # Chart object
        chart = ColumnChart(data_source,width =500, options={'title': 'Average rating of each Prodcut_Q', 'legend': {'position':'right'}, 'bar': {'groupWidth': '55%'}, 'vAxis': {'viewWindow':{'max':'10','min':'0'}}})

    #get rating for each programming question

    if not programmingresults:

        chart2 = "No graph avaliable at this time because of data unavaliable"

    else:

        data2 = [['Programming Questions', 'Rating']]
        
        for programmingquestion in programmingquestions:
            
            outputs =  programmingresults.filter(question_number=programmingquestion.id)
            
            total = 0.00
            
            count = 0.00
            
            if outputs:
            
                for output in outputs:
                    
                    total += output.rating_number
                    
                    count += 1

                info2 = [programmingquestion.programming_question_text, round(total/count,2)]
            
            data2.append(info2)

        # DataSource object
        data_source2 = SimpleDataSource(data=data2)
        
        # Chart object
        chart2 = ColumnChart(data_source2,width =500, options={'title': 'Average rating of each Programming_Q', 'colors': ['green'], 'legend': {'position':'right'}, 'bar': {'groupWidth': '40%'}, 'vAxis': {'viewWindow':{'max':'10','min':'0'}}})


    context = {'profiles' : profiles,
        
        'productquestions': productquestions,
            
        'programmingquestions':programmingquestions,
                
        'productresults' : productresults,
                
        'programmingresults' : programmingresults,

        'report_title' : report_title,

        'product_list': product_list,

        'chart': chart,

        'chart2': chart2,

        'report_id' : report_id}
    
    return render(request, 'manage/report.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def personalReport(request, report_id, user_id):
    
    focusedUser = Profile.objects.get(user_id = user_id)
    
    focusedUserName= focusedUser.user.first_name + ' '+ focusedUser.user.last_name
    
    if report_id == '1':
        
        productresults = productResults.objects.filter(user_id_number=user_id, update_date__gte=datetime.date(2017, 5, 1), update_date__lte=datetime.date(2017, 8, 31)).order_by('question_number')
        
        programmingresults = programmingResults.objects.filter(user_id_number=user_id, update_date__gte=datetime.date(2017, 5, 1), update_date__lte=datetime.date(2017, 8, 31)).order_by('question_number')
    
    if productresults:
        
        data = [['Product Questions', 'Rating']]

        for productresult in productresults:
        
            productquestion = Question.objects.get(id = productresult.question_number)
        
            info = [productquestion.question_text, productresult.rating_number]

            data.append(info)

        # DataSource object
        data_source = SimpleDataSource(data=data)
        
        # Chart object
        chart = ColumnChart(data_source,width =400, options={'title': 'Rating of each Prodcut_Q', 'colors': ['#FECF30'],'legend': {'position':'bottom'}, 'bar': {'groupWidth': '55%'}, 'vAxis': {'viewWindow':{'max':'10','min':'0'}}})

    else:
    
        chart = "No graph avaliable at this time because of data unavaliable"

    #Programming part

    if programmingresults:

        data2 = [['Programming Questions', 'Rating']]

        for programmingresult in programmingresults:
            
            programmingquestion = ProgrammingQuestion.objects.get(id = programmingresult.question_number)
            
            info = [programmingquestion.programming_question_text, programmingresult.rating_number]
            
            data2.append(info)

        # DataSource object
        data_source = SimpleDataSource(data=data2)
        
        # Chart object
        chart2 = ColumnChart(data_source,width =400, options={'title': 'Rating of each Programming_Q', 'colors': ['#666868'],'legend': {'position':'bottom'}, 'bar': {'groupWidth': '55%'}, 'vAxis': {'viewWindow':{'max':'10','min':'0'}}})

    else:

        chart2 = "No graph avaliable at this time because of data unavaliable"

    context = {'chart': chart,
               'chart2': chart2,
               'focusedUserName' : focusedUserName}

    return render(request, 'manage/personalReport.html', context)


def engineerList(select=0):
    
    engineer = ['Product','Question']
        
    profiles = Profile.objects.all()
    
    for profile in profiles:
        
        if not profile.user.is_superuser:
        
            user = profile.user.first_name + '_' +profile.user.last_name+'_'+profile.user.email
            
            engineer.append(user)

    if select == 1:
        
        dict ={}
            
        for key in engineer:
            
            dict2 = {key : 0}
            
            dict.update(dict2)

        return dict

    else:
    
        return engineer


class outputs:


    def product(self, user, question, productresults):
        
        result = productresults.filter(user_id_number=user,question_number=question).values('rating_number')
        if result.count() == 0:
            return "N/A"
        else:
            return result[0].values()[0]


    def programming(self, user, question, programmingresults):
        
        result = programmingresults.filter(user_id_number=user,question_number=question).values('rating_number')
        
        if result.count() == 0:
            return "N/A"
        else:
            return result[0].values()[0]

def handler404(request):
    
    return render(request, 'exception/404.html', status=404)

def handler500(request):
    
    return render(request, 'exception/500.html', status=500)








