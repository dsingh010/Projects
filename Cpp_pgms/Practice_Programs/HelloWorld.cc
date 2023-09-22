"""
Function newGraph() returns a Graph pointing to a newly created GraphObj representing a graph having
n vertices and no edges. Function freeGraph() frees all heap memory associated with the Graph *pG,
then sets the handle *pG to NULL. Functions getOrder() and getSize() return the corresponding field
values, and getSource() returns the source vertex most recently used in function BFS(), or NIL if
BFS() has not yet been called. Function getParent() will return the parent of vertex u in the BFS tree
created by BFS(), or NIL if BFS() has not yet been called. Function getDist() returns the distance from
the most recent BFS source to vertex u, or INF if BFS() has not yet been called. Function getPath()
appends to the List L the vertices of a shortest path in G from source to u, or appends to L the value NIL if
no such path exists. getPath() has the precondition getSource(G)!=NIL, so BFS() must be called
before getPath() is called. Functions getParent(), getDist() and getPath() all have the
precondition 1 ≤ 𝑢 ≤ getOrder(𝐺). Function makeNull() deletes all edges of G, restoring it to its 
5
original (no edge) state. (This is called a null graph in graph theory literature). Function addEdge()
inserts a new edge joining u to v, i.e. u is added to the adjacency List of v, and v to the adjacency List of u.
Your program is required to maintain these lists in sorted order by increasing labels. Function addArc()
inserts a new directed edge from u to v, i.e. v is added to the adjacency List of u (but not u to the adjacency
List of v). Both addEdge() and addArc() have the precondition that their two int arguments must lie
in the range 1 to getOrder(G). Function BFS() runs the BFS algorithm on the Graph G with source s,
setting the color, distance, parent, and source fields of G accordingly. Finally, function printGraph()
prints the adjacency list representation of G to the file pointed to by out. The format of this representation
should match the above examples, so all that is required by the client is a single call to printGraph().
"""
//ion to the above prototypes Graph.h will define the type Graph as well as #define constant
//macros INF and NIL
struct GraphObj{
    List* neighbors;
    List color;
    List parent;
    List distance;
    int order;
    int size;
    int source;
}

Graph newGraph(int n){
    Graph* a = new Graph();
    // n is no of verticies
    a->order = n;
    a->size = 0;
    a->source = NULL;
    a->color = MyList();
    a->parent = MyList();
    a->distance = MyList();

    // Each adj list starts empty
    a->neighbors.size() = n + 1;
    for (int i = 0; i <= n; i++) {
        a->neighbors[i] = MyList();
    }

    // there will be color,parent distancelist for each vertex
    for(int i = 0; i <= n; i++){
        a->color.append(WHITE);
        a->distance.append(INF);
        a->parent.append(NULL);
    }
    

    return g;
}



}
void freeGraph(Graph* pG){
    

}
/*** Access functions ***/
int getOrder(Graph G){
    return a->order;
}
int getSize(Graph G){
    return a->size;
}
int getSource(Graph G){
    return a->source;
}
int getParent(Graph G, int u){
    
}
int getDist(Graph G, int u){
    
}


void getPath(List L, Graph G, int u);
/*** Manipulation procedures ***/
void makeNull(Graph G);
void addEdge(Graph G, int u, int v);
void addArc(Graph G, int u, int v);
void BFS(Graph G, int s);
//Use psuedocode
void printGraph(FILE* out, Graph G);