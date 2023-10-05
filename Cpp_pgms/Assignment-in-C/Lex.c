#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "List.h"

#define MAX_STRINGS 100
#define MAX_STRING_LENGTH 100

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

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s input_file output_file\n", argv[0]);
        return 1;
    }

    char strings[MAX_STRINGS][MAX_STRING_LENGTH];
    int numStrings = 0;

    FILE *inputFile = fopen(argv[1], "r");
    if (inputFile == NULL) {
        perror("Error opening input file");
        return 1;
    }

    /* Read strings from the input file */
    while (numStrings < MAX_STRINGS && fgets(strings[numStrings], MAX_STRING_LENGTH, inputFile)) {
        // Remove the newline character if present
        size_t length = strlen(strings[numStrings]);
        if (length > 0 && strings[numStrings][length - 1] == '\n') {
            strings[numStrings][length - 1] = '\0';
        }
        numStrings++;
    }

    fclose(inputFile);

    /* Record index position of each string in List */
    List listStringIndex = newList();
    for (int i = 0; i < numStrings; i++) {
        append(listStringIndex, i);
    }

    /* Sort the list based on lexicographic order, comparing string. */
    sortStringList(listStringIndex, strings, numStrings);

    FILE *outputFile = fopen(argv[2], "w");
    if (outputFile == NULL) {
        perror("Error opening output file");
        return 1;
    }

    /* Write the sorted array of strings to the output file */
    for(moveFront(listStringIndex); index(listStringIndex)>=0; moveNext(listStringIndex)){
      int curIdx = get(listStringIndex);
      fprintf(outputFile, "%s\n", strings[curIdx]);
    }
    fclose(outputFile);

    printf("Strings sorted and written to output.txt\n");

    return 0;
}