from django_cron import CronJobBase, Schedule
from geoscience_api.views import check_earthquake_and_notify

class EarthquakeNotificationCronJob(CronJobBase):
    RUN_EVERY_MINS = 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'earthquake.earthquake_notification_cron_job'

    def do(self):
        check_earthquake_and_notify()
