from apscheduler.schedulers.background import BackgroundScheduler,BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import datetime
import sys
import os 
import time

cpath_current = os.path.dirname(os.path.dirname(__file__))
sys.path.append(cpath_current)
from instock.job.basic_data_daily_job import main as main_dj

#后台任务
scheduler = BlockingScheduler()
def my_task():
    main_dj()
    print("每隔3s执行任务")

scheduler.add_job(my_task, IntervalTrigger(seconds=2))

##启动调度器
scheduler.start()
# i = 0
# while 1:
#     main_dj()
#     i += 1
#     print(i)
#     time.sleep(10)
# main_dj()
