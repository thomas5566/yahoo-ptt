import sys, logging, datetime
sys.path.append("..")

from crawlmovie.spiders.ptt_movies import PttMoviesSpider  # daily
from crawlmovie.spiders.yahoomovie import YahoomovieSpider  # daily
# from crawlmovie.filter import FilterAndInsertData

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.twisted import TwistedScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


logging.basicConfig(
                    filename='SchedulerLog.log',
                    filemode='w',
                    format=('[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s'),
                    datefmt='%H:%M:%S',
                    level=logging.INFO
                )
logging.info("Starting scheduler")

trigger = OrTrigger([
   CronTrigger(hour='15', minute='50'),
   # CronTrigger(hour='16', minute='00'),
   # CronTrigger(hour='23', minute='0-30')
])

def execution_listener(event):
    if event.exception:
        print('The job crashed')
    else:
        print('The job executed successfully')
        # check that the executed job is the first job
        job = scheduler.get_job(event.job_id)
        if job.name == 'yahoo':
            print('Running the second job')
            # lookup the second job (assuming it's a scheduled job)
            jobs = scheduler.get_jobs()
            second_job = next((j for j in jobs if j.name == 'ptt'), None)
            if second_job:
                # run the second job immediately
                second_job.modify(next_run_time=datetime.datetime.now())
            # else:
            #     # job not scheduled, add it and run now
            #     scheduler.add_job(FilterAndInsertData, 'cron', args=[PttMoviesSpider])

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    scheduler = TwistedScheduler()
    scheduler.add_job(process.crawl, trigger, args=[YahoomovieSpider], name='yahoo')
    # scheduler.get_job(job_id ="my_job_id").modify(next_run_time=datetime.datetime.now())
    scheduler.add_job(process.crawl, 'cron', args=[PttMoviesSpider],
                        hour='23', minute='59', name='ptt')
    # scheduler.add_job(FilterAndInsertData, 'cron', day='last sun', name='insertData')
    scheduler.add_listener(execution_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()
    process.start(False)  # Do not stop reactor after spider closes

    # try:
    #     while True:
    #         time.sleep(1)
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown()
