from pycoin.serialize import b2h, h2b
import rlp
from ethereum import utils, transactions
import requests
import json
import time
from ethereum.abi import ContractTranslator
import getopt, sys

def make_transaction(src_priv_key, dst_address, value, data):
    src_address = b2h(utils.privtoaddr(src_priv_key))
    nonce = get_num_transactions(src_address)
    gas_price = get_gas_price_in_wei()
    data_as_string = b2h(data)
    start_gas = eval_startgas(src_address, dst_address, value, data_as_string, gas_price)

    nonce = int(nonce, 16)
    gas_price = int(gas_price, 16)
    start_gas = int(start_gas, 16) + 100000

    tx = transactions.Transaction(nonce,
                                  gas_price,
                                  start_gas,
                                  dst_address,
                                  value,
                                  data).sign(src_priv_key)

    tx_hex = b2h(rlp.encode(tx))
    tx_hash = b2h(tx.hash)
    if use_ether_scan:
        params = [{"hex": "0x" + tx_hex}]
    else:
        params = ["0x" + tx_hex]
    return_value = json_call("eth_sendRawTransaction", params)
    if return_value == "0x0000000000000000000000000000000000000000000000000000000000000000":
        print
        "Transaction failed"
        return False
    wait_for_confirmation(tx_hash)
    return return_value