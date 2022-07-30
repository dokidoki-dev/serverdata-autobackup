class Config:
    dbname = ""  # 数据库名字
    dbuser = ""  # 数据库用户
    dbpasswd = ""  # 数据库密码
    mail_send_user = ""  # 邮件发件人
    mail_send_passwd = ""  # 授权码
    smtp_server = ""  # smtp服务器
    mail_receiver = ""  # 邮件接收人
    AccessKeyID = ""  # 阿里云oss子账号的AccessKeyID
    AccessKeySecret = ""  # 阿里云oss子账号的AccessKeySecret
    Endpoint = ""  # oss所在地域Bucket地址
    BucketName = ""  # Bucket名称
    web_path_backup = ""  # 网站web备份文件夹
    web_file_path = ""  # 网站web文件路径
    web_tmp_path_backup = ""  # 网站web文件临时备份路径


class Tmp_var:
    """
    存储全局变量(非配置)
    此处变量不可人为手动修改，必须使用此处设置的默认值
    """
    # 是否发送了告警邮件 必须为False， 如果被程序修改为True后，只能重启程序后才可以再次发送告警邮件，用来防止服务器占用过高导致频繁邮件告警
    if_send = False
    # 邮件发送次数
    sends_mail_num = 0
