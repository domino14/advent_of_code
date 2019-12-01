""" Get data from the API """
import re
import os
import requests


ADVENT_SESSION_ID = os.getenv('ADVENT_SESSION_ID')


def get_data(prob, year=2019):
    cache_filename = '/tmp/adventofcode_{year}_{prob}'.format(year=year, 
                                                              prob=prob)
    try:
        with open(cache_filename, 'r') as f:
            print('Reading from cache')
            return str(f.read())
    except FileNotFoundError:
        pass

    print('Making URL request...')
    url = 'https://adventofcode.com/{year}/day/{prob}/input'.format(year=year,
                                                                    prob=prob)
    print('url is', url)
    resp = requests.get(url,
                        headers={'Cookie': 'session={ADVENT_SESSION_ID}'.format(ADVENT_SESSION_ID=ADVENT_SESSION_ID)})

    with open(cache_filename, 'w') as f:
        f.write(resp.text)

    return resp.text


def get_data_lines(prob, year=2019):
    data = get_data(prob, year)
    lines = data.split('\n')
    return list(filter(lambda ln: ln.strip() != '', lines))


def find_numbers(string, ints=True):
    numexp = re.compile(r'[-]?\d[\d,]*[\.]?[\d{2}]*')
    numbers = numexp.findall(string)
    numbers = [x.replace(',', '') for x in numbers]
    if ints is True:
        return [int(x.replace(',', '').split('.')[0]) for x in numbers]
    else:
        return numbers


if __name__ == '__main__':
    print('Number of bytes: ' + str(len(get_data(2))))
