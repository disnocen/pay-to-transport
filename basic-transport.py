#! /usr/bin/python3

# this is the implementation of the basic transportation system of P2T It lack
# the network (and reality) layer: we assume all parties live in this script
# only. All the waiting is simulated. All transaction are in 'dry-run' mode: we
# echo the explicit commands but we do not run them
#Days in reality are epressed in seconds here

import json
import hashlib
import p2t

customer_private_key_seed="seed for private key of customer"
merchant_private_key_seed="seed for private key of merchant"
transporter_private_key_seed="seed for private key of transporter"

customer_private_key=p2t.priv_key_from_string(customer_private_key_seed)
merchant_private_key=p2t.priv_key_from_string(merchant_private_key_seed)
transporter_private_key=p2t.priv_key_from_string(transporter_private_key_seed)

customer_public_key=p2t.pubkey_gen(customer_private_key)
merchant_public_key=p2t.pubkey_gen(merchant_private_key)
transporter_public_key=p2t.pubkey_gen(transporter_private_key)

customer_name='C'
merchant_name='M'
transporter_name='T'

delta_merchant_customer=3
delta_customer_merchant=2
epsilon=1
delta_tilde_merchant_cusomer=delta_merchant_customer+delta_customer_merchant+epsilon

order={"item_id":"AA87F","quantity":3,"cost_per_item":0.001}
order=json.dumps(order)
private_label=p2t.priv_key_from_string(order)
public_label=p2t.pubkey_gen(private_label)

customer_derived_address=p2t.bytes_from_point(p2t.point_add(customer_public_key,public_label))
merchant_derived_address=p2t.bytes_from_point(p2t.point_add(merchant_public_key,public_label))
transporter_derived_address=p2t.bytes_from_point(p2t.point_add(transporter_public_key,public_label))

print(order)
print(private_label)
print(public_label.hex())
print(customer_derived_address.hex())
