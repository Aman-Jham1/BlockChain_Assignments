# This will include our Blockchain assignments throughout the semester.

#Assignment 1:
Link for the problem statement: https://docs.google.com/document/d/1-cIKJF17hL4H00a8stTkdLQxU_CPPgkJ-C2N3jurqXs/edit

We have implemented simple Blockchain in python using object oriented paradigm.

Following functionalities are included:

1.Can retrieve information pertaining to all the available blocks at any point of time.

Each block contains: unique index, transactions, timestamp, previous hash, nonce. 
Nonce = A nonce is an abbreviation for "number only used once," which is a number added to a hashed—or encrypted—block in a blockchain that, when rehashed, meets the difficulty level restrictions.

2.Immutable : Can't edit the added transactions once added to the blockchain.

3.Details of each transaction is readily available.
Transaction: fromAddress, toAddress, amount, timestamp.

4.All the information regarding the completed transactions can be fetched.

When added a new transaction, it goes to unconfirmed transactions pool first then after verifying the new block using Proof of Work (PoW) consensus mechanism, all the unconfirmed transactions are added to this block and then block is added to the blockchain.

Following choices are given: 
1. To print the current blockchain.
2. To add a new transaction.
3. To mine a new block.

Code is well #commented.

Group No. 33:
1. Aman - 2019A7PS0071H
2. Vedang - 2019A7PS0150H
3. Shubh - 2019A7PS0100H
