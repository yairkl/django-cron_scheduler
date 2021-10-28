from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Switch,Action,ActionType

# Create your views here.

def index(request):
    # handle new action post
    if request.method=='POST':
        add_action(request.POST)
        return HttpResponseRedirect(request.path)
    # handle delete request
    elif request.GET.get('delete'):
        Action.objects.get(id=int(request.GET.get('delete'))).delete()
        return HttpResponseRedirect(request.path)
    
    actions = {d:Action.objects.filter(day=n).order_by('time') for n,d in Action.days.items()}
    switches = Switch.objects.all()
    action_types = ActionType.objects.all()
    return render(request,'index.html',{'title':'home','actions':actions,'days_map':Action.days,'switches':switches,'actionTypes':action_types})

def day(request,day:str):
    # handle new action post
    if request.method=='POST':
        add_action(request.POST)
        return HttpResponseRedirect(request.path)
    # handle delete request
    elif request.GET.get('delete'):
        Action.objects.get(id=int(request.GET.get('delete'))).delete()
        return HttpResponseRedirect(request.path)
    
    actions = Action.objects.filter(day=Action.rev_days[day]).order_by('time')
    switches = Switch.objects.all()
    action_types = ActionType.objects.all()

    return render(request,'day.html',{'title':day,'actions':actions,'day':day,'days_map':Action.days,'switches':switches,'actionTypes':action_types})

def add_action(data):
    act_id = int(data.get('id')) if data.get('id') else None
    day = data.get('day')
    time = data.get('time')
    switch = Switch.objects.get(id=int(data.get('switch')))
    action = ActionType.objects.get(id=int(data.get('action')))
    act = Action(id=act_id,day=day,time=time,switch=switch,action=action)
    act.save()

def getState(request,id):
    switch = Switch.objects.get(id=id)
    return HttpResponse(switch.state)

def setState(request,id,state):
    switch=Switch.objects.get(id=id)
    switch.state=(state==1)
    switch.save()
    return HttpResponse(switch.state)
