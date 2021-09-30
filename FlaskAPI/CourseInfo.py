import urllib.request
import re
from bs4 import BeautifulSoup


def getCourse(courseCode, trimesterCode):
    html = urllib.request.urlopen(
        'https://etudier.uqam.ca/cours?sigle='+courseCode).read()
    soup = BeautifulSoup(html, 'html.parser')

    groupsHtml = soup.findAll('div', {"class": "groupe"})

    trimesters = getTrimesters(soup)
    
    groups = []

    for gr in groupsHtml:
        noGroupe = int(re.findall(
            r'\d+', gr.find('h3', {"class": "no_groupe"}).text)[0])
        nomProf = gr.find('li').text

        periods = getPeriods(gr.findAll('td', {"class": "dates"}))

        group = {'noGroupe': noGroupe,
                  'teacher': nomProf,
                  'periods': periods,
                  'trimester': getGroupTrimester(trimesters, gr)}
        if (trimesterCode == group['trimester']):
            groups.append(group)
    
    course = {"courseCode":courseCode, "groups":groups}
    return course

def getCourses(courseCodes, trimester):
    courseCodes = courseCodes.split(',')
    courses = []
    for courseCode in courseCodes:
        courses.append(getCourse(courseCode, trimester))
    return courses

def getPeriods(htmlSoup):
    periods = []

    for periodHtml in htmlSoup:
        elements = periodHtml.parent.findAll('td')
        day = re.findall('[A-Za-z]{1,}', elements[0].text)[0]
        dates = re.findall('[0-9]{1,2} [a-zûé]{3,} [0-9]{4}', elements[1].text)
        
        times = re.findall('[0-9]{2}h[0-9]{2}', elements[2].text)

        type = elements[4].text

        periods.append({'day': day, 'startDate': dates[0], 'endDate': dates[1],
                        'time': times[0]+'-'+times[1], 'type': type})

    return periods


def getTrimesters(soup):
    trimesters = []
    for i in range(0, 3):
        trimesterTxt = soup.find_all(
            "h2", {"data-target": "#horaire"+str(i)})[0]
        season = re.findall("[A-Za-zÉé]{1,}", trimesterTxt.text)[1]
        year = re.findall("[0-9]{4}", trimesterTxt.text)[0]
        trimesters.append({"year": year, "season": season,
                          "lineNb": trimesterTxt.sourceline})

    return trimesters


def getGroupTrimester(trimesters, groupHtml):
    triDict = { "Été": 'E', "Hiver": 'H', "Automne": 'A' }      
    lineNb = groupHtml.sourceline
    for i in range(len(trimesters)-1, -1, -1):
        if (trimesters[i]["lineNb"] < lineNb):
            return triDict[trimesters[i]["season"]] + str(trimesters[i]["year"])[-2:]