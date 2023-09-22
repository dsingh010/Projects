#include <iostream>

using namespace std;

struct Node {
    int data;
    Node* next;

    Node() {
        data = -1;
        next = nullptr;
    }
};

class Stack {
    public:
        void push(int data);
        void pop();
        int top();
        Stack () {
            cur_top = nullptr;
        }
    private:
        Node* cur_top;
};

class Queue {
    public:
        void enqueue(int data);
        void dequeue();
        int front();
        Queue () {
            head = tail = nullptr;
        }
    private:
        Node* head;
        Node* tail;
}