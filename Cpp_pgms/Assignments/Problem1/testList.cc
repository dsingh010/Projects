#include "List.h"
#include <vector>
#include <algorithm>
#include <random>
#include <string>

/*
 * https://www.learncpp.com/cpp-tutorial/generating-random-numbers-using-mersenne-twister/
 */
void random_list(List* list)
{
  // Create a vector of elements to shuffle
  std::vector<int> myVector = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

  // Initialize the random number generator
  std::random_device rd;
  std::mt19937 rng(rd()); // Mersenne Twister engine

  // Shuffle the elements in the vector
  std::shuffle(myVector.begin(), myVector.end(), rng);

  // Print the shuffled vector
  for (const auto& element : myVector) {
    list->append(element);
  }
}

void append_list_print()
{
    List new_list;
    for (int i = 1; i < 10; i++) {
        new_list.append(i);
    }
    cout << "======= Print List using front pointer =======" << endl;
    new_list.printList(std::cout);
    cout << "======= Print List using back pointer =======" << endl;
    new_list.printRevList();
}

void insertion_sort(List* sorted_list)
{
  // Move the cursor to the begining
  sorted_list->moveFront();

  for (int i = 0; i < sorted_list->length(); i++) {
    int cur_idx = sorted_list->index();
    sorted_list->moveFront();

    for (int j = 0; j <= i; j++) {
      // keep shifting largest number
      if (cur_idx < sorted_list->index()) {
        int tmp_idx = sorted_list->index();
        sorted_list->set(cur_idx);
        cur_idx = tmp_idx;
      } else if (j == i && cur_idx > sorted_list->index()) {
        // largest number shoulld be at the last spot
        sorted_list->set(cur_idx);
      }
      sorted_list->moveNext();
    }
  }
}

int main()
{
  append_list_print();
  List list_rand_num;
  random_list(&list_rand_num);
  cout << " =============  Before sort ========== " << endl;

  list_rand_num.printList(std::cout);

  cout << "================ ======================" << endl;
  insertion_sort(&list_rand_num);
  cout << " =============  After sort ========== " << endl;
  list_rand_num.printList(std::cout);
  return 0;
}
