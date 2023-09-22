#ifndef __LIST__H
#define __LIST__H

#include <iostream>

using namespace std;

struct Node {
    Node(int x)
    {
        index = x;
        front = back = nullptr;
    }

    int index;
    Node* front;
    Node* back;
};

class List {
public: /* Constructors-Destructors */
    List()
    {
        head = tail = cursor = nullptr;
        list_length = 0;
    }

    /*
     * Frees all heap memory associated with *pL, and sets
     * *pL to nullptr.
     */
    void freeList();

public: /* Access functions */
    /* Returns the number of elements in L. */
    int length() const;

    /* Returns index of cursor element if defined, -1 otherwise. */
    int index() const;

    /* Returns front element of L. Pre: length()>0 */
    int front();

    /* Returns back element of L. Pre: length()>0 */
    int back();

    /* Returns cursor element of L. Pre: length()>0, index()>=0 */
    int get();

    /*
     * Returns true iff Lists A and B are in same state, and returns
     * false otherwise.
     */
    bool equals(const List& B);

public: /* Manipulation procedures */
    /* Resets L to its original empty state. */
    void clear();

    /* Set cursor to tail. */
    void set_back();

    /*
     * Overwrites the cursor element’s data with x Pre: length()>0, index()>=0
     */
    void set(int x);

    /*
     * If L is non-empty, sets cursor under the front element, otherwise does nothing.
     */
    void moveFront();

    /*
     * If L is non-empty, sets cursor under the back element, otherwise does nothing.
     */
    void moveBack();

    /*
     * If cursor is defined and not at front, move cursor one
     * step toward the front of L; if cursor is defined and at
     * front, cursor becomes undefined; if cursor is undefined
     * do nothing
     */
    void movePrev();

    /*
     * If cursor is defined and not at back, move cursor one
     * step toward the back of L; if cursor is defined and at
     * back, cursor becomes undefined; if cursor is undefined
     * do nothing
     */
    void moveNext();

    /*
     * Insert new element into L. If L is non-empty, insertion takes place
     * before front element.
     */
    void prepend(int x);

    /*
     * Insert new element into L. If L is non-empty, insertion takes place
     * after back element.
     */
    void append(int x);

    /*
     * Insert new element before cursor. Pre: length()>0, index()>=0
     */
    void insertBefore(int x);

    /* Insert new element after cursor.Pre: length()>0, index()>=0 */
    void insertAfter(int x);

    /* Delete the front element. Pre: length()>0 */
    void deleteFront();

    /* Delete the back element. Pre: length()>0 */
    void deleteBack();

    /*
     * Delete cursor element, making cursor undefined. Pre: length()>0, index()>=0
     */
    void delete_list();

    /*
     * Print the list.
     */
    void printList();

    /*
     * Print the list in reverse.
     */
    void printRevList();

    public: /* Other operations */
    /*
     * Returns a new List representing the same integer
     * sequence as L. The cursor in the new list is undefined,
     * regardless of the state of the cursor in L. The state
     * of L is unchanged.
     */
    List copyList();

    /*
     * Returns a new List which is the concatenation of
     * A and B. The cursor in the new List is undefined,
     * regardless of the states of the cursors in A and B.
     * The states of A and B are unchanged.
     */
    List concatList(List B);

    Node* get_cursor() const
    {
        return cursor;
    }

private:
    Node* head;      /*< Points to head of the list */
    Node* tail;      /*< Points to the tail of the list */
    Node* cursor;    /*< Cursor points to where we are in the list */
    int list_length; /*< Length of list. */
};

/*
 * Creates and returns a new empty List.
 */
List newList(void);

/*
 * Frees all heap memory associated with *pL, and sets *pL to nullptr.
 */
void freeList(List* pL);

/* Returns the number of elements in L. */
int length(List L);

/* Returns index of cursor element if defined, -1 otherwise. */
int index(List L);

/* Returns front element of L. Pre: length()>0 */
int front(List L);

/* Returns back element of L. Pre: length()>0 */
int back(List L);

/* Returns cursor element of L. Pre: length()>0, index()>=0 */
int get(List L);

/*
 * Returns true iff Lists A and B are in same state, and returns
 * false otherwise.
 */
bool equals(List A, List B);

/* Resets L to its original empty state. */
void clear(List L);

/*
 * Overwrites the cursor element’s data with x Pre: length()>0, index()>=0
 */
void set(List L, int x);

/*
 * If L is non-empty, sets cursor under the back element, otherwise does nothing.
 */
void moveBack(List L);

/*
 * If cursor is defined and not at front, move cursor one
 * step toward the front of L; if cursor is defined and at
 * front, cursor becomes undefined; if cursor is undefined
 * do nothing
 */
void movePrev(List L);

/*
 * If cursor is defined and not at back, move cursor one
 * step toward the back of L; if cursor is defined and at
 * back, cursor becomes undefined; if cursor is undefined
 * do nothing
 */
void moveNext(List L);

/*
 * Insert new element into L. If L is non-empty, insertion takes place
 * before front element.
 */
void prepend(List L, int x);

/*
 * Insert new element into L. If L is non-empty, insertion takes place
 * after back element.
 */
void append(List L, int x);

void insertAfter(List L, int x);

/* Delete the front element. Pre: length()>0 */
void deleteFront(List L);

/* Delete the back element. Pre: length()>0 */
void deleteBack(List L);

/*
 * Delete cursor element, making cursor undefined. Pre: length()>0, index()>=0
 */
void deleteCursor(List L);

/*
 * Prints to the file pointed to by out, a string representation of L consisting
 * of a space separated sequence of integers, with front on left.
 */
void printList(FILE* out, List L);

/*
    * Returns a new List representing the same integer
    * sequence as L. The cursor in the new list is undefined,
    * regardless of the state of the cursor in L. The state
    * of L is unchanged.
    */
List copyList(List L);

/*
    * Returns a new List which is the concatenation of
    * A and B. The cursor in the new List is undefined,
    * regardless of the states of the cursors in A and B.
    * The states of A and B are unchanged.
    */
List concatList(List A, List B);

#endif