#include <iostream>

class TreeNode {
public:
    int data;
    TreeNode* left;
    TreeNode* right;

    TreeNode(int data) {
        this->data = data;
        this->left = nullptr;
        this->right = nullptr;
    }
};

class BinaryTree {
private:
    TreeNode* root;

public:
    BinaryTree() {
        root = nullptr;
    }

    void insert(int data);

    TreeNode* insertRecursive(TreeNode* current, int data);
    void inorderTraversal(TreeNode* current);

    void display();

    // Destructor to free memory
    ~BinaryTree() {
        destroyTree(root);
    }

    void destroyTree(TreeNode* current);
};


