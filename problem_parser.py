from xml.dom import minidom
from problem import Timewindow, Requirement, ProblemInstance


class XMLProblemParser:
    def __init__(self, filename):
        """
        Parser that receives a path to one of the problems in XML format builds a problem from it.
        :param filename: problem path and filename
        """
        self.filename = filename
        doc = minidom.parse(filename)
        items = doc.getElementsByTagName('basic')
        self.nGS = int(items[0].attributes['nGS'].value)
        self.nSC = int(items[0].attributes['nSC'].value)
        self.nDays = int(items[0].attributes['nDays'].value)
        self.timewindows = []
        timewindowxml = doc.getElementsByTagName('timewindow')
        for tw in timewindowxml:
            GS = int(tw.attributes['GS'].value)
            SC = int(tw.attributes['SC'].value)
            tAos = int(tw.attributes['tAos'].value)
            tLos = int(tw.attributes['tLos'].value)
            self.timewindows.append(Timewindow(GS=GS, SC=SC, tAos=tAos, tLos=tLos))

        self.requirements = []
        requirementsxml = doc.getElementsByTagName('comunication')
        for req in requirementsxml:
            SC = int(req.attributes['SC'].value)
            tBeg = int(req.attributes['tBeg'].value)
            tEnd = int(req.attributes['tEnd'].value)
            tReq = int(req.attributes['tReq'].value)
            self.requirements.append(Requirement(SC=SC, tBeg=tBeg, tEnd=tEnd, tReq=tReq))

    def getProblem(self):
        """
        Returns the proper problem format
        :return: instance of a problem
        """
        return ProblemInstance(nDays=self.nDays,
                               nSC=self.nSC,
                               nGS=self.nGS,
                               timewindows=self.timewindows,
                               requirements=self.requirements)