#include "StackList.h"

void Stack::push(int data)
{
    Node* node = new Node();
    node->data = data;
    if (cur_top == nullptr) {
        cur_top = node;
    } else {
        node->next = cur_top;;
        cur_top = node;
    }
}

void Stack::pop()
{
    if (top != nullptr) {
        Node* tmp = cur_top;
        cur_top = tmp->next;                                         
        delete cur_top;
    } 
}

int Stack::top()
{
    if (top == nullptr) {
        return -1;
    }
    return cur_top->data;
}

int Queue::front()
{
    if (head != nullptr) {
        return head->data;
    }
}

void Queue::enqueue(int data)
{
    Node* node = new Node();
    node->data = data;
    if (head == nullptr) {
        tail = node;
        head = tail;
    } else {
        tail->next = node;
        tail = node;
    }
}

void Queue::dequeue()
{
    if (head != nullptr) {
        Node* tmp_node = head->next;
        delete head;
        head = tmp_node;
    }
}