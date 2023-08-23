import requests
import re
import time
import pandas as pd
import datetime


class ChainEdgeAPI:
    def convert_to_datetime(self, row):
        # Check if the row is already in datetime format
        try:
            pd.Timestamp(row)
            return row  # if it's already in datetime format, return as is
        except:
            pass

        # Extract hours and minutes from the string
        hours = 0
        minutes = 0
        if 'hrs' in row:
            hours = int(row.split(' hrs')[0])
        if 'mins' in row:
            minutes = int(row.split(' mins')[0].split(' ')[-1])

        # Compute the datetime
        now = datetime.datetime.now()
        exact_time = now - datetime.timedelta(hours=hours, minutes=minutes)

        return exact_time.strftime('%Y-%m-%d %H:%M:%S')

    def convert_with_subscript(self, value: str) -> str:
        # Mapping of subscript characters to their integer values
        subscript_map = {
            '₀': 0, '₁': 1, '₂': 2, '₃': 3, '₄': 4,
            '₅': 5, '₆': 6, '₇': 7, '₈': 8, '₉': 9,
            '₁₀': 10, '₁₁': 11, '₁₂': 12, '₁₃': 13, '₁₄': 14,
            '₁₅': 15, '₁₆': 16, '₁₇': 17, '₁₈': 18, '₁₉': 19, '₂₀': 20
        }

        decimal_index = value.find('.')

        # Extract the number and the subscript
        number = value[decimal_index+1:]
        for sub in subscript_map.keys():
            if number.startswith(sub):
                subscript = subscript_map[sub]
                number = number[len(sub):]
                break
        else:
            # If no subscript is found, return the original number
            value = value.replace('$', '').replace(',', '')
            return value

        # Generate the result with leading zeros
        result = '0.' + '0' * subscript + number
        return result

    def extract_text_from_html(self, html_string):
        # Remove all content between < and >
        return re.sub(r'<[^>]+>', '', html_string).strip()

    # Each page has 40 results.
    def get_single_page(self, page=1):
        cookies = {
            '_ga': 'GA1.1.998904606.1692345881',
            '_ga_D6FYDK42KW': 'GS1.1.1692345881.1.1.1692345931.0.0.0',
            'csrftoken': 'EcntbsJKe5xh0EPQtgAh8Wv8pHitEBCb0cz4DmHRZLx5lfxa1688iI8yXoTibaHe',
            'sessionid': '56ktj8xo4zdnn9p31z611irt4vdyzoc8',
        }

        headers = {
            'authority': 'app.chainedge.io',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            # 'cookie': '_ga=GA1.1.998904606.1692345881; _ga_D6FYDK42KW=GS1.1.1692345881.1.1.1692345931.0.0.0; csrftoken=EcntbsJKe5xh0EPQtgAh8Wv8pHitEBCb0cz4DmHRZLx5lfxa1688iI8yXoTibaHe; sessionid=56ktj8xo4zdnn9p31z611irt4vdyzoc8',
            'referer': 'https://app.chainedge.io/alpha_stream/',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {
            'draw': f'{page}',
            'columns[0][data]': 'Address',
            'columns[0][name]': '',
            'columns[0][searchable]': 'true',
            'columns[0][orderable]': 'true',
            'columns[0][search][value]': '',
            'columns[0][search][regex]': 'false',
            'columns[1][data]': 'buy_token',
            'columns[1][name]': '',
            'columns[1][searchable]': 'true',
            'columns[1][orderable]': 'true',
            'columns[1][search][value]': '',
            'columns[1][search][regex]': 'false',
            'columns[2][data]': 'buy_price',
            'columns[2][name]': '',
            'columns[2][searchable]': 'true',
            'columns[2][orderable]': 'true',
            'columns[2][search][value]': '',
            'columns[2][search][regex]': 'false',
            'columns[3][data]': 'sell_token',
            'columns[3][name]': '',
            'columns[3][searchable]': 'true',
            'columns[3][orderable]': 'true',
            'columns[3][search][value]': '',
            'columns[3][search][regex]': 'false',
            'columns[4][data]': 'sell_price',
            'columns[4][name]': '',
            'columns[4][searchable]': 'true',
            'columns[4][orderable]': 'true',
            'columns[4][search][value]': '',
            'columns[4][search][regex]': 'false',
            'columns[5][data]': 'sell_value',
            'columns[5][name]': '',
            'columns[5][searchable]': 'true',
            'columns[5][orderable]': 'true',
            'columns[5][search][value]': '',
            'columns[5][search][regex]': 'false',
            'columns[6][data]': 'chain',
            'columns[6][name]': '',
            'columns[6][searchable]': 'true',
            'columns[6][orderable]': 'true',
            'columns[6][search][value]': '',
            'columns[6][search][regex]': 'false',
            'columns[7][data]': 'id',
            'columns[7][name]': '',
            'columns[7][searchable]': 'true',
            'columns[7][orderable]': 'true',
            'columns[7][search][value]': '',
            'columns[7][search][regex]': 'false',
            'columns[8][data]': 'tn_time',
            'columns[8][name]': '',
            'columns[8][searchable]': 'true',
            'columns[8][orderable]': 'true',
            'columns[8][search][value]': '',
            'columns[8][search][regex]': 'false',
            'order[0][column]': '0',
            'order[0][dir]': 'asc',
            'start': f'{(page-1)*40}',
            'length': '40',
            'search[value]': '',
            'search[regex]': 'false',
            '_': '1692785159473',
        }

        while True:
            response = requests.get('https://app.chainedge.io/alphastreamjson/',
                                    params=params, cookies=cookies, headers=headers)
            status_code = response.status_code

            time.sleep(2)
            if status_code == 200:
                print(f'successfully pulled page {page}')
                break

            print('failed to fetch. retrying...')

        data = response.json()

        df = pd.DataFrame.from_dict(data['data'])

        cols_to_remove_html = ['Address', 'sell_value',
                               'buy_token', 'buy_price', 'sell_token', 'sell_price']

        for col in cols_to_remove_html:
            df[col] = df[col].apply(self.extract_text_from_html)

            if col == 'buy_price' or col == 'sell_price':
                df[col] = df[col].apply(self.convert_with_subscript)

        # Apply the conversion function
        df['tn_time'] = df['tn_time'].apply(self.convert_to_datetime)

        return df

    def get_many_pages(self, pages):

        df = pd.DataFrame()

        for page in range(1, pages+1):
            print(f'pulling page {page}...')
            data = self.get_single_page(page)
            df = pd.concat([df, data], axis=0)

        # drop the mismatched indices
        return df
