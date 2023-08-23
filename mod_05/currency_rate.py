import asyncio
import json
import platform
import sys
from datetime import date, timedelta

import aiohttp

URL = 'https://api.privatbank.ua/p24api/exchange_rates'

CURRENCY_LIST = ('AUD', 'AZN', 'BYN', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR',
                 'GBP', 'GEL', 'HUF', 'ILS', 'JPY', 'KZT', 'MDL', 'NOK', 'PLN',
                 'SEK', 'SGD', 'TMT', 'TRY', 'UAH', 'USD', 'UZS', 'XAU')


def make_answer(data, currency=[]):
    asked_currency = ['USD', 'EUR']
    if currency:
        asked_currency = tuple(asked_currency + currency)
    sorting = dict()
    for cur in data['exchangeRate']:
        if cur['currency'] in asked_currency:
            if cur.get('saleRate'):
                sorting[cur['currency']] = {
                    'sale': cur['saleRate'],
                    'purchase': cur['purchaseRate']
                }
            else:
                sorting[cur['currency']] = {
                    'sale': 'No sale rate',
                    'purchase': 'No purchase rate'
                }
    return sorting


def get_args(args):
    args.pop(0)
    result = dict()
    if len(args) == 0:
        result['days'] = 1
        return result

    for i in args:
        if i.upper() in CURRENCY_LIST:
            if result.get('currency'):
                result['currency'] += [i.upper()]
            else:
                result['currency'] = [i.upper()]
        elif i.isdigit():
            num = int(i)
            if num > 10:
                result['days'] = 10
                print("Можно вывести не более 10-ти дней")
            elif num < 1:
                result['days'] = 1
            else:
                result['days'] = num
    return result


async def get_currency_rate(days=1, currency_l=[]):
    result_dict = dict()

    today = date.today()
    dates = [(today - timedelta(days=i)).strftime('%d.%m.%Y')
             for i in range(days)]

    async with aiohttp.ClientSession() as session:
        for day in dates:
            params = {'json': '', 'date': day}
            try:
                async with session.get(url=URL, params=params) as response:
                    if response.status == 200:
                        result = await response.json()
                        answer = make_answer(result, currency_l)
                        result_dict.update({day: answer})
                    else:
                        print(f"Error status: {response.status} for {response.url}")
            except aiohttp.ClientConnectorError as err:
                print(f'Connection error: {response.url}', str(err))
    return result_dict


async def main():
    command_args = get_args(sys.argv)
    print(command_args)
    days = command_args['days']
    currency_ext_list = command_args.get('currency')

    return await get_currency_rate(days, currency_ext_list)


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    if r is not None:
        print(json.dumps(r, indent=2))
