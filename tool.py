from collections.abc import Callable, Iterable, Mapping
from typing import Any
import json
import threading
import time


def getJson(j: object):
    '''快速获取json'''
    if hasattr(j, "__dict__") == False:  # 普通类型
        return j
    o = {}
    for key in j.__dict__:
        attr = getattr(j, key)
        if isinstance(attr, list):
            for c in attr:
                o[key] = []
                o[key].append(getJson(c))
                pass
        elif hasattr(attr, "__dict__") == True:
            o[key] = getJson(attr)  # type:ignore
        else:
            o[key] = attr
    return o


class QJson():
    '''快速json对象,子属性只适用普通类型,不能套娃!!!'''

    def __init__(self) -> None:
        pass

    def tojson(self):
        return getJson(self)

    def loadjson(self, s: str):
        j = json.loads(s)
        for key in j:
            setattr(self, key, j[key])
        pass


class JThread(threading.Thread):
    '''自制线程器'''

    def __init__(self, target, args=()):
        super(JThread, self).__init__()
        self.target = target
        self.args = args
        self.stop_event = threading.Event()

    def pause(self):
        self.stop_event.wait()

    def resume(self):
        self.stop_event.clear()

    def stop(self):
        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():
            self.target(*self.args)
            time.sleep(1)
