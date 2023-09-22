#include "List.h"

/* Returns the number of elements in L. */
int List::length() const
{
    return list_length;
}

/* Returns index of cursor element if defined, -1 otherwise. */
int List::index() const
{
    if (cursor == nullptr) {
        return -1;
    }
    return cursor->index;
}

/* Returns front element of L. Pre: length()>0 */
int List::front()
{
    if (length() > 0) {
        return head->index;
    }
    return -1;
}

/* Returns back element of L. Pre: length()>0 */
int List::back()
{
    if (length() > 0) {
        return tail->index;
    }
    return -1;
}

/*
 * Returns true iff Lists A and B are in same state, and returns
 * false otherwise.
 */
bool List::equals(const List& B)
{
    if (length() != B.length()) {
        return false;
    }

    while (cursor != nullptr && B.get_cursor()) {
        if (cursor->index != B.get_cursor()->index) {
            return false;
        }
    }
    return true;
}

/* Resets L to its original empty state. */
void List::clear()
{
    cursor = head;
}

/* Resets L to its original empty state. */
void List::set_back()
{
    cursor = tail;
}

/*
 * Overwrites the cursor element’s data with x Pre: length()>0, index()>=0
 */
void List::set(int x)
{
    if (length() > 0) {
        cursor->index = x;
    }
}

/*
 * If L is non-empty, sets cursor under the front element, otherwise does nothing.
 */
void List::moveFront()
{
    if (length() > 0) {
        cursor = head;
    }
}

/*
 * If L is non-empty, sets cursor under the back element, otherwise does nothing.
 */
void List::moveBack()
{
    if (length() > 0) {
        cursor = tail;
    }
}

/*
 * If cursor is defined and not at front, move cursor one
 * step toward the front of L; if cursor is defined and at
 * front, cursor becomes undefined; if cursor is undefined
 * do nothing
 */
void List::movePrev()
{
    if (cursor != nullptr) {
        if (cursor == head) {
            cursor = nullptr;
        } else {
            cursor = cursor->back;
        }
    }
}

/*
 * If cursor is defined and not at back, move cursor one
 * step toward the back of L; if cursor is defined and at
 * back, cursor becomes undefined; if cursor is undefined
 * do nothing
 */
void List::moveNext()
{
    if (cursor != nullptr) {
        if (cursor == tail) {
            cursor = nullptr;
        } else {
            cursor = cursor->front;
        }
    }
}

/*
 * Insert new element into L. If L is non-empty, insertion takes place
 * before front element.
 */
void List::prepend(int x)
{
    Node* tmp_node = new Node(x);
    if (length() > 0) {
        tmp_node->back = nullptr;
        tmp_node->front = head;
        head->back = tmp_node;
        head = tmp_node;
        cursor = head;
    } else {
        head = tmp_node;
        tail = tmp_node;
        cursor = tmp_node;
        head->front = nullptr;
        head->back = nullptr;
        tail->front = nullptr;
        tail->back = nullptr;
    }
    list_length++;
}

/*
 * Insert new element into L. If L is non-empty, insertion takes place
 * after back element.
 */
void List::append(int x)
{
    Node* tmp_node = new Node(x);
    if (length() > 0) {
        tmp_node->front = nullptr;
        tmp_node->back = tail;
        tail->front = tmp_node;
        tail = tmp_node;
        cursor = tail;
    } else {
        head = tmp_node;
        tail = tmp_node;
        cursor = tmp_node;
        head->front = nullptr;
        head->back = nullptr;
        tail->front = nullptr;
        tail->back = nullptr;
    }
    list_length++;
}

/*
 * Insert new element before cursor. Pre: length()>0, index()>=0
 */
void List::insertBefore(int x)
{
    if (cursor == head) {
        prepend(x);
    } else {
        Node* tmp_node = new Node(x);
        Node* front_node = cursor->front;

        front_node->back = tmp_node;
        tmp_node->front = cursor;
        tmp_node->back = front_node;
        cursor->front= tmp_node;
        list_length++;
    }
}

/* Insert new element after cursor.Pre: length()>0, index()>=0 */
void List::insertAfter(int x)
{
    if (cursor == tail) {
        append(x);
    } else {
        Node* tmp_node = new Node(x);
        Node* back_node = cursor->back;

        back_node->front = tmp_node;
        tmp_node->front = cursor;
        tmp_node->back = back_node;
        cursor->back = tmp_node;
        list_length++;
    }
}

/* Delete the front element. Pre: length()>0 */
void List::deleteFront()
{
    if (length() > 0) {
        Node* tmp_node = head;
        if (length() == 1) {
            head->front = nullptr;
            head->back = nullptr;
            tail->front = nullptr;
            tail->back = nullptr;
        } else {
            Node* front_node = head->front;
            front_node->back = nullptr;
            head = front_node;
        }
        delete tmp_node;
    }
}

/* Delete the back element. Pre: length()>0 */
void List::deleteBack()
{
    if (length() > 0) {
        Node* tmp_node = tail;
        if (length() == 1) {
           head->front = nullptr;
           head->back = nullptr;
           tail->front = nullptr;
           tail->back = nullptr;
        } else {
            Node* back_node = tail->back;
            back_node->back = nullptr;
            tail = back_node;
        }
        delete tmp_node;
        list_length--;
    }
}

/*
 * Delete cursor element, making cursor undefined. Pre: length()>0, index()>=0
 */
void List::delete_list()
{
    while (list_length > 0) {
        deleteBack();
    }
}

/*
 * Prints to the file pointed to by out, a string representation of L consisting
 * of a space separated sequence of integers, with front on left.
 */
void List::printList()
{
    clear();
    for (int i = 0; i < length(); i++) {
        cout << index() << endl;
        moveNext();
    }
}

/*
 * Prints to the file pointed to by out, a string representation of L consisting
 * of a space separated sequence of integers, with front on left.
 */
void List::printRevList()
{
    if (length())
    {
        set_back();
        for (int i = length(); i > 0; i--) {
            cout << index() << endl;
            movePrev();
        }
    }
}

/*
 * Returns a new List representing the same integer
 * sequence as L. The cursor in the new list is undefined,
 * regardless of the state of the cursor in L. The state
 * of L is unchanged.
 */
List List::copyList()
{
    List new_list;

    clear(); //clear the cursor
    while (cursor != tail) {
        new_list.append(cursor->index);
        cout << cursor->index << endl;
        moveNext();
    }

    return new_list;
}

/*
 * Returns a new List which is the concatenation of
 * A and B. The cursor in the new List is undefined,
 * regardless of the states of the cursors in A and B.
 * The states of A and B are unchanged.
 */
List List::concatList(List B)
{

 return B;
}