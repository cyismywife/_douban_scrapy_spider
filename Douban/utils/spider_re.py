import re


def production_country_re(response):
    try:
        country = re.search('.*?制片国家/地区:</span>(.*?)<br/>.*?', response).group(1).strip()
        return country
    except AttributeError:
        return 'null'


def language_re(response):
    try:
        return re.search('.*?语言:</span>(.*?)<br/>.*?', response).group(1).strip()
    except AttributeError:
        return 'null'