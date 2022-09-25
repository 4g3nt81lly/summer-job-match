#views
from textwrap import indent
from django.shortcuts import render

# Create your views here.


from django.shortcuts import render

from django import forms
from django.forms import fields
from django.forms import widgets
from django.shortcuts import render,redirect,HttpResponse,reverse

from findbestjob import models



# Create your views here.

# Home page
def index(request):
    return render(request,'index.html')



class LoginForm(forms.Form):

    account = fields.CharField(
        widget=widgets.TextInput(attrs={ "class": "form-control" }),
        required=True,
        max_length=50,
        min_length=4,
        error_messages={ "required": "Cannot be blank" }
    )

    password = fields.CharField(
        widget=widgets.TextInput(attrs={ "type": "password",
                                        "class": "form-control" }),
        required=True,
        max_length=50,
        error_messages={ "required": "Cannot be blank" }
    )


class RegisterForm(forms.Form):
    name = fields.CharField(
        required=True,
        max_length=50,
        min_length=4,
        error_messages={ "required": "Cannot be blank" }
        )

    account = fields.CharField(
        required=True,
        max_length=50,
        min_length=4,
        error_messages={ "required": "Cannot be blank" }
        )

    password = fields.CharField(
        required=True,
        max_length=50,
        min_length=4,
        error_messages={ "required": "Cannot be blank" }
    )

    gender = fields.CharField(
        widget=widgets.RadioSelect(choices=[(1, "Male"),
                                            (2, "Female")]),   #single choice radio
        initial = 2,
    )
    age = fields.CharField(
        widget=widgets.TextInput(attrs={"type": "number",
                                        "min": "14",
                                        "max": "20"}),
        required=True,
        initial=14,
        error_messages={ "required": "Cannot be blank" }
    )

    address = fields.CharField(
        required=True,
        max_length=128,
        min_length=3,
        error_messages={ "required": "Cannot be blank" }
    )



class SurveyForm(forms.Form):
    q1 = fields.CharField(
        required=True,
        label="1 Which field do you prefer to work in?",
        widget=widgets.RadioSelect(
            choices=[
                (1, "Business"),
                (2, "Liberal Arts & Humanities"),
                (3, "Math, Science & Technology"),
                (4, "Fine Arts & Design"),
            ]
        ), # single choice radio
        initial=1,
    )
    q2 = fields.CharField(
        required=True,
        label="2 Your expected working days per week",
        widget=widgets.RadioSelect(
            choices=[
                (1, "1-2 days a week"),
                (2, "2-3 days a week"),
                (3, "4-6 days a week"),
                (4, "6-7 days a week"),
            ]
        ), # single choice radio
        initial=1,
    )
    q3 = fields.CharField(
        required=True,
        label="3 Your expectation for daily working duration",
        widget=widgets.RadioSelect(
            choices=[
                (1, "1-3 h"),
                (2, "3-6 h"),
                (3, "6-9 h"),
                (3, "more than 9h"),
            ]
        ), # single choice radio
        initial=1,
    )
    q4 = fields.CharField(
        required=True,
        label="4 Your expectation of hourly wage ($/h)?",
        widget=widgets.RadioSelect(
            choices=[
                (1, "5-10$"),
                (2, "10-15$"),
                (3, "15-20$"),
                (4, "20-25$"),
            ]
        ), # single choice radio
        initial=1,
    )
    q5=fields.CharField(
        required=True,
        label="5 How much do you expect this job to help you in college application?",
        widget=widgets.RadioSelect(
            choices=[
                (1, "1"),
                (2, "2"),
                (3, "3"),
                (4, "4"),
            ]
        ), # single choice radio
        initial=1,
    )

# Log in page
def login(request):
    obj = LoginForm()
    if request.method == 'POST':
        info_dic = {
            'account': request.POST.get('account'),
            'password': request.POST.get('password')
        }
        user_obj = models.Student.objects.filter(account=info_dic.get('account')).first()
        if user_obj:
            if info_dic['password'] == user_obj.password:
                return redirect('/findbestjob/survey?sid=' + str(user_obj.id))
            else:
                #return HttpResponse('Password error')
                #return redirect('/findbestjob/login',{'errorInfo':''})
                return render(request,'login.html',{'errorInfo': 'Password error',
                                                    'obj': obj})
        else:
            #return HttpResponse('User does not exist')
            return redirect('/findbestjob/register')

    #obj = LoginForm()
    return render(request,'login.html',{'obj':obj})


