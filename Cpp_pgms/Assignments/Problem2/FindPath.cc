#include "../Problem1/List.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <queue>

using namespace std;

/* Define constants for INF and NIL */
const int INF = 1000000;
const int NIL = -1;

/**
 * White: White is used to indicate that a vertex has not been visited or explored yet.
 * When the traversal algorithm begins, all vertices are initially marked as white.
 *
 * Gray: Gray is used to indicate that a vertex is currently being processed or explored.
 * When a vertex is first encountered during the traversal, it is marked as gray.
 * This means that the algorithm is actively exploring the neighbors of this vertex.
 *
 * Black: Black is used to indicate that a vertex has been fully explored,
 * including all its neighbors. Once all neighbors of a vertex have been processed,
 * the vertex is marked as black. This implies that the algorithm has finished exploring
 * this vertex and moved on to other parts of the graph.
 */
enum Color {
    WHITE = 0,
    GRAY = 1,
    BLACK = 2
};

struct Graph {
    /**
     * Constructor
     */
    Graph(int num_vertices) {
        V = num_vertices;
        adj_list = new List[num_vertices + 1];
        color = new int[num_vertices + 1];
        parent = new int[num_vertices + 1];
        distance = new int[num_vertices + 1];

        for (int i = 0; i <= num_vertices; i++) {
            color[i] = Color::WHITE;
            parent[i] = NIL;
            distance[i] = INF;
        }
    }

    void reset_color_parent_dist()
    {
        for (int i = 0; i <= V; i++) {
            color[i] = Color::WHITE;
            parent[i] = NIL;
            distance[i] = INF;
        }
    }

    /**
     * Function to add edge
     */
    void addEdge(int v, int w) {
        adj_list[v].append(w);
        adj_list[w].append(v);
    }

    /**
     * Function to print adjacency list.
     */
    void printAdjList(std::ostream& ss) {
        for (int i = 0; i <= V; i++) {
            ss << i << ":";
            if (adj_list[i].length() > 0) {
                adj_list[i].printList(ss);
            }
            ss << endl;
        }
    }

    /**
     * give back the heap memory used by the graph.
     */
    void freeGraph()
    {
        for (int i = 0; i <= V; i++) {
            adj_list[i].delete_list();
        }
        delete[] adj_list;
        delete[] color;
        delete[] parent;
        delete[] distance;

        adj_list = nullptr;
        color = nullptr;
        parent = nullptr;
        distance = nullptr;
        V = 0;
    }

    /**
     * Destructor
     */
    ~Graph() {
        freeGraph();
    }

    /**
     * Variables associated with the graph.
     */
    int V;              /* Number of vertices */
    List* adj_list;     /* Pointer to an array of adjacency list*/
    int* color;         /* Color of vertices */
    int* parent;        /* Parent of vertices */
    int* distance;      /* Distance from source */
};

void BFS(Graph& G, int s, int dest) {
    queue<int> q;
    q.push(s);
    G.color[s] = Color::GRAY;
    G.distance[s] = 0;

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        if (dest == u) {
            return;
        }
        List& adj_list = G.adj_list[u];
        adj_list.clear();
        for (int i = 0; i < G.adj_list[u].length(); i++) {
            int v = G.adj_list[u].index();
            if (G.color[v] == Color::WHITE) { // White

                q.push(v);
                G.color[v] = Color::GRAY;
                G.distance[v] = G.distance[u] + 1;
                G.parent[v] = u;
            }
            G.adj_list[u].moveNext();
        }
        G.color[u] = Color::BLACK; // Mark as black
    }
}

void getPath(Graph& G, int s, int d, stringstream& ss) {
    if (d == s) {
        ss << s << " ";
    } else if (G.parent[d] == 0) {
        ss << "No path exists";
    } else {
        getPath(G, s, G.parent[d], ss);
        ss << d << " ";
    }
}

int main(int argc, char* argv[])
{
    if (argc != 3) {
        cerr << "Usage: " << argv[0] << " input_file output_file" << endl;
        return 1;
    }

    ifstream input(argv[1]);
    ofstream output(argv[2]);

    int n ; // Number of vertices
    input >> n;

    Graph *pG = new Graph(n);

    int u, v;
    while (input >> u >> v && (u != 0 || v != 0)) {
        pG->addEdge(u, v);
    }

    pG->printAdjList(output);


    int s, d;
    while (input >> s >> d && (s != 0 || d != 0)) {
        BFS(*pG, s, d);
        stringstream ss;
        getPath(*pG, s, d, ss);

        // Output results
        output << "The distance from " << s << " to " << d << " is " << pG->distance[d] << endl;
        output << "A shortest " << s << "-" << d << " path is: ";
        if (pG->distance[d] != INF) {
            output << ss.str() << endl;
        } else {
            output << "No path exists" << endl;
        }
        output << endl;
        pG->reset_color_parent_dist();
    }

    input.close();
    output.close();
    pG->freeGraph();

    return 0;
}