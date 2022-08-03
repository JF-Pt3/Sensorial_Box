from threading import Thread
from time import sleep

from .posture_evaluator import PostureEvaluator
from .posture_peripheral import PosturePeripheral


class PostureFusion:

    def __init__(self, addr1, addr2, name, client, threshold):
        evaluator = PostureEvaluator(threshold, client, "stream/%s" % name, self)

        self.__peripheral1 = PosturePeripheral(addr1, evaluator, 0)
        self.__peripheral2 = PosturePeripheral(addr2, evaluator, 1)

    def start(self):
        t1 = None
        t2 = None

        while True:
            if t1 is None or not t1.is_alive():
                t1 = Thread(target=self.__peripheral1.connect)
                t1.start()
            if t2 is None or not t2.is_alive():
                t2 = Thread(target=self.__peripheral2.connect)
                t2.start()

            sleep(5)

    def vibrate(self, status):
        self.__peripheral1.vibrate(status)
