import subprocess
import shutil
import os
from module.logger import log
from setting import Config

logger = log()


class File(object):
    """
    文件处理类
    """

    @staticmethod
    def compress(new_filename: str, old_path: str):
        """
        文件压缩
        :param new_filename: 压缩后新文件的名称： 绝对路径名称
        :param old_path: 要压缩的文件路径： 绝对路径
        """
        logger.info("开始文件压缩")
        File().dir_if(old_path)
        cmd = "tar -zcPf {0} {1}".format(new_filename, old_path)
        result = subprocess.call(cmd, shell=True)
        logger.info("文件压缩结束")
        if result == 0:
            logger.info("文件压缩成功！")
            return True
        else:
            logger.info("文件压缩失败！")
            return False

    @staticmethod
    def copy(file_type: int, old_path: str, new_path: str):
        """
        文件复制
        :param file_type: 文件类型： 1文件夹 2文件
        :param old_path: 原文件路径： 绝对路径
        :param new_path: 新文件路径： 绝对路径

        """
        logger.info("开始拷贝文件")
        if file_type == 1:
            cmd = "cp -R {0} {1} > /dev/null 2>&1".format(old_path, new_path)
        else:
            cmd = "cp {0} {1} > /dev/null 2>&1".format(old_path, new_path)
        result = subprocess.call(cmd, shell=True)
        logger.info("文件拷贝结束")
        if result == 0:
            logger.info("文件拷贝成功！")
            return True
        else:
            logger.info("文件拷贝失败！")
            return False

    @staticmethod
    def remove(file_type: int, file_path: str):
        """
        删除文件
        :param file_type: 文件类型： 1文件夹 2文件
        :param file_path: 删除的文件，包含绝对路径
        """
        logger.info("开始删除文件")
        if file_type == 1:
            try:
                shutil.rmtree(file_path)
                logger.info("文件删除结束")
            except Exception as e:
                logger.error("error：" + str(e))
                return False
            logger.info("文件夹删除成功")
            return True
        else:
            try:
                os.remove(file_path)
                logger.info("文件删除结束")
            except Exception as e:
                logger.error("error：" + str(e))
                return False
            logger.info("文件删除成功")
            return True

    @staticmethod
    def backup_sql(file_sqlname):
        """
        备份数据库，导出sql
        file_sqlname: 导出的文件，包含绝对路径
        """
        logger.info("开始备份sql")
        user = Config.dbuser
        passwd = Config.dbpasswd
        dbname = Config.dbname
        cmd = "mysqldump -u{0} -h localhost -p{1} {2} > {3}".format(user, passwd, dbname, file_sqlname)
        result = subprocess.call(cmd, shell=True)
        logger.info("备份sql文件结束")
        if result == 0:
            logger.info("sql导出成功")
            return True
        else:
            logger.info("sql导出失败")
            return False

    @staticmethod
    def dir_if(dir_path):
        """
        判断文件夹是否存在，不在则创建
        dir_path: 文件路径
        """
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            logger.info("文件夹成功创建")
        logger.info("文件夹已存在")

    @staticmethod
    def dir_exist(dir_path):
        """
        判断文件夹是否存在
        :param dir_path: 文件路径
        """
        if not os.path.exists(dir_path):
            return False
        return True