def register(request):
    if request.method == "GET":
        obj = RegisterForm()
        # render(request,'register.html',{"obj":obj})

    if request.method == 'POST':
        obj = RegisterForm(request.POST)
        '''
        obj_dic = {
            'name':request.POST.get('name'),
            'account':request.POST.get('account'),
            'gender':request.POST.get('gender'),
            'age':request.POST.get('age'),
            'password':request.POST.get('password'),
            'address':request.POST.get('address')
        }
        '''
        obj_dic = {}
        for field in obj:
            obj_dic[field.name] = request.POST.get(field.name)

        # print(obj_dic)
        student = models.Student.objects.create(**obj_dic)
        return redirect('/findbestjob/survey?uid=' + str(student.id))

    return render(request, 'register.html', {'obj': obj})


def survey(request):
    if request.method == "GET":
        obj = SurveyForm()
        render(request, 'survey.html', {"obj": obj})

    if request.method == 'POST':
    #Save the survey
        obj = SurveyForm(request.POST)
        sid = request.GET.get("sid")
        obj_dic = {}
        for field in obj:
            obj_dic[field.name] = request.POST.get(field.name)
        obj_dic["sid"] = sid  # student id
        answer = models.Answer.objects.create(**obj_dic)
        return redirect('/findbestjob/radar?sid=' + str(answer.sid) + '&aid=' + str(answer.id))

    return render(request, 'survey.html', {'obj': obj})


# install pyecharts first using comand as below:
#   pip3 install pyecharts

from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker
from django.http import HttpResponse
from pyecharts.charts import Radar
import pyecharts.options as opts

top_n = 3
def find_best_job(a,top_n):
    sql = "select id,title,company,abs(ind1-%s)+abs(ind2-%s)+abs(ind3-%s)+abs(ind4-%s)+abs(ind5-%s) as ind6 from findbestjob_job order by ind6 asc limit %s"
    jobs = models.Job.objects.raw(sql, [a[0], a[1], a[2], a[3], a[4], top_n])
    return jobs


def radar(request):

    aid = request.GET.get("aid")
    #get the job id & info
    jid = request.GET.get("jid")
    #Get the user answer of job quetionnaire fro database
    answer = models.Answer.objects.get(pk=int(aid))
    v1 = [[int(answer.q1), int(answer.q2), int(answer.q3), int(answer.q4), int(answer.q5)]]
    job = None
    #Finding the best top n job (current setting is top3)
    querySet = find_best_job(v1[0], top_n)
    #The most suitable job
    jobs = []
    for j in querySet:
        jobs.append(j)
    if job == None and jobs:
        job = jobs[0]
    if jid:
        job = models.Job.objects.get(pk=int(jid))
    #The five index of the best fit job
    v2 = [[job.ind1, job.ind2, job.ind3, job.ind4, job.ind5]]

    c = (
        Radar(init_opts=opts.InitOpts(bg_color="#ffffff"))
        .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="Working Field", max_=8),
                opts.RadarIndicatorItem(name="Working Day", max_=8),
                opts.RadarIndicatorItem(name="Working Hour", max_=8),
                opts.RadarIndicatorItem(name="Hourly Wage" , max_=8),
                opts.RadarIndicatorItem(name="Help in Application", max_=8),

            ],
            splitarea_opt=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=0.5,
                    color= {
                        "type": 'radial',
                        "x": 0.5,
                        "y": 0.5,
                        "r": 0.5,
                        "colorStops": [{
                         "offset": 0, "color": '#ff0000' # 0% color
                        }, {
                        "offset": 1, "color": '#ffdddd' # 100% color
                        }],

                    }
                )
            ),
            textstyle_opts=opts.TextStyleOpts(color="black"),
        )
        .add(
            series_name="Your requirements ",
            data=v1,
            linestyle_opts=opts.LineStyleOpts(color="#CD0000"),
        )
        .add(
            series_name=job.title,
            data=v2,
            linestyle_opts=opts.LineStyleOpts(color="#0000FF"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Matching result and radar chart"),
            legend_opts=opts.LegendOpts()
        )

    )

    return render(request, 'radar.html', {
        'radar_chart1': c.render_embed(),
        'aid': aid,
        'job1': {"title": jobs[0].title,
                 "id": jobs[0].id,
                 "company": jobs[0].company},
        'job2': {"title": jobs[1].title,
                 "id": jobs[1].id,
                 "company": jobs[1].company},
        'job3': {"title": jobs[2].title,
                 "id": jobs[2].id,
                 "company": jobs[2].company},
    })

    #return  HttpResponse(c.render_embed())
