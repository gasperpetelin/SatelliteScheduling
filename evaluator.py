from collections import defaultdict


def accessWindowObj(problemInstance, schedule):
    # Compute (tAos, tLos) unions for each SC, GS pair (equation 1)
    AW = defaultdict(lambda: [])
    for tw in problemInstance.timewindows:
        AW[(tw.GS, tw.SC)].append((tw.tAos, tw.tLos))
    FitAW = 0
    for sol in schedule:
        for tAos, tLos in AW[(sol.GS, sol.SC)]:
            if tAos <= sol.tStart <= tLos and tAos <= sol.tStart + sol.tDur <= tLos:
                FitAW += 1
    return (FitAW / len(schedule)) * 100


def communicationClashObj(problemInstance, schedule):
    # Split schedule events by the GS they are trying to communicate with.
    GS_communication = defaultdict(lambda: list())
    for x in schedule:
        GS_communication[x.GS].append(x)

    FitCS = 0
    for GS in GS_communication.keys():
        sorted_events = sorted(GS_communication[GS], key=lambda x: x.tStart)
        if len(sorted_events) < 2:
            # Skip checking if 0 or 1 SC are communicating with GS
            continue
        for i in range(len(sorted_events) - 1):
            if sorted_events[i + 1].tStart < sorted_events[i].tStart + sorted_events[i].tDur:
                FitCS -= 1
    return ((len(schedule) + FitCS) / len(schedule)) * 100


def getOverlap(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))


def unions(a):
    b = []
    for begin, end in sorted(a):
        if b and b[-1][1] >= begin - 1:
            b[-1][1] = max(b[-1][1], end)
        else:
            b.append([begin, end])
    return b


def communicationTimeRequirementObj(problemInstance, schedule):
    requirements_grouped = defaultdict(lambda: list())
    for x in problemInstance.requirements:
        requirements_grouped[x.SC].append(x)

    schedule_grouped = defaultdict(lambda: list())
    for x in schedule:
        schedule_grouped[x.SC].append(x)

    FitTR = 0
    for SC, SC_requirements in requirements_grouped.items():
        SC_schedule = schedule_grouped[SC]
        for req in SC_requirements:
            total_overlap = 0
            for sch in SC_schedule:
                overlap = getOverlap([req.tBeg, req.tEnd], [sch.tStart, sch.tStart + sch.tDur])
                total_overlap += overlap

            if total_overlap >= req.tReq:
                FitTR += 1

    return (FitTR / len(problemInstance.requirements)) * 100


def daysToMinutes(days):
    return days * 24 * 60


def groundStationUsageObj(problemInstance, schedule):
    days_to_minutes = daysToMinutes(problemInstance.nDays)
    schedule_grouped = defaultdict(lambda: list())
    for x in schedule:
        schedule_grouped[x.GS].append(x)

    total_time = 0
    for GS, events in schedule_grouped.items():
        events_times = [(x.tStart, min(days_to_minutes, x.tStart + x.tDur)) for x in events]
        union_times = unions(events_times)
        for start, end in union_times:
            total_time += end - start
    f = (total_time / (days_to_minutes * problemInstance.nGS)) * 100
    return f


class ScheduleEvaluator:
    """
    Evaluator that receives the problem instance and schedule and return objectives
    """
    @staticmethod
    def evaluate(problemInstance, schedule):
        FitAW = accessWindowObj(problemInstance, schedule)
        FitCS = communicationClashObj(problemInstance, schedule)
        FitTR = communicationTimeRequirementObj(problemInstance, schedule)
        FitGU = groundStationUsageObj(problemInstance, schedule)
        return FitAW, FitCS, FitTR, FitGU
