import os
import asyncio
import aiohttp
import platform
from datetime import datetime
from tabulate import tabulate
from settings import proxy_type, do_report, country

clear_text = 'cls' if platform.system().lower() == 'windows' else 'clear'

info = {}


async def print_data():
    os.system(clear_text)
    headers = ['#', f'Work', '       IP', 'Timeout', 'Country', 'City']
    table = [[k, i['work'], i['ip'], i['timeout'], i['country'], i['city']] for k, i in info.items()]

    final_table = tabulate(table, headers, tablefmt='mixed_outline', colalign=('center', 'center', 'left', 'center', 'center', 'center'))
    print(final_table)


async def set_proxy(proxy_str):
    if '@' in proxy_str:
        if '//' in proxy_str:
            proxy = proxy_str.split('//')[1]
        else:
            proxy = proxy_str
        proxy_address = str(proxy.split('@')[1]).split(':')[0]
    else:
        proxy_things = proxy_str.split(':')
        if len(proxy_things) == 2:
            proxy_address = proxy_things[0]
            proxy_port = proxy_things[1]
            proxy = f'{proxy_address}:{proxy_port}'
        else:
            proxy_login = proxy_things[2]
            proxy_password = proxy_things[3]
            proxy_address = proxy_things[0]
            proxy_port = proxy_things[1]
            proxy = f'{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}'

    proxy_final = f'{proxy_type}://{proxy}'
    return proxy_address, proxy_final


async def read_proxies():
    with open("proxies.txt", "r") as file:
        n = 0
        for row in file.readlines():
            n += 1
            proxy_base = row.strip()
            if proxy_base:
                ip, proxy = await set_proxy(proxy_base)
                info[str(n)] = {
                    'ip': ip,
                    'base_format': proxy_base,
                    'proxy': proxy,
                    'work': '🍋\u200a',
                    'timeout': '░░░░░',
                    'country': '░░',
                    'city': '░░░░░░░░░░'
                }


async def checker(n, data):
    proxies = data['proxy']
    time_start = datetime.now()
    try:
        url = 'http://ip-api.com/json'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=proxies) as response:
                result = await response.json()
                if result['status'] == 'success':
                    info[n]['work'] = '🍏\u200a'
                    info[n]['ip'] = result['query']
                    info[n]['country'] = result['countryCode']
                    info[n]['city'] = result['city']
                else:
                    info[n]['work'] = '🍎\u200a'
    except Exception:
        info[n]['work'] = '🍎\u200a'
    time_end = datetime.now()
    time_res = time_end - time_start
    info[n]['timeout'] = str(round(time_res.total_seconds(), 3))
    await print_data()


async def report():
    good_proxies = []
    bad_proxies = []
    for i, data in info.items():
        if '🍏' in data['work']:
            good_proxies.append(data['base_format'])
        elif '🍎' in data['work']:
            bad_proxies.append(data['base_format'])

    with open('good_proxies.txt', 'w') as file:
        file.write('\n'.join(good_proxies))

    with open('bad_proxies.txt', 'w') as file:
        file.write('\n'.join(bad_proxies))


async def main():
    await read_proxies()
    await print_data()
    await asyncio.gather(*[checker(n, data) for n, data in info.items()])

    if do_report:
        await report()

    if country:
        country_report = []
        for i, data in info.items():
            if data['country'] == country:
                country_report.append(data['base_format'])
        with open('country_report.txt', 'w') as file:
            file.write('\n'.join(country_report))


if __name__ == '__main__':
    asyncio.run(main())
