#!/usr/bin/env python

from  time import sleep
from perf_tool import PerfTool, perf_tool

@perf_tool('main')
def main():
    @perf_tool('body')
    def scoped(): sleep(0.05)
    with PerfTool('call'): scoped()
    for row in range(10):
        with PerfTool('row'):
            sleep(0.001)

PerfTool.set_enabled()
main()
PerfTool.show_stats_if_enabled()

