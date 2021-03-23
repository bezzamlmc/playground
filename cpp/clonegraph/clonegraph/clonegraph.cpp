// clonegraph.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <vector>
#include <map>

//#define DEBUG1 1

using namespace std;

struct GraphNode
{
    string label;
    int value;
    //A neighbour vector which contains addresses to 
    //all the neighbours of a GraphNode 
    vector<GraphNode*> neighbours;
};

// Vuild a disconnected node
GraphNode* buildSolo(const string& label,const int& value)
{
    GraphNode* singleNode = new GraphNode();
    singleNode->value = value;
    singleNode->label = label;
    return singleNode;
}

//Check whether a node belongs to a list
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
void connectTo(GraphNode *node1, GraphNode *node2)
{
    if (nodeMatched(node2,node1->neighbours))
        return;
    node1->neighbours.push_back(node2);
}


GraphNode* buildExample(const int& sample)
{
//    if (sample == 1) {
    GraphNode *node0 = buildSolo("node0", 0);
    GraphNode* node1 = buildSolo("node1", 1);
    GraphNode* node2 = buildSolo("node2", 2);
    connectTo(node0, node1);
    connectTo(node0, node2);
    connectTo(node2, node0);
    return node0;

//    }
}

std::map<GraphNode*, int> cached;
std::map<GraphNode*, GraphNode*> cachedAddress;

void printoutGraph(GraphNode* node)
{
#if defined DEBUG1
    std::cout << "Cache size is " << cached.size() << std::endl;
#endif
    cached[node] = 0;
#if defined DEBUG1
    std::cout << "Address stored in cache " << static_cast<void*>(node) << std::endl;
#endif
    std::cout << "Printing graph for " << node->label << std::endl;
    std::cout << "Value: " << node->value << std::endl;
    if (node->neighbours.empty()) {
        cout << "No neighbours " << std::endl;
        return;
    }
    std::cout << " Neighbours are :";
    for (auto it : node->neighbours) {
        std::cout << it->label << " with value " << it->value << std::endl;
    }
    for (auto it : node->neighbours) {
#if DEBUG1
        std::cout << "Checking if " << static_cast<void*>(node) << " was in cache" << std::endl;
        if (cached.find(it) == cached.end())
            std::cout << "Not found in cache " << std::endl;
        else
            std::cout << "Found in cache";
#endif
        if (cached.find(it) == cached.end())
            printoutGraph(it);
        else
            cached[it] += 1;
    }
}

GraphNode* cloneGraph(GraphNode* node)
{
#if defined DEBUG2
    std::cout << "Cache size is " << cachedAddress.size() << std::endl;
#endif
    GraphNode* newNode = buildSolo(node->label, node->value);
    cachedAddress[node] = newNode;
#if defined DEBUG2
    std::cout << "Addresses stored in cache " << static_cast<void*>(node) << " " << static_cast<void*>(newNode) << std::endl;
#endif
    if (node->neighbours.empty()) {
        return newNode;
    }
    for (auto it : node->neighbours) {
#if defined DEBUG2
        std::cout << "Checking if " << static_cast<void*>(it) << " was in cache" << std::endl;
        if (cachedAddress.find(it) == cachedAddress.end())
            std::cout << "Not found in cache " << std::endl;
        else
            std::cout << "Found in cache";
#endif
        if (cachedAddress.find(it) == cachedAddress.end())
            connectTo(newNode,cloneGraph(it));
        else 
            connectTo(newNode, cachedAddress[it]);
    }
    return newNode;
}



int main()
{
    cout << "Cloning graph\n";
    GraphNode* myGraph = buildExample(1);
    cached.clear();
    printoutGraph(myGraph);
    cachedAddress.clear();
    cout << "Cloned graph " << endl;
    GraphNode *newGraph = cloneGraph(myGraph);
    cached.clear();
    printoutGraph(newGraph);
}

