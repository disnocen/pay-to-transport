#! /usr/bin/python3

# this is the implementation of the basic transportation system of P2T It lack
# the network (and reality) layer: we assume all parties live in this script
# only. All the waiting is simulated. All transaction are in 'dry-run' mode: we
# echo the explicit commands but we do not run them
# Days in reality are epressed in seconds here

import json
import p2t

customer_secr_key_seed="seed for secret key of customer"
merchant_secr_key_seed="seed for secret key of merchant"
transporter_secr_key_seed="seed for secret key of transporter"

customer_secr_key=p2t.secr_key_from_string(customer_secr_key_seed)
merchant_secr_key=p2t.secr_key_from_string(merchant_secr_key_seed)
transporter_secr_key=p2t.secr_key_from_string(transporter_secr_key_seed)

# transporter creates the secret
transporter_secret_hash_lock="this is a s3cr3t" 
transporter_hashed_hash_lock=p2t.create_hash_from_string(transporter_secret_hash_lock)

customer_public_key=p2t.pubkey_gen(customer_secr_key)
merchant_public_key=p2t.pubkey_gen(merchant_secr_key)
transporter_public_key=p2t.pubkey_gen(transporter_secr_key)

customer_name='C'
merchant_name='M'
transporter_name='T'

delta_merchant_transporter=3
delta_transporter_merchant=2
epsilon=1
delta_tilde_merchant_transporter=delta_merchant_transporter+delta_transporter_merchant+epsilon

order={"item_id":"AA87F","quantity":3,"cost_per_item":0.001}
order=json.dumps(order)
secr_label=p2t.secr_key_from_string(order)
public_label=p2t.pubkey_gen(secr_label)

customer_derived_pubkey=p2t.bytes_from_point(p2t.point_add(customer_public_key,public_label))
merchant_derived_pubkey=p2t.bytes_from_point(p2t.point_add(merchant_public_key,public_label))
transporter_derived_pubkey=p2t.bytes_from_point(p2t.point_add(transporter_public_key,public_label))

print("The order is:" ,order)

print(transporter_name, "generates secret" )
print("the hashed secret of", transporter_name, "is:"  , transporter_hashed_hash_lock)
print(transporter_name, "sends hash of secret to", customer_name )
print()
print(customer_name,"pays" ,merchant_name,"transportation costs (P2PKH transaction)")
print()

print("CT1:", customer_name, "sends conditional transaction with output script:")
print( "IF t1+", p2t.days_to_blocks(delta_tilde_merchant_transporter), "CHECKLOCKTIMEVERIFY DROP", transporter_hashed_hash_lock, "CHECKEQUALVERIFY 2", customer_derived_pubkey.hex(),transporter_derived_pubkey.hex(),"2 CHECKMULTISIG ELSE", customer_derived_pubkey.hex(), "CHECKSIG" )
print()
print("CT2:", transporter_name, "sends conditional transaction with output script:")
print( "IF t1+", p2t.days_to_blocks(delta_merchant_transporter), "CHECKLOCKTIMEVERIFY DROP 2", merchant_derived_pubkey.hex(),transporter_derived_pubkey.hex(),"2 CHECKMULTISIG ELSE", transporter_derived_pubkey.hex(), "CHECKSIG" )
print()
print("CT3:", transporter_name, "and" , merchant_name, "send conditional transaction with output script:")
print( "IF t1+", p2t.days_to_blocks(delta_tilde_merchant_transporter+delta_transporter_merchant), "CHECKLOCKTIMEVERIFY DROP 2", merchant_derived_pubkey.hex(),transporter_derived_pubkey.hex(),"2 CHECKMULTISIG ELSE",transporter_hashed_hash_lock,"CHECKEQUALVERIFY" , customer_derived_pubkey.hex(), "CHECKSIG" )
print()
