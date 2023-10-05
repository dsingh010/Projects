/****************************************************************************************
*  ListTest.c
*  Test program for List ADT
*****************************************************************************************/
#include "List.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <assert.h>

#define MAX_STRING_LENGTH 100

/*
 * This function does a random shuffle to ensure we have different input
 * for the same input sequence.
 */
void shuffleArray(char arr[][MAX_STRING_LENGTH], int size) {
    srand(time(NULL));
    for (int i = size - 1; i > 0; i--) {
        int j = rand() % (i + 1);

        char temp[MAX_STRING_LENGTH];
        strcpy(temp, arr[i]);
        strcpy(arr[i], arr[j]);
        strcpy(arr[j], temp);
    }
}

/*
 * This function will sort the list entries in sorted order.
 */
void sortStringList(List sortedList, char arr[][MAX_STRING_LENGTH], int size)
{
  int i = 0;
  for (moveFront(sortedList); index(sortedList) >= 0; moveNext(sortedList), i++) {

      /* Get current cursor position */
      int arrayIdx = get(sortedList);
      int cursorIdx = index(sortedList);

      /* Start from the begining to the cursor index */
      moveFront(sortedList);
      for (int j = 0; j < cursorIdx; j++, moveNext(sortedList)) {
         /* keep shifting largest value to right */
         int curArrayIdx = get(sortedList);
         if (strcmp(arr[arrayIdx], arr[curArrayIdx]) < 0) {
            set(sortedList, arrayIdx);
            arrayIdx = curArrayIdx ;
         }
      }
      /* Largest value is a the end, where initially cursor index was. */
      set(sortedList, arrayIdx);
   }
}

/*
 * This function is used to test that list is sorted based on
 * lexicographic order of strings.
 */
void test_lexlist()
{
    char lexicalArray[][MAX_STRING_LENGTH] = {"Apple", "Banana", "Cherry", "Date", "Fig"};
    int arrayLength = sizeof(lexicalArray) / sizeof(lexicalArray[0]);

    /* Record index position of each string in List */
    List listStringIndex = newList();
    for (int i = 0; i < arrayLength; i++) {
        append(listStringIndex, i);
    }

    /*
     * This is to make the list random, so that every time
     * we run this program shuffle will generate a different
     * list of strings for same input array.
     */
    shuffleArray(lexicalArray, arrayLength);

    printf("======== String array before sort ==========\n");
    for(moveFront(listStringIndex); index(listStringIndex) >= 0; moveNext(listStringIndex)) {
      int curIdx = get(listStringIndex);
      printf("idx:%d value:%s\n", curIdx, lexicalArray[curIdx]);
    }
    printf("==========================================\n");

    /* Sort the list based on lexicographic order, comparing string. */
    sortStringList(listStringIndex, lexicalArray, arrayLength);

    printf("======== String array after sort ==========\n");
    int arrayIdx = 0;
    for(moveFront(listStringIndex); index(listStringIndex)>=0; moveNext(listStringIndex)){
      int curIdx = get(listStringIndex);
      printf("idx:%d value:%s\n", curIdx, lexicalArray[curIdx]);
      arrayIdx++;
    }
    printf("==========================================\n");
}

/**
 * Output of this program:
 * 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
 * 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1
 * 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
 * 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
 * false
 * false
 * true
 * 1 2 3 4 5 -1 6 7 8 9 11 12 13 14 15 -2 16 17 18 19 20
 * 21
 * 0
 */
void test_list()
{
   List A = newList();
   List B = newList();
   List C = NULL;
   int i;

   for(i=1; i<=20; i++){
      append(A,i);
      prepend(B,i);
   }

   printList(stdout,A);
   printf("\n");
   printList(stdout,B);
   printf("\n");

   for(moveFront(A); index(A)>=0; moveNext(A)){
      printf("%d ", get(A));
   }
   printf("\n");
   for(moveBack(B); index(B)>=0; movePrev(B)){
      printf("%d ", get(B));
   }
   printf("\n");

   C = copyList(A);
   printf("%s\n", equals(A,B)?"true":"false");
   printf("%s\n", equals(B,C)?"true":"false");
   printf("%s\n", equals(C,A)?"true":"false");

   moveFront(A);
   for(i=0; i<5; i++) {
      moveNext(A); // at index 5
   }
   insertBefore(A, -1); // at index 6

   for(i=0; i<9; i++) {
      moveNext(A); // at index 15
   }
   insertAfter(A, -2); // at index 16

   for(i=0; i<5; i++) {
      movePrev(A); // at index 10
   }

   delete(A);
   printList(stdout,A);
   printf("\n");
   printf("\n");
   printf("Before clear of List %d\n", length(A));
   clear(A);
   printf("After clear of List %d\n", length(A));

   freeList(&A);
   freeList(&B);
   freeList(&C);
}

int main(int argc, char* argv[]) {
   test_list();
   test_lexlist();
   return(0);
}

