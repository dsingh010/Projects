#ifndef _STACK_H
#define _STACK_H

#include <iostream>
const int max_elem = 100;

class Stack{
    public:
        Stack() {
           idx = -1;
        }

        void push(int data);
        void pop();
        int top();
        bool empty();

    private:   
        int idx;
        int stack_array[max_elem];
};

#endif