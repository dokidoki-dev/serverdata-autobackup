import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from module.logger import log
from module.setting import Config

logger = log()


class Mail(object):
    """
    邮件处理类
    """
    @staticmethod
    def sendmail(title="定时备份任务执行消息通知", msg="默认消息"):
        logger.info("开始发送邮件")
        # 发送邮箱服务器
        smtp_server = Config.smtp_server
        # 发送邮箱用户/密码
        user = Config.mail_send_user
        password = Config.mail_send_passwd  # (授权码)
        # 发送邮箱
        sender = Config.mail_send_user
        # 接收邮箱
        receiver = Config.mail_receiver
        # 发送邮件主题
        subject = title
        # 发送的附件
        msg_root = MIMEMultipart('related')
        msg_root['Subject'] = subject
        # 邮件正文内容
        msg_root.attach(MIMEText(msg, 'plain', 'utf-8'))
        # 连接发送邮件
        try:
            # 使用25端口
            # smtp = smtplib.SMTP()
            # smtp.connect(smtp_server)
            # 使用ssl端口
            smtp = smtplib.SMTP_SSL(smtp_server, 465)
            smtp.login(user, password)
            smtp.sendmail(sender, receiver, msg_root.as_string())
            smtp.quit()
            logger.info("邮件发送结束")
        except Exception as e:
            logger.error(e)
            return False
        logger.info("邮件发送成功！")
        return True
