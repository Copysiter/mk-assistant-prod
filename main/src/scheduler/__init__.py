from apscheduler.schedulers.background import BackgroundScheduler

from .tasks import run_daily_tasks, run_hourly_tasks, run_minutely_tasks

scheduler = BackgroundScheduler({"apscheduler.timezone": "UTC"})

scheduler.add_job(
    run_minutely_tasks, trigger="cron", month="*", day="*", hour="*", minute="*/1"
)
scheduler.add_job(
    run_hourly_tasks, trigger="cron", month="*", day="*", hour="*", minute="1"
)
scheduler.add_job(
    run_daily_tasks, trigger="cron", month="*", day="*", hour="0", minute="1"
)
