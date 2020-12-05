# -*- coding: utf-8 -*-
__author__ = 'Gla'

from collections import defaultdict
from functools import wraps
from threading import Lock
from time import time
import math
import functools
import traceback

lock = Lock()




def star(f):
    """
    An helper function to lack of tuple unpacking in py3
    """
    @functools.wraps(f)
    def f_inner(args):
        return f(*args)
    return f_inner


def mean(v):
    """
    mean function of bounch of values
    """
    return sum(v) / len(v)

def variance(v, ddof=0):
    """
    variance function of bounch of values
    """
    n = len(v)
    return sum((x - mean(v)) ** 2 for x in v) / (n - ddof)

def stdev(v):
    """
    standard devfiation function of bounch of values
    """
    var = variance(v)
    std_dev = math.sqrt(var)
    return std_dev


class Singleton(object):
    _instances = {}
    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            #class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
            class_._instances[class_] = super(Singleton, class_).__new__(class_)
        return class_._instances[class_]


def perf_tool(tsk):
    """
    Function decorator

    :param tsk:
    :return:
    """
    def decorator(fun):
        @wraps(fun)
        def dec_func(*args, **kw):
            with PerfTool(tsk):
                return fun(*args, **kw)
        return dec_func
    return decorator


class PerfTool(Singleton):
    """
    Context Manager

    A Compund timer with the purpose of collect partial timing
    It consider nested procedures, and calculate each time separately.

    nested tasks are deduced from the lenght from the code flow.
    so the same function called by different stack, can be followed punctually

    Can be enabled and disabled at runtime
    """
    times = defaultdict(list)
    running = []  # I'm a mutable... but singleton!
    t0 = []
    enabled = False
    cum_stats = 'sum'  # which stats must be used for sorting? probably sum | mean

    def __init__(self, tsk):
        if self.enabled:
            self.running.append(tsk)

    def __enter__(self):
        if self.enabled:
            self.t0.append(time())

    def __exit__(self, type, value, traceback):
        if self.enabled:
            delta = time() - self.t0.pop()
            self.times[tuple(self.running)].append(delta)
            self.running.pop()

    @classmethod
    def set_enabled(cls, enabled=True):
        cls.enabled = enabled
        return cls.enabled

    @classmethod
    def has(cls, key):
        """
        Return True or False if key was collected
        This works either if collector was not enabled

        nested method can be reached using dotted notation:

        PT.has('root')
        PT.has('root.sub1')
        PT.has('root.sub1.sub2.subn')

        """
        return tuple(key.split('.')) in cls.times.keys()

    @classmethod
    def empty(cls):
        """
        Reset internal status,
        in multiple use without contamination

        return: None
        """
        cls.times = defaultdict(list)
        cls.running = []
        cls.t0 = []


    @classmethod
    def show_stats_if_enabled(cls, return_if_succeeded=False):
        try:
            if cls.enabled:

                d = {}

                for k, v in cls.times.items():
                    stats = {'count': len(v),
                             'mean': mean(v),
                             'sum': sum(v),
                             'std': stdev(v),
                             'sub': {}}
                    d[k] = stats
                    d[k]['cum'] = stats[cls.cum_stats]

                # Hadling nested tasks, Root task inherits cum timer from sub task
                for k in sorted(cls.times.keys(), key=lambda k: len(k), reverse=True):
                    if len(k) > 1:
                        d[k[:-1]]['sub'][k] = d[k]
                        d[k[:-1]]['cum'] += d[k]['cum']

                print("=" * 18, 'PerfTool', "=" * 18)
                print("{k:25}|{mean:8}|{sum:8}|{count:8}|{std:8}".format(k='task', mean='aver(s)', sum='sum(s)', count='count', std='std'))

                def nested_print(k, v, level=0, done=[]):
                    if k not in done:
                        if level:
                            prefix = '  ' * level + '+-'
                        else:
                            prefix = ''
                        print("{k:25.25}|{mean:8.3f}|{sum: 8.3f}|{count:8}|{std:8.3f}".format(k=prefix + k[-1], **v))
                        done.append(k)

                    if v.get('sub'):
                        for _k, _v in v['sub'].items():
                            nested_print(_k, _v, level + 1)

                for k, v in sorted(d.items(),
                                   key=star(lambda k, v: v['cum']),
                                   reverse=True):
                    nested_print(k, v)

                print()
                print("{k:25}|{mean:8.2f}|{sum: 8.2f}|{count:8}|{std:8}".format(k='overall',
                                                                                mean=mean(
                                                                                    [v['mean'] for v in d.values()]),
                                                                                sum=sum(
                                                                                    [v['sum'] for k, v in d.items() if len(k) < 2]),
                                                                                count=sum(
                                                                                    [v['count'] for v in d.values()]),
                                                                                std='-'))
        except Exception as err:
            print("Sorry something went wrong with CompTimer")
            print(traceback.format_exc())
            cls.set_enabled(False)
            if return_if_succeeded:
                return False
        else:
            if return_if_succeeded:
                return True


