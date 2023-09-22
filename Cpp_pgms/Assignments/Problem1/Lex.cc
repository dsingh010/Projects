#include "List.h"
#include <iostream>
#include <algorithm>
#include <random>
#include <string>

void sort_string_list(List* sorted_list, string* arr)
{
  // Move the cursor to the begining
  sorted_list->moveFront();

  for (int i = 0; i < sorted_list->length(); i++) {
    int cur_idx = sorted_list->index();
    sorted_list->moveFront();

    for (int j = 0; j <= i; j++) {
      // keep shifting largest number
      if (arr[cur_idx] < arr[sorted_list->index()]) {
        int tmp_idx = sorted_list->index();
        sorted_list->set(cur_idx);
        cur_idx = tmp_idx;
      } else if (j == i && arr[cur_idx] > arr[sorted_list->index()]) {
        // largest number shoulld be at the last spot
        sorted_list->set(cur_idx);
      }
      sorted_list->moveNext();
    }
  }
}

int main()
{
    std::string lexicalArray[] = {"Apple", "Banana", "Cherry", "Date", "Fig"};

    // Get the length of the array
    int arrayLength = sizeof(lexicalArray) / sizeof(lexicalArray[0]);

    // Seed the random number generator
    std::random_device rd;
    std::mt19937 rng(rd());

    // Shuffle the array
    std::shuffle(lexicalArray, lexicalArray + arrayLength, rng);

    cout << "======= String array before sort =========" << endl;
    for (int i = 0; i < arrayLength; i++) {
    cout << lexicalArray[i] << endl;
    }

    List list_string_index;
    for (int i = 0; i < arrayLength; i++) {
        list_string_index.append(i);
    }

    sort_string_list(&list_string_index, lexicalArray);

    cout << " ======== String array after sort ===========" << endl;
    list_string_index.moveFront();

    for (int i = 0; i <  arrayLength; i++) {
    cout << lexicalArray[list_string_index.index()] << endl;
    list_string_index.moveNext();
    }

    return 0;
}