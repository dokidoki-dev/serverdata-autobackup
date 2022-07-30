import time
import psutil


class CPU_INFO(object):
    """
    查询CPU信息类
    """

    @staticmethod
    def __cpu_monitor(interval=1, percpu=False):
        """
            查询cpu占用率
            interval: 查询多少秒内cpu平均占用率
            percpu: True 返回一个数组，包含每个cpu占用率，False 默认，返回cpu整体占用率
        """
        num = psutil.cpu_percent(interval, percpu)  # 设置查询3秒中的平均占用率
        return num

    @staticmethod
    def cpu_warn(num=5, time_num=3, warn_rate=50, interval=1, percpu=False):
        """
        cpu监控告警
        warn_rate: cpu: cpu占用率达到此阈值告警
        time_num: 每次轮询等待时间
        num: 轮询cpu占用率次数
        return : True: 告警 False：未告警
        """
        tmp = 0
        for i in range(num):
            result = CPU_INFO().__cpu_monitor(interval, percpu)
            if result >= warn_rate:
                tmp += 1
            time.sleep(time_num)
        if tmp == num:
            return True
        return False
