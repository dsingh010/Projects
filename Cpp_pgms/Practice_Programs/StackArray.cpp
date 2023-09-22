#include "StackArray.h"

using namespace std;

void Stack::push(int data){
    idx = idx + 1;
    stack_array[idx] = data;

}

void Stack:: pop(){
    if (idx != -1){
        stack_array[idx] = 0;
        idx--;
    }
}

int Stack:: top(){
    if (idx == -1){
        return -1;
    }
    return stack_array[idx];
}

bool Stack:: empty(){
    return idx == -1;
}

int main() {
    Stack st;
    for(int i = 0;i<10;i++){
        st.push(i);
    }
    while (!st.empty()){
        cout<<st.top()<<endl;
        st.pop();
    }
    return 0;
}


















