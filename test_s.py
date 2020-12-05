from perf_tool import PerfTool, perf_tool
import time
import pytest


class Case1:
    """
    Class that represent some piece of code
    sleep is a placeholed for time consuming algorithm
    """

    # used like a decorator
    @perf_tool('meth1')
    def meth1(self):
        time.sleep(0.01)

    @perf_tool('nested')
    def meth2(self):
        time.sleep(0.01)
        for x in range(5):
            # used as a context manager
            with PerfTool('internal'):
                time.sleep(0.01)
                for x in range(2):
                    with PerfTool('internal2'):
                        time.sleep(0.01)




@pytest.fixture()
def on_run_off():
    # Singleton instance
    assert PerfTool.set_enabled()
    yield
    assert PerfTool.show_stats_if_enabled(return_if_succeeded=True)
    assert not PerfTool.set_enabled(False)
    assert PerfTool.show_stats_if_enabled(return_if_succeeded=True)
    PerfTool.empty()
    assert not PerfTool.t0
    assert not PerfTool.times
    assert not PerfTool.running


def test_algo1(on_run_off):
    aa = Case1()
    for x in range(3):
        aa.meth1()
        aa.meth2()

    for x in range(5):
        # as a context manager
        with PerfTool('meth2'):
            time.sleep(0.01)


    assert PerfTool.has('meth2')
    assert PerfTool.has('meth1')
    assert PerfTool.has('nested')
    assert PerfTool.has('nested.internal')
    assert PerfTool.has('nested.internal.internal2')



@perf_tool('main')
def main():
    """
    Dummy example of use
    """
    with PerfTool('preparation'):
        time.sleep(0.01)

    with PerfTool('calculus'):
        time.sleep(0.03)

    with PerfTool('output'):
        time.sleep(0.02)
        for row in range(100):
            with PerfTool('row write'):
                time.sleep(0.001)


def test_sample1(on_run_off):
    main()



