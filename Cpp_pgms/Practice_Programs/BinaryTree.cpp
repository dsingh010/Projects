#include "BinaryTree.h"

void BinaryTree::insert(int data) {
    root = insertRecursive(root, data);
}

TreeNode* BinaryTree::insertRecursive(TreeNode* current, int data) {
    if (!current) {
        return new TreeNode(data);
    }

    if (data < current->data) {
        current->left = insertRecursive(current->left, data);
    } else if (data > current->data) {
        current->right = insertRecursive(current->right, data);
    }

    return current;
}

void BinaryTree::inorderTraversal(TreeNode* current) {
    if (current) {
        inorderTraversal(current->left);
        std::cout << current->data << " ";
        inorderTraversal(current->right);
    }
}

void BinaryTree::display() {
    inorderTraversal(root);
    std::cout << std::endl;
}


void BinaryTree::destroyTree(TreeNode* current) {
    if (current) {
        destroyTree(current->left);
        destroyTree(current->right);
        delete current;
    }
}

int main() {
    BinaryTree binaryTree;
    binaryTree.insert(20);
    binaryTree.insert(10);
    binaryTree.insert(30);
    binaryTree.insert(5);
    binaryTree.insert(15);

    binaryTree.display();

    return 0;
}