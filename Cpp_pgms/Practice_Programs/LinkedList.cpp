#include "LinkedList.h"

void LinkedList::append(int data) {
    Node* new_node = new Node(data);
    if (!head) {
        head = new_node;
        return;
    }
    Node* current = head;
    while (current->next) {
        current = current->next;
    }
    current->next = new_node;
}

void LinkedList::display() {
    Node* current = head;
    while (current) {
        std::cout << current->data << " -> ";
        current = current->next;
    }
    std::cout << "nullptr" << std::endl;
}

int main() {
    LinkedList linkedList;
    linkedList.append(10);
    linkedList.append(20);
    linkedList.append(30);

    linkedList.display();

    return 0;
}