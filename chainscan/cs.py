import requests
import os
import time
from dotenv import load_dotenv


class Chainscanner:

    def __init__(self, chain):
        load_dotenv()

        self.targetChain = chain

        if chain == 'eth':
            self.apikey = os.getenv('ETHERSCAN_TOKEN')
        elif chain == 'bsc':
            self.apikey = os.getenv('BSCSCAN_TOKEN')
        elif chain == 'polygon':
            self.apikey = os.getenv('POLYGONSCAN_TOKEN')
        elif chain == 'ftm':
            self.apikey = os.getenv('FTMSCAN_TOKEN')
        elif chain == 'heco':
            self.apikey = os.getenv('HECOINFO_TOKEN')
        elif chain == 'optimism':
            self.apikey = os.getenv('OPETHERSCAN_TOKEN')
        elif chain == 'hsc':
            self.apikey = os.getenv('HOOSCAN_TOKEN')
        else:
            raise ValueError('Unsupported chain')

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
        self.targetUrl = ''

        if self.targetChain == 'eth':
            self.targetUrl = 'https://api.etherscan.io'
        elif self.targetChain == 'bsc':
            self.targetUrl = 'https://api.bscscan.com'
        elif self.targetChain == 'polygon':
            self.targetUrl = 'https://api.polygonscan.com'
        elif self.targetChain == 'ftm':
            self.targetUrl = 'https://api.ftmscan.com'
        elif self.targetChain == 'heco':
            self.targetUrl = 'https://api.hecoinfo.com'
        elif self.targetChain == 'optimism':
            self.targetUrl = 'https://api-optimistic.etherscan.io'
        elif self.targetChain == 'hsc':
            self.targetUrl = 'https://api.hooscan.com'
        else:
            raise ValueError('Error with desired chain: ' + self.targetChain)

        url = f'https://{self.targetUrl}/api?module={module}&action={action}&' \
              f'address={address}&startblock={first_block}&endblock={last_block}' \
              f'&sort={sort}&apikey={self.apikey}'
        r = requests.get(url).json()

        assert r['status'] == '1', 'Error when calling API'

        return r['result']
 