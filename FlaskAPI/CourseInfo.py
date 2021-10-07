import urllib.request
import re
from bs4 import BeautifulSoup


def getCourse(courseCode, trimesterCode):
    courseCode = courseCode.upper()
    trimesterCode = trimesterCode.upper()
    html = urllib.request.urlopen(
        'https://etudier.uqam.ca/cours?sigle='+courseCode).read()
    soup = BeautifulSoup(html, 'html.parser')

    title = str(soup.find("title")).split("|")[1].strip()

    courseInfo = soup.findAll("div", {"class": "rubrique"})

    objectiveTitles = ["Objectifs"]
    descriptionTitles = ["Sommaire du contenu", "Description"]
    modalitiesTitles = ["Modalité d'enseignement"]
    prerequisitesTitles = ["Préalables académiques"]
    objective, description, modalities, prerequisites = "", "", "", []
    for i in range(len(courseInfo)):
        if courseInfo[i].find('h2').text in objectiveTitles:
            objective = courseInfo[i].find('p').text
        elif courseInfo[i].find('h2').text in descriptionTitles:
            description = courseInfo[i].find('p').text
        elif courseInfo[i].find('h2').text in modalitiesTitles:
            modalities = courseInfo[i].find('p').text
        elif courseInfo[i].find('h2').text in prerequisitesTitles:
            if (courseInfo[i].find('p').find('ul')):
                prerequisites = re.findall(r'[A-Z]{3}[0-9]{4}', courseInfo[i].find('p').find('ul').text)
            else:
                prerequisites = re.findall(r'[A-Z]{3}[0-9]{4}', courseInfo[i].text)

    relatedProgramsSoup = soup.find(
        'div', {"class": "related-programs"}).findAll('a', href=True)
    relatedPrograms = []
    for rP in relatedProgramsSoup:
        relatedPrograms.append(int(rP['href'][-4:]))

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
                 'trimester': getGroupTrimester(trimesters, gr)
                 }
        if (trimesterCode == group['trimester']):
            groups.append(group)

    course = {"courseCode": courseCode, "title": title, "objective": objective,
              "description": description, "modalities": modalities, "prerequisites": prerequisites,
              "relatedPrograms": relatedPrograms, "groups": groups}
    return course


def getCourses(courseCodes, trimester):
    courseCodes = courseCodes.split(',')
    courses = []
    for courseCode in courseCodes:
        courses.append(getCourse(courseCode, trimester))
    return courses


def getPeriods(htmlSoup):
    datesDict = {"janvier": "01", "février": "02", "mars": "03", "avril": "04",
                 "mai": "05", "juin": "06", "juillet": "07", "août": "08",
                 "septembre": "09", "octobre": "10", "novembre": "11", "décembre": "12"}
    daysDict = {"Lundi": 0, "Mardi": 1, "Mercredi": 2,
                "Jeudi": 3, "Vendredi": 4, "Samedi": 5, "Dimanche": 6}
    periods = []

    for periodHtml in htmlSoup:
        elements = periodHtml.parent.findAll('td')
        day = re.findall('[A-Za-z]{1,}', elements[0].text)[0]
        dates = re.findall('[0-9]{1,2} [a-zûé]{3,} [0-9]{4}', elements[1].text)
        for i in range(2):
            dates[i] = dates[i].split(' ')
            dates[i][1] = datesDict[dates[i][1]]
            dates[i] = '/'.join(dates[i])

        times = re.findall('[0-9]{2}h[0-9]{2}', elements[2].text)

        type = elements[4].text

        period = {'day': daysDict[day], 'date': dates[0]+'-'+dates[1],
                  'time': times[0]+'-'+times[1], 'type': type}
        if (len(periods) == 0 or periods[-1] != period):
            periods.append(period)

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
    triDict = {"Été": 'E', "Hiver": 'H', "Automne": 'A'}
    lineNb = groupHtml.sourceline
    for i in range(len(trimesters)-1, -1, -1):
        if (trimesters[i]["lineNb"] < lineNb):
            return triDict[trimesters[i]["season"]] + str(trimesters[i]["year"])[-2:]