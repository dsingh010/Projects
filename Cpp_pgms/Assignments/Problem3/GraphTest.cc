#include "Graph.h"

int main() {
    int numVertices, u, v;
    cout << "Enter the number of vertices: ";
    cin >> numVertices;

    Graph graph(numVertices);

    cout << "Enter the arcs (u v), terminate with (0 0):\n";
    while (true) {
        cin >> u >> v;
        if (u == 0 && v == 0) {
            break;
        }
        graph.addArc(u, v);
    }

    cout << "======= print Adj List ===================" << endl;
    graph.printAdjList(std::cout);

    cout << "======= print Transpose Adj List ===================" << endl;
    graph.printTransposeAdjList(std::cout);

    cout << " ==== DFS ======" << endl;
    graph.DFS();
    for (int i = 1; i <= numVertices; i++) {
        cout<< "[" << i << "]" << " DISCOVER time:" << graph.discoverTime[i]
        <<  " FINISH time:" << graph.finishTime[i] << endl;
    }

    Graph transposedGraph = graph.transpose();

    cout << " ==== Strongly connected componenents ===== " << endl;
    graph.printStronglyConnectedComponents();

    return 0;
}