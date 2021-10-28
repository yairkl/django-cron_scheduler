from django.apps import AppConfig
import io

class CronSchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cron_scheduler'
    def ready(self):
        try:
            if is_raspberrypi():
                from .models import Switch
                import RPi.GPIO as GPIO
                switches = Switch.objects.filter(mode=GPIO.OUT)
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)
                for switch in switches:
                    GPIO.setup(switch.id, GPIO.OUT)
                    GPIO.output(switch.id, GPIO.LOW if switch.state else GPIO.HIGH)
        except Exception as e:
            print('ERROR', e)

def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception: pass
    return False

