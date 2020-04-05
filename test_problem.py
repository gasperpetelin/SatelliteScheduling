from unittest import TestCase

from problem import Timewindow, Requirement, Event, ProblemInstance, Schedule

tw = Timewindow(GS=3, SC=1, tAos=120, tLos=300)
rq = Requirement(SC=1, tBeg=1000, tEnd=2000, tReq=100)
ev = Event(SC=1, GS=2, tStart=50, tDur=100)


class TestTimewindow(TestCase):
    def test_tw1(self):
        self.assertEqual(str(tw), '(GS: 3, SC: 1, tAos: 120, tLos: 300)')


class TestRequirement(TestCase):
    def test_rq1(self):
        self.assertEqual(str(rq), '(SC: 1, tBeg: 1000, tEnd: 2000, tReq: 100)')


class TestEvent(TestCase):
    def test_ev1(self):
        self.assertEqual(str(ev), '(SC: 1, GS: 2, tStart: 50, tDur: 100)')


class TestProblemInstance(TestCase):
    def test_pi1(self):
        pi = ProblemInstance(nDays=5, nSC=3, nGS=4, timewindows=[tw], requirements=[rq])
        self.assertEqual(str(pi), '(nDays: 5, nSC: 3, nGS: 4, timewindows: 1, requirements: 1)')


class TestSchedule(TestCase):
    def test_sc1(self):
        sc = Schedule([ev])
        sc.addSolutionPair(ev)
        self.assertEqual(len(sc), 2)

    def test_sc2(self):
        sc = Schedule([ev])
        sc.addSolutionPair(ev)
        for x in sc:
            self.assertEqual(str(x), '(SC: 1, GS: 2, tStart: 50, tDur: 100)')
