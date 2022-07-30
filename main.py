from module.logger import log
from module.mail import Mail
from apscheduler.schedulers.blocking import BlockingScheduler
from module.run_case import run, cpu_run
from module.file import File
from setting import Config, Tmp_var

logger = log()


def task():
    # 服务器定时备份任务
    result = run()
    # 发送邮件
    if result:
        Mail().sendmail("定时任务执行成功通知", "服务器定时备份任务执行成功！")
        logger.info("定时备份任务执行成功")
    else:
        Mail().sendmail("定时任务执行失败通知", "服务器定时备份任务执行失败，请登录服务器查看失败日志！")
        logger.info("定时备份任务执行失败")
    result = File().dir_exist(Config.web_path_backup)
    if result:
        File().remove(1, Config.web_path_backup)
        logger.info("网站备份文件夹删除成功")


def task_001():
    if Tmp_var.if_send:
        return
    # cpu占用率监测任务
    result = cpu_run()
    # 发送邮件
    if result:
        Mail().sendmail("服务器CPU占用率过高通知", "服务器CPU占用率已经超过50%，请关注！")
        logger.info("服务器CPU占用率过高")
    Tmp_var.sends_mail_num += 1
    if Tmp_var.sends_mail_num >= 3:
        Tmp_var.if_send = True


if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(task, 'interval', days=15)
    scheduler.add_job(task_001, 'interval', minutes=1)
    scheduler.start()
