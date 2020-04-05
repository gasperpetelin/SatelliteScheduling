from unittest import TestCase

from evaluator import accessWindowObj, communicationClashObj, communicationTimeRequirementObj, groundStationUsageObj
from problem import Timewindow, ProblemInstance, Schedule, Event, Requirement

tw1 = [Timewindow(GS=1, SC=1, tAos=100, tLos=200),
       Timewindow(GS=1, SC=1, tAos=300, tLos=400),
       Timewindow(GS=1, SC=1, tAos=500, tLos=600),
       Timewindow(GS=1, SC=1, tAos=700, tLos=800)]

pi1 = ProblemInstance(nDays=10, nSC=1, nGS=1, timewindows=tw1, requirements=[])

reqs2 = [Requirement(SC=1, tBeg=100, tEnd=200, tReq=20), Requirement(SC=1, tBeg=300, tEnd=500, tReq=100)]

pi2 = ProblemInstance(nDays=10, nSC=1, nGS=1, timewindows=[], requirements=reqs2)


class TestEvaluator(TestCase):
    # Test accessWindowObj
    def test_evaluate1(self):
        sc = Schedule([Event(SC=1, GS=1, tStart=10, tDur=200)])
        self.assertAlmostEqual(accessWindowObj(pi1, sc), 0, places=5)

    def test_evaluate2(self):
        sc = Schedule([Event(SC=1, GS=1, tStart=110, tDur=30)])
        self.assertAlmostEqual(accessWindowObj(pi1, sc), 100, places=5)

    def test_evaluate3(self):
        sc = Schedule([Event(SC=1, GS=1, tStart=110, tDur=30), Event(SC=1, GS=1, tStart=160, tDur=10)])
        self.assertAlmostEqual(accessWindowObj(pi1, sc), 100, places=5)

    def test_evaluate4(self):
        sc = Schedule([Event(SC=1, GS=1, tStart=110, tDur=30), Event(SC=1, GS=1, tStart=160, tDur=50)])
        self.assertAlmostEqual(accessWindowObj(pi1, sc), 50, places=5)

    def test_evaluate5(self):
        sc = Schedule([Event(SC=1, GS=1, tStart=110, tDur=130), Event(SC=1, GS=1, tStart=160, tDur=150)])
        self.assertAlmostEqual(accessWindowObj(pi1, sc), 0, places=5)

    def test_evaluate6(self):
        sc = Schedule([Event(SC=1, GS=1, tStart=520, tDur=20), Event(SC=1, GS=1, tStart=760, tDur=30)])
        self.assertAlmostEqual(accessWindowObj(pi1, sc), 100, places=5)

    # Test communicationClashObj
    def test_evaluate7(self):
        sc = Schedule([Event(SC=1, GS=1, tStart=520, tDur=100), Event(SC=1, GS=1, tStart=600, tDur=30)])
        self.assertAlmostEqual(communicationClashObj(pi1, sc), 50, places=5)

    def test_evaluate8(self):
        sc = Schedule([Event(SC=1, GS=1, tStart=520, tDur=100),
                       Event(SC=1, GS=1, tStart=600, tDur=30),
                       Event(SC=1, GS=2, tStart=610, tDur=130)])
        self.assertAlmostEqual(communicationClashObj(pi1, sc), 100 * 2 / 3, places=5)

    def test_evaluate9(self):
        sc = Schedule([Event(SC=1, GS=1, tStart=100, tDur=100),
                       Event(SC=1, GS=1, tStart=140, tDur=100),
                       Event(SC=1, GS=1, tStart=170, tDur=100)])
        self.assertAlmostEqual(communicationClashObj(pi1, sc), 100 * 1 / 3, places=5)

    def test_evaluate10(self):
        sc = Schedule([Event(SC=1, GS=1, tStart=100, tDur=100),
                       Event(SC=1, GS=2, tStart=140, tDur=100),
                       Event(SC=1, GS=1, tStart=170, tDur=100)])
        self.assertAlmostEqual(communicationClashObj(pi1, sc), 100 * 2 / 3, places=5)

    # Test communicationTimeRequirementObj
    def test_evaluate11(self):
        sc = Schedule([Event(SC=1, GS=1, tStart=100, tDur=100)])
        self.assertAlmostEqual(communicationTimeRequirementObj(pi2, sc), 50, places=5)

    def test_evaluate12(self):
        sc = Schedule([Event(SC=1, GS=1, tStart=90, tDur=20)])
        self.assertAlmostEqual(communicationTimeRequirementObj(pi2, sc), 0, places=5)

    def test_evaluate13(self):
        sc = Schedule([Event(SC=1, GS=1, tStart=90, tDur=2000)])
        self.assertAlmostEqual(communicationTimeRequirementObj(pi2, sc), 100, places=5)

    def test_evaluate14(self):
        sc = Schedule([Event(SC=1, GS=1, tStart=90, tDur=20), Event(SC=1, GS=1, tStart=150, tDur=15)])
        self.assertAlmostEqual(communicationTimeRequirementObj(pi2, sc), 50, places=5)

    # Test groundStationUsageObj
    def test_evaluate15(self):
        sc = Schedule([Event(SC=1, GS=1, tStart=90, tDur=20), Event(SC=1, GS=1, tStart=150, tDur=15)])
        self.assertAlmostEqual(groundStationUsageObj(pi2, sc), 0.17361111111, places=5)
