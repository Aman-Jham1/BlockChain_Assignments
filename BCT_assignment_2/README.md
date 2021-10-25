**Assignment 2**:
Link for the problem statement: https://docs.google.com/document/d/1iIvN0DQxyW5LHFkvt6bePDXxrvfU0_x1NzOQWIyrsFc/edit

Earlier we implemented simple Blockchain in python using an object-oriented paradigm. Now it's time to improve the security by incorporating a consensus algorithm into the blockchain.
We have incorporated the Proof of Elapsed Time (PoET) consensus algorithm in our previously developed blockchain
Multiple nodes are implemented.
Each node is assigned a random time and the node which completes the assigned time first is allowed to mine the current block and
then that node will mine the block, after that again each block is assigned with a new random time.

How to run Dexter's Blockchain

Install dependencies
$ cd BCT_Assignment2
$ pip install -r requirements.txt
Start a blockchain node server,

$ set FLASK_APP=node_server.py
$ flask run --port 8000
One instance of our blockchain node is now up and running at port 8000.

Run the application on a different terminal session,

$ python run_app.py
The application should be up and running at http://localhost:5000.

# port already running at 8000

# Creating up new nodes

$ flask run --port 8001 &
$ flask run --port 8002 &
Use the following cURL requests to register the nodes at port 8001 and 8002 with the already running 8000.

The chain of the nodes can also be inspected by invoking /chain endpoint using cURL.

$ curl -X GET http://localhost:8001/chain
$ curl -X GET http://localhost:8002/chain

Group No. 33:

1. Aman - 2019A7PS0071H
2. Vedang - 2019A7PS0150H
3. Subh - 2019A7PS0100H
