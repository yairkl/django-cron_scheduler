from django.db import models
import os
from .apps import is_raspberrypi as is_pi
if is_pi():
    import RPi.GPIO as GPIO

# class ActionType(models.Model):
#     name=models.CharField(max_length=200)
#     command=models.TextField()

#     def __str__(self):
#         return self.name

# class SwitchType(models.Model):
#     name=models.CharField(max_length=200)
#     status_action=models.ForeignKey(ActionType,on_delete=models.CASCADE)
#     on_action=models.ForeignKey(ActionType,on_delete=models.CASCADE)
#     off_action=models.ForeignKey(ActionType,on_delete=models.CASCADE)

# Create your models here.
class Switch(models.Model):
    switch_types={
        'GPIO':0,
        'TASMOTA':1}

    name = models.CharField(max_length=200)
    id = models.CharField(max_length=200,primary_key=True)
    mode = models.SmallIntegerField(choices=[(0,'Out'),(1,'In')],default=0)
    state = models.BooleanField()
    switch_type = models.SmallIntegerField(choices=[(j,i) for i,j in switch_types.items()],default=0)

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        self.apply_state()

    def apply_state(self):
        if self.switch_type==self.switch_types['GPIO']:
            if  is_pi():
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.id, self.mode)
                if self.mode==0:
                    GPIO.output(self.id, GPIO.HIGH if self.state else GPIO.LOW)
            else:
                print("GPIO at", self.id, 'to state', self.mode)
        elif self.switch_type==self.switch_types['TASMOTA']:
            #TODO implement backend
            print('Tasmota at',self.id ,'to state', self.mode)

class Action(models.Model):
    days={
        '0':'Sunday',
        '1':'Monday',
        '2':'Tuesday',
        '3':'Wednesday',
        '4':'Thursday',
        '5':'Friday',
        '6':'Saturday',
        '*':'Everyday'
    }
    rev_days = {d:i for i,d in days.items() }
    switch = models.ForeignKey(Switch,on_delete=models.CASCADE)
    action = models.ForeignKey(ActionType,on_delete=models.CASCADE)
    day = models.CharField(max_length=1,choices=[(i,j) for i,j in days.items()])
    time = models.TimeField()
    params = models.JSONField(default=dict)


    def day_to_str(self):
        return self.days[self.day]

    def cron_str(self):
        return f'{self.time.minute} {self.time.hour} * * {self.day} {self.action.command.format(switch=self.switch.id,**self.params)}'


    def __str__(self):
        return f'on {self.day_to_str()} at {self.time} preform {self.action} on {self.switch}'

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        with open('cron.txt','w') as file:
            file.write('\n'.join([i.cron_str() for i in Action.objects.all()])+'\n')
        os.system('crontab cron.txt')
    
    def delete(self,*args,**kwargs):
        super().delete(*args,**kwargs)
        with open('cron.txt','w') as file:
            file.write('\n'.join([i.cron_str() for i in Action.objects.all()])+'\n')
        os.system('crontab cron.txt')

