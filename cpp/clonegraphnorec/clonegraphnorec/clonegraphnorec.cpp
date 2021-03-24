// clonegraphnorec.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <vector>
#include <map>
#include <queue>

//#define DEBUG1 1
#define DEBUG2

using namespace std;

struct GraphNode
{
    string label;
    int value;
    //A neighbour vector which contains addresses to 
    //all the neighbours of a GraphNode 
    vector<GraphNode*> neighbours;
};

// Build a disconnected node
GraphNode* buildSolo(const string& label, const int& value)
{
    GraphNode* singleNode = new GraphNode();
    singleNode->value = value;
    singleNode->label = label;
    return singleNode;
}

//Check whether a node belongs to a vector
// Returns true if it does, false otherwise
bool nodeMatched(GraphNode* node, vector<GraphNode*>nodes)
{
    /**
        for (std::vector<GraphNode*>::iterator it = nodes.begin();it!=nodes.end();it++)
            if (it == node)
                return true;
    */
    for (auto it : nodes) {
        if (it == node)
            return true;
    }
    return false;
}


//Connect node1 to node2
void connectTo(GraphNode* node1, GraphNode* node2)
{
    if (nodeMatched(node2, node1->neighbours))
        return;
    node1->neighbours.push_back(node2);
}


GraphNode* buildExample(const int& sample)
{
    GraphNode* node1 = buildSolo("node1", 1);
    if (sample == 1) {
        GraphNode* node2 = buildSolo("node2", 2);
        GraphNode* node3 = buildSolo("node3", 3);
        connectTo(node1, node2);
        connectTo(node1, node3);
        connectTo(node3, node1);
    }
    else if (sample == 2) {
 //       [[2, 4], [1, 3], [2, 4], [1, 3]]
        GraphNode* node2 = buildSolo("node2", 2);
        GraphNode* node3 = buildSolo("node3", 3);
        GraphNode* node4 = buildSolo("node4", 4);
        connectTo(node1, node2);
        connectTo(node1, node4);
        connectTo(node2, node1);
        connectTo(node2, node3);
        connectTo(node3, node2);
        connectTo(node3, node4);
        connectTo(node4, node1);
        connectTo(node4, node3);
    }
    return node1;
}

void printoutNode(GraphNode* node)
{
    std::cout << "*** Node " << node->label << " Value: " << node->value << std::endl;
    if (node->neighbours.empty()) {
        cout << "No neighbours ***" << std::endl;
        return;
    }
    std::cout << " Neighbours are :\n";
    for (auto it : node->neighbours) {
        std::cout << it->label << " with value " << it->value << std::endl;
    }
    std::cout << "***" << endl;
}


void printoutGraph(GraphNode* node)
{
    if (node == NULL)
        std::cout << "Empty graph \n";
    std::cout << "Printing graph for " << node->label << std::endl;
    std::vector<GraphNode*> cached;
    std::queue<GraphNode*> pending;
    pending.push(node);
    while (!pending.empty()) {
        GraphNode* current = pending.front();
        pending.pop();
        cached.push_back(current);
        printoutNode(current);
        for (auto it : current->neighbours) {
            if (!nodeMatched(it, cached))
                pending.push(it);
        }
#if defined DEBUG1
        std::cout << "Cache size is " << cached.size() << std::endl;
#endif
#if defined DEBUG1
        std::cout << "Address stored in cache " << static_cast<void*>(it) << std::endl;
#endif
    }
}

GraphNode* cloneGraph(GraphNode* node)
{
    if (node == NULL)
        return NULL;
    std::map<GraphNode*, GraphNode*> cachedAddress;
    std::queue<GraphNode*> pending;
    GraphNode* newNode = buildSolo(node->label, node->value);
    pending.push(node);
    cachedAddress[node] = newNode;
    while (!pending.empty()) {
#if defined DEBUG2
        std::cout << "Cache size is " << cachedAddress.size() << std::endl;
#endif
        GraphNode* current = pending.front();
        GraphNode* newNode = cachedAddress[current];
        pending.pop();
#if defined DEBUG2
        std::cout << "Addresses stored in cache " << static_cast<void*>(current) << " " << static_cast<void*>(newNode) << std::endl;
#endif
        for (auto it : current->neighbours) {
#if defined DEBUG2
            std::cout << "Checking if " << static_cast<void*>(it) << " was in cache" << std::endl;
            if (cachedAddress.find(it) == cachedAddress.end())
                std::cout << "Not found in cache " << std::endl;
            else
                std::cout << "Found in cache\n";
#endif
            if (cachedAddress.find(it) == cachedAddress.end()) {
                GraphNode* newNeighbour = buildSolo(it->label, it->value);
                cachedAddress[it] = newNeighbour;
                pending.push(it);
            }
            connectTo(newNode, cachedAddress[it]);
#if defined  DEBUG2
            std::cout << "Connected " << newNode->label << " to " << cachedAddress[it]->label << std::endl;
#endif
        }
    }
    return newNode;
}



int main()
{
    cout << "Print graph\n";
//    GraphNode* myGraph = buildExample(1);
    GraphNode* myGraph = buildExample(0);
    printoutGraph(myGraph);
    cout << "Cloned graph " << endl;
    GraphNode* newGraph = cloneGraph(myGraph);
    printoutGraph(newGraph);
}

