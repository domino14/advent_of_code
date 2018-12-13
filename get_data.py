""" Get data from the API """
import os
import requests


ADVENT_SESSION_ID = os.getenv('ADVENT_SESSION_ID')


def get_data(prob, year=2018):
    cache_filename = f'/tmp/adventofcode_{year}_{prob}'
    try:
        with open(cache_filename, 'r') as f:
            print('Reading from cache')
            return str(f.read())
    except FileNotFoundError:
        pass

    print('Making URL request...')
    url = f'https://adventofcode.com/{year}/day/{prob}/input'
    resp = requests.get(url,
                        headers={'Cookie': f'session={ADVENT_SESSION_ID}'})

    with open(cache_filename, 'w') as f:
        f.write(resp.text)

    return resp.text


def get_data_lines(prob, year=2018):
    data = get_data(prob, year)
    lines = data.split('\n')
    return list(filter(lambda ln: ln.strip() != '', lines))


if __name__ == '__main__':
    print(f'Number of bytes: {len(get_data(2))}')
