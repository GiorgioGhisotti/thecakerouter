# TheCakeRouter

Simple implementation of a TOR-like anonimization system in Python. Work in progress.

# How it works

A node server keeps track of all available proxy nodes. When a node is started, it registers itself with the node server. Clients can obtain the list of nodes from the node server.

Once a client has the list, it can randomly choose a route for its traffic with an arbitrary number of nodes (assuming they are available; 3-5 nodes is a reasonable amount). The client then sends a "cake" to the first node; the "cake" is encrypted with the node's public key and contains the node's forward and backward symmetric keys as well as the address of the next node (or server) in the route.

The client sends one "cake" to every node, sending them through the route and receiving confirmation from each node (once a node has received its "cake", it sends back confirmation and treats every new message as a normal packet).

Nodes then forward every message they receive to the next node in the line and wait for an answer; the message is decrypted with each node's symmetric *forwards* key and the answer is encrypted with each node's symmetric *backwards* key.

The nodes don't know where they are inside the route and they can only remove a single layer of encryption from any given message. The node server knows which clients requested a list, but it can't determine what their destination is or which route they will take.
