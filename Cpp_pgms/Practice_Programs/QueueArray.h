#include <iostream>

using namespace std;
 const int QUEUE_SZ = 10;
class Queue {
public:
    Queue()
    {
        forward = -1;
        rear = -1;
        count = 0;
    }

    void push(int);
    void pop();
    int front();
    bool empty();
    int size();

private:

    int forward;
    int rear;
    int count;
    int queue_array[QUEUE_SZ];
};