import oss2
import os
from setting import Config
from module.logger import log

logger = log()


class AliyunOSS(object):
    """
    阿里云oss存储类
    """

    @staticmethod
    def upload(file_name, oss_filename):
        """
        上传文件到oss
        file_name: 要上传的文件名称，包含绝对路径
        oss_path_filename: oss上保存的文件名称
        """
        logger.info("开始oss文件上传")
        oss_path_filename = "wqcsj_backup_data/{0}".format(oss_filename)
        # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
        auth = oss2.Auth(Config.AccessKeyID, Config.AccessKeySecret)
        # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
        # 填写Bucket名称。
        bucket = oss2.Bucket(auth, Config.Endpoint, Config.BucketName)
        # # 必须以二进制的方式打开文件。
        # # 填写本地文件的完整路径。如果未指定本地路径，则默认从示例程序所属项目对应本地路径中上传文件。
        # 指定x-oss-forbid-overwrite为true时，表示禁止覆盖同名Object，如果同名Object已存在，程序将报错。
        headers = dict()
        headers["x-oss-forbid-overwrite"] = "true"
        with open(file_name, 'rb') as fileobj:
            # Seek方法用于指定从第0个字节位置开始读写。上传时会从您指定的第0个字节位置开始上传，直到文件结束。
            fileobj.seek(0, os.SEEK_SET)
            # Tell方法用于返回当前位置。
            current = fileobj.tell()
            # 填写Object完整路径。Object完整路径中不能包含Bucket名称。
            try:
                result = bucket.put_object(oss_path_filename, fileobj, headers=headers)
                logger.info("oss文件上传结束")
            except Exception as e:
                logger.error("阿里oss上传失败：" + str(e))
                return False
        if result.status == 200:
            logger.error("阿里oss上传成功")
            return True
        else:
            logger.error("阿里oss网关api错误")
            return False
