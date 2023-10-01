#include <iostream>
#include <vector>
#include <stack>
#include "../Problem1/List.h"

using namespace std;

const int WHITE = 0;
const int GREY = 1;
const int BLACK = 2;

/* Define a class for the directed graph */
class Graph {
public:
    Graph(int vertices);
    void addArc(int u, int v);
    Graph transpose();
    Graph copyGraph();
    void DFS();
    void printStronglyConnectedComponents();
    int getOrder();
    int getDiscover(int u);
    int getFinish(int u);
    void printAdjList(std::ostream& ss);
    void printTransposeAdjList(std::ostream& ss);

public:
    int* discoverTime;
    int* finishTime;

private:
    int num_vertices;
    List* adj;
    List* adjTranspose;
    int* color;
    stack<int> dfsStack;
    int time;

    void DFSUtil(int v);
    void DFSTransposeUtil(int v, vector<int>& component);
};