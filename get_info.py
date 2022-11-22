import requests
from bs4 import BeautifulSoup
import re



class Notam:
    def __init__(self, affectedaerodrome, effectivestart, effectiveend, schedule, text):
        self.affectedaerodrome = affectedaerodrome
        self.effectivestart = effectivestart
        self.effectiveend = effectiveend
        self.schedule = schedule
        self.text = text


def get_notam():
    notam_url = 'https://api.laminardata.aero/v2/aerodromes/RJFU/notams'
    params = {'user_key': '89b19ff537150988ed28cb02e05663a8'}

    res = requests.get(notam_url, params=params)
    data = res.json()

    notam_classes = []
    for d in data['features']:
        try:
            scedule = d['properties']['schedule']
        except:
            scedule = 'no data'

        notam = Notam(
            affectedaerodrome=d['properties']['affectedAerodrome'],
            effectivestart=d['properties']['effectiveStart'],
            effectiveend=d['properties']['effectiveEnd'],
            schedule=scedule,
            text=d['properties']['text']
        )
        notam_classes.append(notam)

    return notam_classes


def get_metar_taf():
    metar_url = 'http://www.imocwx.com/i/metar.php?Area=8&Port=RJFU'
    taf_url = 'http://www.imocwx.com/i/taf.php?Area=3&Port=RJFU'
    m_html_text = requests.get(metar_url).text
    m_soup = BeautifulSoup(m_html_text, 'html.parser')
    t_html_text = requests.get(taf_url).text
    t_soup = BeautifulSoup(t_html_text, 'html.parser')

    m_text = m_soup.getText()
    metar = re.findall(r'.*METAR\s[\s\S]*=', m_text)

    t_text = t_soup.getText()
    taf = re.findall(r'.*TAF\s[\s\S]*=', t_text)
    metar_taf = {'METAR': ''.join(metar), 'TAF': ''.join(taf)}

    return metar_taf




# notam_url = 'https://www.notams.faa.gov/dinsQueryWeb/queryRetrievalMapAction.do#RJFU'
# n_html_text = requests.get(notam_url).text
# n_soup = BeautifulSoup(n_html_text, 'html.parser')

# trs = n_soup.find_all('pre')
#
# print(n_soup)