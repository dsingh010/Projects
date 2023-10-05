#include "List.h"
#include <assert.h>

#define FAILED -1

/* Returns reference to new Node */
Node newNode(NodeElement data)
{
    Node tmp_node = malloc(sizeof(struct NodeObj));
    assert(tmp_node != NULL);
    if (tmp_node != NULL) {
        tmp_node->value = data;
        tmp_node->front = tmp_node->back = NULL;
    }
    return tmp_node;
}

/* Frees up the heap memory pointed by pN and sets it to NULL */
void freeNode(Node* pN)
{
    if (pN != NULL) {
        free(*pN);
        *pN = NULL;
    }
}

/* Returns reference to new empty List */
List newList()
{
    List tmp_list = malloc(sizeof(struct ListObj));
    assert(tmp_list != NULL);
    if (tmp_list != NULL) {
        tmp_list->list_length = 0;
        tmp_list->cursor_index = -1;
        tmp_list->head = tmp_list->tail = tmp_list->cursor = NULL;
    }
    return tmp_list;
}

/* Frees up heap memory pointed by */
void freeList(List* pL)
{
    /* Nothing to do for an empty List */
    if (pL == NULL || *pL == NULL) {
        return;
    }
    if ((*pL)->list_length > 0) {
        printf("Deleting a non empty list\n");
    }
    free(*pL);
    *pL = NULL;
}

/* Returns the number of elements in L. */
int length(List L)
{
    return L->list_length;
}

/* Returns index of cursor element if defined, -1 otherwise. */
int index(List L)
{
    return L->cursor_index;
}

/* Returns front element of L. Pre: length()>0 */
int front(List L)
{
    if (L->list_length > 0) {
        return L->head->value;
    }
    printf("List error front called on an empty list\n");
    return FAILED;
}

/* Returns back element of L. Pre: length()>0 */
int back(List L)
{
    if (L->list_length > 0) {
        return L->tail->value;
    }
    printf("List error back called on an empty list\n");
    return FAILED;
}

/* Returns the cursor element of L.*/
int get(List L)
{
    if (L->list_length > 0 && L->cursor_index >= 0) {
        return L->cursor->value;
    }
    return FAILED;
}

/*
 * Returns true iff Lists A and B are in same state, and returns
 * false otherwise.
 */
bool equals(List A, List B)
{
    if (A->list_length != B->list_length) {
        return false;
    }
    /* Two empty lists are equal */
    if (A->list_length == B->list_length && A->list_length == 0)
    {
        return true;
    }

    moveFront(A);
    moveFront(B);
    while (index(A) >= 0 && index(B) >= 0) {
        if (get(A) != get(B)) {
            return false;
        }
        moveNext(A);
        moveNext(B);
    }
    return index(A) == index(B);
}

/* Resets L to its original empty state. */
void clear(List L)
{
    moveBack(L);
    while (index(L) >= 0) {
        deleteBack(L);
        moveBack(L);
    }
    L->cursor = L->head = L->tail = NULL;
    L->cursor_index = -1;
    L->list_length = 0;
}

/* Overwrites the cursor element’s data with x */
void set(List L, int x)
{
    if (length(L) > 0 && L->cursor_index >= 0) {
        L->cursor->value = x;
    }
}

/*
 * If L is non-empty, sets cursor under the front element, otherwise does nothing.
 */
void moveFront(List L)
{
    if (length(L) > 0) {
        L->cursor = L->head;
        L->cursor_index = 0;
    }
}

/*
 * If L is non-empty, sets cursor under the back element, otherwise does nothing.
 */
void moveBack(List L)
{
    if (length(L) > 0) {
        L->cursor = L->tail;
        L->cursor_index = length(L) - 1;
    }
}

/*
 * If cursor is defined and not at front, move cursor one
 * step toward the front of L; if cursor is defined and at
 * front, cursor becomes undefined; if cursor is undefined
 * do nothing
 */
void movePrev(List L)
{
    if (L->cursor_index > 0) {
        L->cursor = L->cursor->back;
        L->cursor_index = L->cursor_index - 1;
    } else {
        L->cursor_index = -1;
        L->cursor = NULL;
    }
}

/*
 * If cursor is defined and not at back, move cursor one
 * step toward the back of L; if cursor is defined and at
 * back, cursor becomes undefined; if cursor is undefined
 * do nothing
 */
void moveNext(List L)
{
    if (L->cursor_index < length(L) - 1) {
        L->cursor = L->cursor->front;
        L->cursor_index = L->cursor_index + 1;
    } else {
        L->cursor_index = -1;
        L->cursor = NULL;
    }
}

/*
 * Insert new element into L. If L is non-empty, insertion takes place
 * before front element.
 */
void prepend(List L, int x)
{
    Node tmp_node = newNode(x);
    if (tmp_node == NULL) {
        printf("Error no memory, prepend\n");
        return;
    }
    if (length(L) > 0) {
        tmp_node->back = NULL;
        tmp_node->front = L->head;
        L->head->back = tmp_node;
        L->head = tmp_node;
        if (L->cursor_index != -1) {
            L->cursor_index = L->cursor_index + 1;
        }
    } else {
        L->head = tmp_node;
        L->tail = tmp_node;
        L->cursor = tmp_node;
        L->head->front = NULL;
        L->head->back = NULL;
        L->tail->front = NULL;
        L->tail->back = NULL;
        L->cursor_index = 0;
    }
    L->list_length++;
}

