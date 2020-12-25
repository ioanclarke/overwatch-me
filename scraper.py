import requests
from bs4 import BeautifulSoup as bs

HARRY = 'SwankyTiger-211960'
ME = 'LetsGo-21230'


def get_player_url():
    region = input('Region: ')
    platform = input('Platform: ')
    name = input('Name: ')
    if region == '':
        region = 'en-us'
    if platform == '':
        platform = 'pc'
    if name == '':
        name = ME
    url = f'https://playoverwatch.com/{region}/career/{platform}/{name}/'
    return url


def fetch_content(url):
    print()
    print(f'Searching...')
    print()
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')
    return soup


def fetch_player_stats(soup):
    # level = soup.find('div', class_='player-level')
    # level_image_url = level['style'][22:-2]
    # rank = level.find('div', class_='player-rank')
    # rank_image_url = rank['style'][22:-2]

    comp_rank_titles = soup.findAll('div', class_='competitive-rank-tier')
    comp_rank_levels = soup.findAll('div', class_='competitive-rank-level')
    comp_ranks = []
    for role, sr in zip(comp_rank_titles, comp_rank_levels):
        comp_ranks.append((role['data-ow-tooltip-text'][:role['data-ow-tooltip-text'].find('Skill')-1], sr.text))

    comp = soup.findAll('div', {'data-category-id': '0x0860000000000021'})
    hero_name_data = comp[1].findAll('div', class_='ProgressBar-title')
    hero_time_data = comp[1].findAll('div', class_='ProgressBar-description')
    hero_names = []
    hero_times = []
    for name, time in zip(hero_name_data[:5], hero_time_data[:5]):
        hero_names.append(name.text)
        hero_times.append(time.text)
    return set(comp_ranks), hero_names, hero_times  # comp_ranks is turned into a set because it contains duplicates
    # for some reason


def display_stats(comp_ranks, hero_names, hero_times):
    print('SR')
    print('---------------------------')
    for role in comp_ranks:
        print('{0:10} {1}'.format(role[0], role[1]))
    print()
    print()
    print('Top 5 competitive heroes:')
    print('---------------------------')
    for name, time in zip(hero_names, hero_times):
        print('{0:10} {1}'.format(name, time))


if __name__ == '__main__':
    url = get_player_url()
    page_content = fetch_content(url)
    comp_ranks, hero_names, hero_times = fetch_player_stats(page_content)
    display_stats(comp_ranks, hero_names, hero_times)
