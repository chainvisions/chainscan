import pytest
from cs import Chainscanner


def test():
    contract = '0xBcca60bB61934080951369a648Fb03DF4F96263C'
    cs = Chainscanner('eth')
    assert type(cs.get_first_block(contract)) == int
    assert type(cs.get_last_block(contract)) == int
    assert len(cs.get_accounts(contract)) > 0
