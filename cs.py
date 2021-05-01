import requests
import os
import time
from dotenv import load_dotenv


class Chainscanner:

    def __init__(self, chain):
        load_dotenv()

        if chain == 'eth':
            self.apikey = os.getenv('ETHERSCAN_TOKEN')
        elif chain == 'bsc':
            self.apikey = os.getenv('BSCSCAN_TOKEN')
        else:
            raise ValueError('chain must be either eth or bsc')

    def get_first_block(self, contract):
        return self._get_block(contract, 'asc')

    def get_last_block(self, contract):
        return self._get_block(contract, 'desc')

    def get_accounts(self, contract):

        first = self.get_first_block(contract)
        last = self.get_last_block(contract)
        block = first
        s = set()

        while block != last:
            time.sleep(0.5)
            module = 'account'
            action = 'txlist'
            address = contract
            starblock = block
            endblock = 99999999
            sort = 'asc'

            result = self._call_api(module, action, address, starblock, endblock, sort)

            for res in result:
                block = int(res['blockNumber'])
                if block == last:
                    return s
                else:
                    if res['to'].lower() == contract.lower():
                        s.add(res['from'])

        return s

    def _get_block(self, contract, sort):

        module = 'account'
        action = 'txlist'
        address = contract
        first_block = 1
        last_block = 99999999

        result = self._call_api(module, action, address, first_block, last_block, sort)

        return int(result[0]['blockNumber'])

    def _call_api(self, module, action, address, first_block, last_block, sort):

        url = f'https://api.etherscan.io/api?module={module}&action={action}&' \
              f'address={address}&startblock={first_block}&endblock={last_block}' \
              f'&sort={sort}&apikey={self.apikey}'
        r = requests.get(url).json()

        assert r['status'] == '1', 'error when calling etherscan api'

        return r['result']
