#include "QueueArray.h"

void Queue::push(int data)
{
    if ((forward == 0 && rear == QUEUE_SZ - 1) ||
        (rear + 1) % QUEUE_SZ == forward) {
        cout << "queue is full" << endl;
    } else if ( forward == -1) {
        /* Insert after element */
        forward = rear = 0;
        queue_array[0] = data;
    } else if (rear == QUEUE_SZ - 1 && forward != 0) {
        rear = 0;
        queue_array[rear] = data;
    } else {
        rear++;
        queue_array[rear] = data;
    }

}

void Queue::pop()
{
    if (forward == -1) {
        cout<< "Queue is empty" <<endl;
        return;
    }

    int data = queue_array[forward];
    queue_array[forward] = -1;

    if (forward == rear) {
        forward = rear - 1;
    } else if (forward == QUEUE_SZ - 1) {
        forward = 0;
    } else {
        forward++;
    }
}

int Queue::front()
{
    return queue_array[forward];
}

int Queue::size()
{
    return count;
}

bool Queue::empty()
{
    return (forward == rear);
}

int main()
{
    Queue q;

    for (int i = 0; i < 10; i++) {
        q.push(i);
    }

    while (!q.empty()) {
        cout << q.front() << endl;
        q.pop();
    }

    return 0;
}