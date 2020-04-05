class Timewindow:
    def __init__(self, SC, GS, tAos, tLos):
        self.tLos = tLos
        self.tAos = tAos
        self.SC = SC
        self.GS = GS

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '(GS: {}, SC: {}, tAos: {}, tLos: {})'.format(self.GS, self.SC, self.tAos, self.tLos)


class Requirement:
    def __init__(self, SC, tBeg, tEnd, tReq):
        self.SC = SC
        self.tBeg = tBeg
        self.tEnd = tEnd
        self.tReq = tReq

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '(SC: {}, tBeg: {}, tEnd: {}, tReq: {})'.format(self.SC, self.tBeg, self.tEnd, self.tReq)


class Event:
    def __init__(self, SC, GS, tStart, tDur):
        self.SC = SC
        self.GS = GS
        self.tStart = tStart
        self.tDur = tDur

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '(SC: {}, GS: {}, tStart: {}, tDur: {})'.format(self.SC, self.GS, self.tStart, self.tDur)


class Schedule:
    def __init__(self, events=None):
        if events is None:
            self.events = []
        else:
            self.events = events

    def __len__(self):
        return len(self.events)

    def addSolutionPair(self, event):
        self.events.append(event)

    def __iter__(self):
        return iter(self.events)


class ProblemInstance:
    def __init__(self, nDays, nSC, nGS, timewindows, requirements):
        self.nDays = nDays
        self.nSC = nSC
        self.nGS = nGS
        self.timewindows = timewindows
        self.requirements = requirements

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '(nDays: {}, nSC: {}, nGS: {}, timewindows: {}, requirements: {})'.format(self.nDays, self.nSC, self.nGS,
                                                                                         len(self.timewindows),
                                                                                         len(self.requirements))
