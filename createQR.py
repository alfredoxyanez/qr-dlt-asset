import qrcode
import json
import os
from PIL import Image
from datetime import datetime
import hashlib

from web3.auto import w3
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

#Load parameters
path = os.path.join(os.path.dirname(__file__),'parameters.json' )
with open(path) as f:
    parameters = json.load(f)

# Smart Contract Variables

sc_address = Web3.toChecksumAddress(parameters["CONTRACT_ADDRESS"])
sc_abi = parameters["ABI"]


def make_qr():
    """Makes a QR code for an asset

    Args: None
    Returns:
        QR CODE: This saves and shows a qr code for a particular asset

    """
	#Web 3 Set UP
	w3 = Web3(HTTPProvider(parameters["INFURA_LINK"]))
	w3.middleware_stack.inject(geth_poa_middleware, layer=0)

	# Make default account
	private_key = parameters["PRIVATE_KEY"]
	w3.eth.defaultAccount = w3.eth.account.privateKeyToAccount(private_key)
	print("address: ", w3.eth.defaultAccount.address)


	# Create data for QR Code
	NAME = "Marquez" #NAME FOR MACHINE
	AGENCY = "OICT" #AGENCY THAT MACHINE BELONGS TO
	LOCATION = "NYC HQ2" #LOCATION OF AGENCY


	date_time = str(datetime.utcnow())
	total = NAME +  AGENCY + date_time
	code_id = hashlib.sha256(total.encode('utf-8'))
	hex_dig = code_id.hexdigest()
	id = "0x"+ hex_dig
	print(id)

	#Make QR code
	data = {"id":id, "name":NAME, "agency": AGENCY, "datetime": date_time}
	js  = json.dumps(data)
	img = qrcode.make(js)



	#Make instance of Smart Contract
	asset_contract = w3.eth.contract(
	    address=sc_address,
	    abi=sc_abi
	)

	# Make raw transaction
	nonce = w3.eth.getTransactionCount(w3.eth.defaultAccount.address)
	deploy_txn = asset_contract.functions.createAsset(id, LOCATION).buildTransaction({
	'nonce': nonce,
	'gas': 2000000,
	'gasPrice': 2345678976543,

	})
	#Sign raw Trabsaction
	signed = w3.eth.account.signTransaction(deploy_txn, private_key)

	#Send Raw Transaction
	txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
	w3.eth.waitForTransactionReceipt(txn_hash )

	#Show QR code
	img.show()


if __name__ == "__main__":
	make_qr()
