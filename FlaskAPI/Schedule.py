from re import split
from CourseInfo import getCourses


class TimePeriod:
    day: int
    startTime: int
    endTime: int

    def __init__(self, period):
        timesStr = period["times"].split('h')

        self.startTime = int(timesStr[0].split(
            'h')[0])*60 + int(timesStr[0].split('h')[1])
        self.endTime = int(timesStr[1].split('h')[0]) * \
            60 + int(timesStr[1].split('h')[1])
        self.day = period["day"]

    def overlaps(self, other: object):
        if (self.day != other.day):
            return False
        else:
            return (self.startTime > other.startTime and self.startTime < other.endTime) or (self.endTime > other.startTime and self.endTime < other.endTime)


def getSchedule(courseCodes, trimester):
    courses = getCourses(courseCodes, trimester)
    timePeriods = [] 

    for course in courses:
        print("\n" + course["courseCode"])
        for group in course["groups"]:
            print(toTimes(group["periods"][0]))


def fitsInSchedule(schedule, periods):
    for period in periods:
        for times in schedule:
            if timesOverlap(times, toTimes(period["time"])):
                return False
    return True
