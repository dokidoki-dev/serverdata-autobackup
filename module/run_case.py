from module.file import File
import time
from module.Internet_security import Security
from module.oss_store import AliyunOSS
from module.logger import log
from setting import Config
from module.cpu_info import CPU_INFO

logger = log()


def run():
    # 复制文件
    File().dir_if(Config.web_tmp_path_backup)
    result = File().copy(file_type=1, old_path=Config.web_file_path, new_path=Config.web_tmp_path_backup)
    if not result:
        return False
    # 压缩文件
    time_tmp = time.strftime("%Y-%m-%d", time.localtime())
    file_name = "blog_file_{0}.tar.gz".format(time_tmp)
    file_tmp_name = "/root/backup/files/{0}".format(file_name)
    result = File().compress(file_tmp_name, Config.web_path_backup)
    if not result:
        return False
    # 安全检查
    result = Security().scan_baidu(file_tmp_name)
    if result == 0:
        File().remove(2, file_tmp_name)
        return False
    ok = Security().result_baidu(result["task_md5"], result["task_url"])
    if ok == 1:
        num = 0
        while 1:
            num += 1
            time.sleep(5)
            ok = Security().result_baidu(result["task_md5"], result["task_url"])
            if ok != 1:
                break
            if num > 20:
                logger.info("轮询安全检查api任务超时")
                File().remove(2, file_tmp_name)
                return False
    if ok == 0:
        File().remove(2, file_tmp_name)
        return False
    if ok != 2:
        File().remove(2, file_tmp_name)
        logger.error("发现风险文件数量：" + str(ok))
        return False
    # 处理sql，导出sql备份
    sql_name = "blog_data_{0}.sql".format(time_tmp)
    sql_tmp_name = "/root/backup/sql/{0}".format(sql_name)
    result = File().backup_sql(sql_tmp_name)
    if result == 0:
        File().remove(2, file_tmp_name)
        return False
    # 上传文件到oss存储
    oss_path_file = "web_files/{0}".format(file_name)
    result = AliyunOSS().upload(file_tmp_name, oss_path_file)
    if not result:
        return False
    oss_path_sql = "blog_sql/{0}".format(sql_name)
    result = AliyunOSS().upload(sql_tmp_name, oss_path_sql)
    if not result:
        return False
    # 删除备份过的文件
    result = File().remove(2, file_tmp_name)
    if not result:
        return False
    result = File().remove(2, sql_tmp_name)
    if not result:
        return False
    result = File().remove(1, Config.web_path_backup)
    if not result:
        return False
    return True


def cpu_run():
    # cpu占用率检测
    result = CPU_INFO.cpu_warn()
    return result


