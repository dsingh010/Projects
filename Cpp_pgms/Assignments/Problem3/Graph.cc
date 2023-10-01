#include "Graph.h"
#include <algorithm>

using namespace std;

Graph::Graph(int vertices) {
    this->num_vertices = vertices;
    adj = new List[num_vertices + 1];
    adjTranspose = new List[num_vertices + 1];
    color = new int[num_vertices + 1];
    discoverTime = new int[num_vertices + 1];
    finishTime = new int[num_vertices + 1];

    for (int i = 0; i <= num_vertices; i++) {
        color[i] = WHITE;
        discoverTime[i] = -1;
        finishTime[i] = -1;
    }
    time = 0;
}

void Graph::addArc(int u, int v) {
    adj[u].append(v);
    adjTranspose[v].append(u);
}

Graph Graph::transpose() {
    Graph transposedGraph(num_vertices);
    for (int v = 1; v <= num_vertices; ++v) {
        adj[v].clear();
        for (int i = 0; i < adj[v].length(); i++) {
            int neighbor = adj[v].index();
            transposedGraph.addArc(neighbor, v);
        }
    }
    return transposedGraph;
}

Graph Graph::copyGraph() {
    Graph copiedGraph(num_vertices);
    for (int v = 1; v <= num_vertices; ++v) {
        adj[v].clear();
        for (int i = 0; i < adj[v].length(); i++) {
            int neighbor = adj[v].index();
            copiedGraph.addArc(v, neighbor);
        }
    }
    return copiedGraph;
}

void Graph::DFSUtil(int v) {
    color[v] = GREY;
    discoverTime[v] = ++time;
    adj[v].clear();
    for (int i = 0; i < adj[v].length(); i++) {
        int neighbor = adj[v].index();
        if (color[neighbor] == WHITE) {
            DFSUtil(neighbor);
        }
        adj[v].moveNext();
    }
    color[v] = BLACK;
    finishTime[v] = ++time;
    dfsStack.push(v);
}

void Graph::DFS() {
    for (int i = 1; i <= num_vertices; ++i) {
        if (color[i] == WHITE) {
            DFSUtil(i);
        }
    }
}

void Graph::DFSTransposeUtil(int v, vector<int>& component) {
    color[v] = GREY;
    component.push_back(v);
    adjTranspose[v].clear();

    for (int i = 0; i < adjTranspose[v].length(); i++) {
        int neighbor = adjTranspose[v].index();
        if (color[neighbor] == WHITE) {
            DFSTransposeUtil(neighbor, component);
        }
        adjTranspose[v].moveNext();
    }
    color[v] = BLACK;
}

/**
 * Function to print adjacency list.
 */
void Graph::printAdjList(std::ostream& ss) {
    for (int i = 1; i <= num_vertices; i++) {
        ss << i << ":";
        if (adj[i].length() > 0) {
            adj[i].printList(ss);
        }
        ss << endl;
    }
}

void Graph::printTransposeAdjList(std::ostream& ss) {
    for (int i = 1; i <= num_vertices; i++) {
        ss << i << ":";
        if (adjTranspose[i].length() > 0) {
            adjTranspose[i].printList(ss);
        }
        ss << endl;
    }
}

void Graph::printStronglyConnectedComponents() {
    for (int i = 0; i <= num_vertices; ++i) {
        color[i] = WHITE;
    }

    vector<pair<int,int>> finish_times;
    for (int i = 0; i <= num_vertices; ++i) {
        finish_times.push_back({i, finishTime[i]});
    }

    std::sort(finish_times.begin(), finish_times.end(),
         [](const pair<int, int>& a, const pair<int, int>& b) {
             return a.second > b.second;
         });

    for (const auto& vertexFinishTime : finish_times) {
        int v = vertexFinishTime.first;
        if (color[v] == WHITE) {
            vector<int> component;
            DFSTransposeUtil(v, component);
            cout << "Component: ";
            for (int vertex : component) {
                cout << vertex << " ";
            }
            cout << endl;
        }
    }
}

int Graph::getOrder() {
    return num_vertices;
}

int Graph::getDiscover(int u) {
    return discoverTime[u];
}

int Graph::getFinish(int u) {
    return finishTime[u];
}

