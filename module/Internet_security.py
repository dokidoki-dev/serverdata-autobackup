from module.logger import log
import requests

logger = log()


class Security(object):
    """
    网络安全检查处理类，确保存储的数据是安全的数据
    """
    @staticmethod
    def scan_baidu(file_path):
        """
        网络安全检查
        file_path: 要检查的文件，包含绝对路径
        """
        logger.info("开始创建安全扫描任务")
        url = "https://scanner.baidu.com/enqueue"
        file = {
            "archive": open(file_path, 'rb')
        }
        try:
            r = requests.post(url=url, files=file, timeout=120)
            logger.info("创建安全扫描任务结束")
        except Exception as e:
            logger.error(e)
            return 0
        if r.status_code != 200:
            logger.info("百度安全api网络错误")
            return 0
        try:
            task_md5 = r.json().get("md5")
            task_url = r.json().get("url")
        except Exception as e:
            logger.error("scan_baidu: " + str(e))
            return 0
        result = {"task_md5": task_md5, "task_url": task_url}
        logger.info(result)
        return result

    @staticmethod
    def result_baidu(task_md5: str, task_url: str):
        """
        获取文件扫描结果
        task_md5: 百度安全接口返回的md5
        task_url： 百度安全接口返回的url
        :return 0:失败，或任务不存在 1: 任务正在进行中 2: 任务结束，没有发现安全风险 返回{"detected": int}发现的风险文件数量
        """
        logger.info("开始安全检查")
        try:
            r = requests.get(url=task_url, timeout=120)
            logger.info("安全检查结束")
        except Exception as e:
            logger.error(e)
            return 0
        if r.status_code != 200:
            logger.info("百度安全api网络错误")
            return 0
        result = r.json()[0]
        if result.get("status") == "pending":
            logger.info("定时任务还在进行中")
            return 1
        if result.get("md5") != task_md5:
            logger.info("md5值异常")
            return 0
        if result.get("detected") == 0:
            logger.info("安全检查执行通过，文件无风险")
            return 2
        unsafe_info = result.get("data")
        logger.info("发现的风险文件信息：" + str(unsafe_info))
        return {"detected": result.get("detected")}
