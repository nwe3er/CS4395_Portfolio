import collections
import copy
import math
import random
import sys


# Node class to model the nodes from the decision tree
class Node:
    def __init__(self, attribute=None, attributeVal=None, label=None,
                 attributeParent=None, attributeParentVal=None):
        if attributeVal is None:
            attributeVal = []
        self.child = {}
        self.attributeParent = attributeParent
        self.attributeParentVal = attributeParentVal
        self.attribute = attribute
        self.attributeVal = attributeVal
        self.label = label


def countClasses(data):
    """
    This function returns a map of the class counts in a data
    """

    # The key is the class and the value is the number of examples of that class in the data
    countClass = collections.defaultdict(int)

    for ex in data:
        countClass[ex["class"]] = countClass[ex["class"]] + 1

    return countClass


def entropyPriority(data):
    """
    calculates the entropy of a data before to splitting
    """
    # The key is the class and the value is the number of examples of that class in the data
    countClass = countClasses(data)

    if len(countClass) != 1:
        entro = 0
        examNum = sum(countClass.values())

        for counter in countClass.values():
            # 0 * log_2(0) = 0
            if counter == 0:
                continue
            entro = entro - (counter / examNum) * math.log2(counter / examNum)

        return entro

    # everything is in the same class -> entropy = 0
    return 0


def entropy(data, attribute, attributeVal):
    """
    calculates the entropy of a data with the provided value for a specific
    attribute
    """
    countClass = collections.defaultdict(int)

    for ex in data:
        if ex[attribute] == attributeVal:
            countClass[ex["class"]] = countClass[ex["class"]] + 1

    if len(countClass) == 1:
        return 0

    entro = 0
    examNum = sum(countClass.values())

    for counter in countClass.values():
        if counter == 0:
            continue
        entro = entro - (counter / examNum) * math.log2(counter / examNum)

    return entro


def IG(data, attribute):
    """
    calculates the IG after splitting the data on the provided attribute
    """
    # The key is the class and the value is the number of examples of that class in the data
    attributeValCount = collections.defaultdict(int)

    for ex in data:
        attributeValCount[ex[attribute]] = attributeValCount[ex[attribute]] + 1

    ig = entropyPriority(data)
    exNum = sum(attributeValCount.values())

    for attributeVal, count in attributeValCount.items():
        ig = ig - (count / exNum) * entropy(data, attribute, attributeVal)

    return ig


def highIGAttr(data, remainingAttr):
    """
    returns the attribute with the highest information gain,
    breaking ties by choosing the earliest one
    """
    attrChoice = None
    gainingMax = -float("inf")

    attributes = remainingAttr

    for attribute in attributes:
        gain = IG(data, attribute)
        if gain > gainingMax:
            gainingMax = gain
            attrChoice = attribute

    return attrChoice


def mostComClass(dataset):
    """
    returns the most common class in the data,
    breaking ties by choosing class 0 -> class 1 -> class 2
    """
    classCount = countClasses(dataset)

    return max(sorted(classCount), key=classCount.get)


def sameClass(data):
    """
    returns true if all examples belong to the same class
    """
    classVal = set()

    for ex in data:
        classVal.add(ex["class"])

    return len(classVal) == 1


def getEntireAttrValues(data):
    """
    returns maps of all values of all attributes in a data
    """
    attributes = list(data[0].keys())[:-1]
    attributeVal = collections.defaultdict(set)

    for ex in data:
        for attribute in attributes:
            attributeVal[attribute].add(ex[attribute])

    return attributeVal


def isLeafNode(data, attribute):
    """
    determines whether a dataset is a leaf node
    """
    # leaf node, nothing left
    if len(data) == 0:
        return 1

    # leaf node, all examples are tied to the same class
    if sameClass(data):
        return 2

    # leaf node, examples are tied to multiple classes
    # in this case,
    if len(attribute) == 0:
        countClass = countClasses(data)
        # now we want to see if there is tie for most frequent class
        if len(set(countClass.values())) != 1:
            return 3
        else:
            return 4
    else:
        return 0


