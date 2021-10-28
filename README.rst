=====
Cron_scheduler
=====

Cron_scheduler is a Django app to control and schedule tasks on Raspberry-pi GPIOs.

Quick start
-----------

1. Add "cron_scheduler" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'cron_scheduler',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('scheduler/', include('cron_scheduler.urls')),

3. Run ``python manage.py migrate`` to create the cron_scheduler models.

4. Make shure the timezone is set currectly

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to create tasks (you'll need the Admin app enabled).

6. Visit http://127.0.0.1:8000/scheduler/ to scedule tasks.