/*
 * Insert new element into L. If L is non-empty, insertion takes place
 * after back element.
 */
void append(List L, int x)
{
    Node tmp_node = newNode(x);
    if (tmp_node == NULL) {
        printf("Error no memory, append\n");
        return;
    }
    if (length(L) > 0) {
        tmp_node->front = NULL;
        tmp_node->back = L->tail;
        L->tail->front = tmp_node;
        L->tail = tmp_node;
        L->cursor = L->tail;
    } else {
        L->head = tmp_node;
        L->tail = tmp_node;
        L->cursor = tmp_node;
        L->cursor_index = 0;
        L->head->front = NULL;
        L->head->back = NULL;
        L->tail->front = NULL;
        L->tail->back = NULL;
    }
    L->list_length++;
    L->cursor_index++;
}

/*
 * Insert new element before cursor. Pre: length()>0, index()>=0
 */
void insertBefore(List L, int x)
{
    if (length(L) == 0 || index(L) == -1) {
        printf("List error insertBefore length:%d index:%d\n",
                length(L), index(L));
        return;
    }
    Node tmp_node = newNode(x);
    Node back_node = L->cursor->back;

    back_node->front = tmp_node;
    tmp_node->front = L->cursor;
    tmp_node->back = back_node;
    L->cursor->back = tmp_node;
    L->list_length++;
    L->cursor_index++;
}

/* Insert new element after cursor.Pre: length()>0, index()>=0 */
void insertAfter(List L, int x)
{
    if (length(L) == 0 || index(L) == -1) {
        printf("List error insertAfter length:%d index:%d\n",
                length(L), index(L));
        return;
    }
    Node tmp_node = newNode(x);
    Node front_node = L->cursor->front;
    /* cursor_index not affected as the node is added after cursor */
    front_node->back = tmp_node;
    tmp_node->back = L->cursor;
    tmp_node->front = L->cursor->front;
    L->cursor->front = tmp_node;
    L->list_length++;
}

/* Delete the front element. Pre: length()>0 */
void deleteFront(List L)
{
    if (length(L) > 0) {
        Node tmp_node = L->head;
        /* Only one node in the List */
        if (length(L) == 1) {
            L->head = NULL;
            L->tail = NULL;
            L->cursor = NULL;
        } else {
            Node front_node = L->head->front;
            front_node->back = NULL;
            L->head = front_node;
        }
        L->cursor_index = -1;
        freeNode(&tmp_node);
        L->list_length--;
    }
}

/* Delete the back element. Pre: length()>0 */
void deleteBack(List L)
{
    if (length(L) > 0) {
        Node tmp_node = L->tail;
        if (length(L) == 1) {
           L->head = NULL;
           L->tail = NULL;
           L->cursor = NULL;
        } else {
            Node back_node = L->tail->back;
            back_node->front = NULL;
            L->tail = back_node;
        }
        L->cursor_index = -1;
        freeNode(&tmp_node);
        L->list_length--;
    }
}

/*
 * Delete cursor element, making cursor undefined. Pre: length()>0, index()>=0
 */
void delete(List L)
{
    if (length(L) > 0 && index(L) >= 0)
    {
        if (L->cursor_index == 0) {
            deleteFront(L);
        } else if (L->cursor_index == length(L) - 1) {
            deleteBack(L);
        } else {
            Node back_node = L->cursor->back;
            Node front_node = L->cursor->front;
            front_node->back = back_node;
            back_node->front = front_node;
            free(L->cursor);
            L->list_length = L->list_length - 1;
        }
        L->cursor = NULL;
        L->cursor_index = -1;
    }
}

/*
 * Prints to the file pointed to by out, a string representation of L consisting
 * of a space separated sequence of integers, with front on left.
 */
void printList(FILE* out, List L)
{
    if (length(L) >= 0)
    {
        moveFront(L);
        while (index(L) >= 0) {
            fprintf(out, "%d ", get(L));
            moveNext(L);
        }
    }
}

/*
 * Prints to the file pointed to by out, a string representation of L consisting
 * of a space separated sequence of integers, with front on left.
 */
void printRevList(FILE* out, List L)
{
    if (length(L) >= 0)
    {
        moveBack(L);
        while (index(L) >= 0) {
            fprintf(out, "%d ", get(L));
            movePrev(L);
        }
    }
}

/*
 * Returns a new List representing the same integer
 * sequence as L. The cursor in the new list is undefined,
 * regardless of the state of the cursor in L. The state
 * of L is unchanged.
 */
List copyList(List L)
{
    if (length(L) == 0) {
        return NULL;
    }

    List new_list = newList();
    moveFront(L);
    while (index(L) >= 0) {
        append(new_list, L->cursor->value);
        moveNext(L);
    }

    return new_list;
}

/*
 * Returns a new List which is the concatenation of
 * A and B. The cursor in the new List is undefined,
 * regardless of the states of the cursors in A and B.
 * The states of A and B are unchanged.
 */
List concatList(List A, List B)
{

 return B;
}