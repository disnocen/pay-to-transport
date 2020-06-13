# Pay to Transport 

This code is relative to the pay to transport (P2T) protocol.

There is a set of functions in `p2t.py` which is imported in the script `basic-transport.py`.

## Basic Transport

It implements the protocol explained in the paper, without the network layer.

We print the CT1, CT2 and CT3 transaction scripts as they appear in the article. As you can see from the code, the scripts contain the derived public keys of the participants. We preferred to leave the original public key instead of the hash for ease of understanding of the structure of the transaction: in reality it would be more appropriate not to put the public keys in the output script, but the their hashes.

## `p2t.py`

This set of functions provides all the necessary functions to implement the protocol from a cryptographic point of view. In particular there are:

- functions to create derived key pair starting from the order and a private key
- transalation function from days to number of blocks, used for the CHELOCKTIMEVERIFY opcode
