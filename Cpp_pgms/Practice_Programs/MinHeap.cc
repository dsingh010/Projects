#include "MinHeap.h"

void MinHeap::insertKey(int key)
{
    if (arr.size() == 0) {
       arr.push_back(key);
    } else {
        arr.push_back(key);
        int cur_idx = arr.size() - 1;

        while (cur_idx != 0 &&  arr[parent_idx(cur_idx)] > arr[cur_idx]) {
            swap(arr[cur_idx], arr[parent_idx(cur_idx)]);
            cur_idx = parent_idx(cur_idx);
        }
    }
}

int MinHeap::extractMin()
{
    int key_removed = numeric_limits<int>::max();
    if (arr.size() != 0) {
        key_removed = arr[0];
        if (arr.size() == 1) {
            arr.clear();
        } else {
            vector<int> tmp_arr(arr.begin() + 1, arr.end());
            arr.clear();
            for (int key : tmp_arr) {
                arr.push_back(key);
            }
            minHeapify(0);
        }
    }
    return key_removed;
}


void MinHeap::decreaseKey(int old_key_val, int new_key_val)
{
    int idx = 0;
    for (int i = 0 ; i < arr.size(); i++) {
        if (arr[i] == old_key_val) {
            arr[i] = new_key_val;
            idx = i;
            break;
        }
    }

    while (idx != 0 and arr[parent_idx(idx)] > arr[idx]) {
        swap(arr[parent_idx(idx)], arr[idx]);
        idx = parent_idx(idx);
    }
    swap(arr[idx], arr[0]);
    minHeapify(0);

}

void MinHeap::minHeapify(int index)
{
    int left_key_idx = left_child_idx(index);
    int right_key_idx = right_child_idx(index);

    right_key_idx = arr.size() <= right_key_idx ? index : right_key_idx;
    left_key_idx =  arr.size() <= left_key_idx ? index : left_key_idx;

    if (arr[left_key_idx] < arr[index] || arr[right_key_idx] < arr[index]) {
        if (arr[left_key_idx] < arr[right_key_idx]) {
            swap(arr[index], arr[left_key_idx]);
            index = left_key_idx;
        } else if (arr[left_key_idx] > arr[right_key_idx]) {
            swap(arr[index], arr[right_key_idx]);
            index = right_key_idx;
        }
        minHeapify(index);
    }
}

int MinHeap::deleteKey(int key)
{
    int key_removed = numeric_limits<int>::max();
    if (arr.size() != 0) {
        key_removed = key;
        vector<int> tmp_arr;
        for (int i = 0 ; i < arr.size(); i++) {
            if (arr[i] != key) {
                tmp_arr.push_back(arr[i]);
            }
        }
        arr.clear();
        for (int num : tmp_arr) {
            arr.push_back(num);
        }
        minHeapify(0);
    }
    return key_removed;
}

int main()
{
    MinHeap min_heap;

    min_heap.insertKey(3);
    min_heap.insertKey(2);
    min_heap.deleteKey(3);
    min_heap.insertKey(15);
    min_heap.insertKey(5);
    min_heap.insertKey(4);
    min_heap.insertKey(45);

    cout << min_heap.extractMin() << " ";
    cout << min_heap.getMin() << " ";
    min_heap.decreaseKey(5, 1);

    cout << min_heap.getMin() << endl;

    while (!min_heap.is_empty()) {
        cout << min_heap.extractMin() << endl;
    }
    return 0;
}
