#ifndef MIN_HEAP_H
#define MIN_HEAP_H

#include <iostream>
#include <vector>
#include <limits>
using namespace std;


class MinHeap {
public:
    MinHeap()
    {}

    void insertKey(int key);
    int extractMin();
    void decreaseKey(int old_key_val, int new_key_val);

    int getMin()
    {
        return arr[0];
    }

    int deleteKey(int key);
    void minHeapify(int index);
    bool is_empty() {
        return arr.size() == 0;
    }

private: /* Methods */
    int parent_idx(int idx)
    {
        return (idx - 1)/2;
    }

    int left_child_idx(int idx)
    {
        return (2 * idx) + 1;
    }

    int right_child_idx(int idx)
    {
        return (2 * idx) + 2;
    }
private:
    vector<int> arr;
};

#endif