def id3Algorithm(data, label, attributeVal, attribute, classCount):
    """
    implementation of the id3 algorithm
    :param data: a list of maps, where each maps is an example in the data
    :param label: most common class in the beginning data
    :param attributeVal: list of values that an attribute in the data can handle
    :param attribute: list of attributes that we haven't split on
    :param classCount: count of examples of each class in the data
    :return: a decision tree
    """
    # base case -> leaf node
    # apply the tie breaking rules
    leafType = isLeafNode(data, attribute)
    if leafType:
        # no examples left, choose class that is most used in train set
        if leafType == 1:
            return Node(label=label)

        # attributes left or all examples tie to same class
        elif leafType == 2 or leafType == 3:
            return Node(label=mostComClass(data))

        # tie for most used class, chooses most used node
        else:
            # count of class values in the dataset and the whole training set
            counts1 = countClasses(data)
            countClass = classCount

            # key -> class values in subset, value -> their counts in the entire dataset
            count2 = collections.defaultdict(int)

            for classValue in counts1:
                count2[classValue] = countClass[classValue]

            return Node(label=max(sorted(count2), key=count2.get))

    else:
        # find the attribute with the highest IG
        maxIGAttribute = highIGAttr(data, attribute)

        # remove the highest IG attribute
        attribute = copy.deepcopy(attribute)
        attribute.remove(maxIGAttribute)

        # make decision tree
        attributeValues = [attrVal for attrVal in attributeVal[maxIGAttribute]]
        dtree = Node(attribute=maxIGAttribute,
                     attributeVal=attributeValues,
                     label=mostComClass(data))

        # split the dataset on the highest IG attribute
        for attrValue in dtree.attributeVal:
            split = [example for example in data if attrValue == example[maxIGAttribute]]

            # recursively create subtrees and link them with the tree
            subtree = id3Algorithm(split, label, attributeVal, attribute, classCount)
            subtree.attributeParent = maxIGAttribute
            subtree.attributeParentVal = attrValue
            dtree.child[attrValue] = subtree

        return dtree


def showTree(tree):
    """
    prints the decision tree to screen output
    """
    stack = [(tree, 0)]
    while stack:
        node, depth = stack.pop()
        # skip the root node
        if node.attributeParent:
            parent = node.attributeParent
            val = str(node.attributeParentVal)
            label = str(node.label)
            # is it possible to use str.format() for repeated symbols
            line = (depth - 1) * "| " + parent + " = " + val + " : "

            # non-leaf
            if node.child:
                print(line.lstrip())

            # leaf node
            else:
                line += label + " "
                print(line.lstrip())

        for childNode in list(node.child.values())[::-1]:
            stack.append((childNode, depth + 1))


def treePrediction(tree, example):
    """
    returns the tree's prediction
    """
    stack = [tree]
    while stack:
        node = stack.pop()

        # leaf node, return its label
        if not node.child:
            return node.label

        # get the attribute of the current node, and the example's mapping value
        attributeValue = example[node.attribute]

        # go down the branch mapping to this attribute value
        if attributeValue in node.child:
            stack.append(node.child[attributeValue])


def accuracy(tree, data):
    """
    returns the accuracy of the decision tree on the data
    """
    correct = 0

    for ex in data:
        if treePrediction(tree, ex) == ex["class"]:
            correct = correct + 1

    return correct / len(data)


def main():
    # arguments passed
    path1 = sys.argv[1]
    path2 = sys.argv[2]

    # read the training and test data
    with open(path1) as l:
        # assign training data and skip lines
        trainingData = [line.split() for line in l if line.strip()]

    # remove the first line from the training data
    attributes = trainingData.pop(0)

    # make the attributes map to each line in the training data
    trainingData = [dict(zip(attributes, list(map(int, example)))) for example in trainingData]

    # complete the same task for the test data done above for the training data to make data usable
    with open(path2) as l:
        testData = [line.split() for line in l if line.strip()]

    testData.pop(0)
    testData = [dict(zip(attributes, list(map(int, example)))) for example in testData]

    # Task A
    data = trainingData
    label = mostComClass(trainingData)
    attributeVal = getEntireAttrValues(trainingData)
    attribute = attributes[:-1]
    countClass = countClasses(trainingData)
    decision_tree = id3Algorithm(data, label, attributeVal, attribute, countClass)
    showTree(decision_tree)

    # Task B
    trainAccuracy = accuracy(decision_tree, trainingData)
    print("\nAccuracy on training set ({} instances): {}%".format(len(trainingData), round(100 * trainAccuracy, 2)))

    # Task C
    testAccuracy = accuracy(decision_tree, testData)
    print("\nAccuracy on test set ({} instances): {}%".format(len(testData), round(100 * testAccuracy, 2)))

    # task D ->>>>> The graph will be on the README.md file.

    # train_set_sizes = list(range(100, 900, 100))
    # results = collections.defaultdict(float)
    #
    # for size in train_set_sizes:
    #     random.shuffle(trainingData)
    #     decision_tree = id3Algorithm(trainingData[:size], label, attributeVal,
    #                                  attribute, countClass)
    #     results[size] = accuracy(decision_tree, testData)
    #
    # print("\n")
    # for train_set_size, acc in results.items():
    #     print("Training set size = {}, Accuracy on test set = {}".format(train_set_size, acc))


if __name__ == "__main__":
    main()
