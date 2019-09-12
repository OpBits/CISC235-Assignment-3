#Author: Alexander Nechyporenko

import os

#This class object is the node that holds the key and the corresponding val list.
#This node also has the attributes to point to the left and right sub children
class AVLNode(object):
    def __init__(self, key, val = None):
        self.key = key
        if val is None:
            self.val = []
        else:
            self.val = val
        self.left = None
        self.right = None

'''
This class represents the AVL tree data structure that contains the key-value pairs.
The map is traversed via the key values, be it strings or integers. Then values can be
added or extracted. The values are in list format, where they can hold strings or integers.
'''
class AVLTreeMap(object):

    #initializing the node attribute of the tree, where the node will point to
    #child nodes from the previous class. Each node also holds the attribute of height
    #and balance. Where height is the height value of each node, and the balance is
    #the height comparison of the child nodes.
    def __init__(self):
        self.node = None
        self.height = 1
        self.balance = 0

    '''
    This function inserts a node with the key value pairing. This functon takes a key and
    val as its parameters, where key can be a string or an int and the val is the value
    to be put into a list. This function essentially creates a node if necessary and then
    has the key and value added to it.
    '''
    def put(self, key, val):
        if self.node is None:
            temp = [val]
            self.node = AVLNode(key,temp)
            self.node.left = AVLTreeMap()
            self.node.right = AVLTreeMap()
        else:
            if key < self.node.key:
                self.node.left.put(key,val)
            elif key > self.node.key:
                self.node.right.put(key, val)
            else:
                newLst = self.node.val
                newLst.append(val)
                leftC = self.node.left
                rightC = self.node.right
                self.node = AVLNode(key,newLst)
                self.node.left = leftC
                self.node.right = rightC
            self.setHeight()
            self.setBalances()

            if self.balance > 1:
                if self.balance < 0:
                    self.node.left.leftRotate()
                self.rightRotate()
                self.setHeight()
            if self.balance < -1:
                if self.balance > 0:
                    self.node.right.rightRotate()
                self.leftRotate()
                self.setHeight()
 
    '''
    This function takes a node and sets the height of this node and all the child nodes.
    If the node is empty, the nodes height is set to the default height.
    '''
    def setHeight(self):
        if self.node:
            if self.node.left:
                self.node.left.setHeight()
            if self.node.right:
                self.node.right.setHeight()
            self.height = 1 + max(self.node.left.height, self.node.right.height)
        else:
            self.height = 1
    '''
    This function works similarily to the set heights fucntion, except that it
    sets the balances for the node itself and all of its child nodes.
    '''
    def setBalances(self):
        if self.node:
            if self.node.left:
                self.node.left.setBalances()
            if self.node.right:
                self.node.right.setBalances()
            self.balance = self.node.left.height  - self.node.right.height
        else:
            self.balance = 0
    
    '''
    This function perfroms the left rotation, where the current root is replaced
    by the right subtree
    '''
    def leftRotate(self):
        root = self.node.right.node
        leftSubT = root.left.node
        oldRoot = self.node

        self.node = root
        oldRoot.right.node = leftSubT
        root.left.node = oldRoot
    '''
    This function perfroms the right rotation, where the current root is replaced
    by the left subtree
    '''
    def rightRotate(self):
        root = self.node.left.node
        leftSubT = root.right.node
        oldRoot = self.node

        self.node = root
        oldRoot.left.node = leftSubT
        root.right.node = oldRoot

    '''
    This function takes the key parameter, and has a preset parameter of keyList,
    which is initialized to an empty list. This function returns a list of all the node
    keys visited when search for a specific key. 
    '''
    def searchPath(self, key, keyList = None):
        if keyList == None:
           keyList = []

        if self.node is None:
            return keyList
        else:
            if key < self.node.key:
                if self.node.left is None:
                    keyList.append(self.node.key)
                    return keyList
                keyList.append(self.node.key)
                return self.node.left.searchPath(key,keyList)
            elif key > self.node.key:
                if self.node.right is None:
                    keyList.append(self.node.key)
                    return keyList
                keyList.append(self.node.key)
                return self.node.right.searchPath(key,keyList)
            else:
                keyList.append(self.node.key)
                return keyList
    '''
    This function has the key as the parameter. If the key exists in the AVL tree, then
    the value corresponding to the key is returned. If the key does not exist, None is
    returned.
    '''
    def get(self, key):
        if self.node is None:
            return None

        if self.node.key == key:
            return self.node.val
        else:
            if self.node.key > key:
                if self.node.left is None:
                    return None
                return self.node.left.get(key)
            elif self.node.key < key:
                if self.node.right is None:
                    return None
                return self.node.right.get(key)

    '''
    Prints the AVl Tree in Order
    '''
    def printTree(self):
        if self.node is None:
            return
        if self.node.left:
            self.node.left.printTree()
        print("key :", self.node.key, ", val: ", self.node.val)
        if self.node.right:
            self.node.right.printTree()

'''
THis class takes a web page(i.e. file) and then converts all the words in the file
into an AVL tree. Each word is a seperate key in the tree and each index position of
the word within the file is the array of indices.
'''
class WebPageIndex(object):
    #This class initializes, by setting the filename attribute. Then sets attribute of
    #contents, which is a list containing all the words within the file.
    #Next, the last attribute is the AVLTree itself that holds all the key-value pairs
    def __init__(self, fileName):
        self.fileName = fileName
        self.contents = self.readFromFile(fileName)
        self.AVLTree = self.createWebIndexTree()

    '''
    This function takes the file name as its parameter. The function then creates a string
    of the entire file and then converts it to a list of words. All the words are made lower
    case and then the list is returned.
    '''
    def readFromFile(self, fileName):
        with open(fileName, 'r+', encoding="utf-8") as file:
            listOfWords = file.read().replace('\n','')
            listOfWords = listOfWords.replace('(', '')
            listOfWords = listOfWords.replace(')', '')
            listOfWords = listOfWords.replace('.', '')
            listOfWords = listOfWords.replace(',', '')

        listOfWords = listOfWords.split(' ')
        
        for i in range(len(listOfWords)):
            listOfWords[i] = listOfWords[i].lower()           
        return listOfWords

    '''
    This function creates the avl tree that contains each word as a key and holds its
    associated value list that contains all the indices where the word can be found
    in the file. The function returns the avltree as an attribute of the class object
    '''
    def createWebIndexTree(self):
        self.AVLTreeMap = AVLTreeMap()
        webIndex = self.contents

        for i in range(len(webIndex)):
            self.AVLTreeMap.put(webIndex[i], i)
        return self.AVLTreeMap

    '''
    This function returns the amount of times the word appears within the web or file
    that is passed through the parameter.
    '''
    def Count(self, word):
        listOfIndices = self.AVLTree
        listOfIndices = listOfIndices.get(word)

        if listOfIndices is None:
            return None
        else:
            return len(listOfIndices)
        
    def getFileName(self):
        return self.fileName
'''
This class object creates a maxheap list that holds lists with two elements. The
first element being the webpageindex instance and the other the priority value.
The priority is the representation of the amount of times the query string shows up
within the webpage. The max heap the sets the highest priority lists to the top, while
the lowest priority to the bottom
'''
class WebpagePriorityQueue(object):
    '''
    Initialize query, where query string is set to lower case. The other parameter
    is the set of all webpageindex instances. I set an attribute to hold all the
    original set webpages, while the other attribute to hold the maxheap itself.
    '''
    def __init__(self, query, setOfWebInstances = None):
        self.query = query.lower()
        if setOfWebInstances == None:
            self.maxHeap = []
            self.setOfOriginalInstances = []
        else:
            self.setOfOriginalInstances = setOfWebInstances
            self.maxHeap = self.createMaxHeap(setOfWebInstances, query)

    '''
    This function takes the set of web instances and the query. Then creates the max
    heap which is then returned by the function.
    '''
    def createMaxHeap(self, setOfWebInstances, query):
        tempList = []
        maxHeap = []
        querySplit = query.split()
        
        for i in range(len(setOfWebInstances)):
            wordCount = 0
            heapElement = [None]*2
            for j in range(len(querySplit)):
                tempCount = setOfWebInstances[i].Count(querySplit[j])
                if tempCount is None:
                    tempCount = 0
                wordCount += tempCount
            
            heapElement[0] = setOfWebInstances[i]
            heapElement[1] = wordCount            
            tempList.append(heapElement)

        HighElement = tempList[0]
        index = 0

        while len(tempList) > 0:
            if tempList[index][1] > HighElement[1]:
                HighElement = tempList[index]
            index +=1
            if index == len(tempList):
                maxHeap.append(HighElement)
                tempList.remove(HighElement)
                if tempList:
                    HighElement = tempList[0]
                index = 0
        
        return maxHeap
        
    #This function takes no parameters. Only returns the top element of the max heap,
    #which contains both the webpage instance and the priority number
    def peek(self):
        return self.maxHeap[0]
        
    #This function does the same as above, except it removes the top element of the max
    #heap as well
    def poll(self):
        topWebInstance = self.maxHeap[0]
        del (self.maxHeap[0])
        return topWebInstance
        
    '''
    This function takes a new query as a parameter and then rehashes the list
    with the same set of webpage instances except re-prioritizes it based on the
    new query.
    '''
    def rehash(self, newQuery):
        if self.query != newQuery:
            self.query = newQuery.lower()
            self.maxHeap = self.createMaxHeap(self.setOfOriginalInstances, newQuery)

'''
Process queries is a class object that takes a folder of files that represent
webpages. We then go through a list of queries and create the max heaps for the
corresponding queries and webpages. This class' function then prints all the relevant
pages corresponding to the query
'''
class ProcessQueries(object):
    '''
    First attribute is the specified limit, which is an int that determines
    the amount of webpages to show at maximum. The next attribute creates a list
    of all the webpage file names in webpageIndexList. The attribute webpageInstances
    is the webpageIndex instances of all the files. Next attribute is the list
    of all the queries from the queries text file. Last attribute is the
    empty priority queue attribute that will be used to instantiate the
    priority queue class.
    '''
    def __init__(self, folderName, queryFileName, specifiedLimit = None):
        if specifiedLimit == None:
            self.specifiedLimit = None
        else:
            self.specifiedLimit = specifiedLimit
        self.webpageIndexList = self.webpageListGenerator(folderName)
        self.webpageInstances = self.createWebPageInstances(self.webpageIndexList, folderName)
        self.queryList = self.createQueryList(queryFileName)
        self.webPagePriorityQueue = None

    #Returns a list of all the files in the folder
    def webpageListGenerator(self, folderName):
        listOfFileNames = os.listdir(folderName)
        return listOfFileNames
        
    #Takes the list of files and then creates the webpage index instances of them.
    #It returns the webpage index instances.
    def createWebPageInstances(self, webpageIndexList, folderName):
        webPageInstances = []
        for i in range(len(webpageIndexList)):
            webpageName = folderName + '/' + webpageIndexList[i]
            tempInstance = WebPageIndex(webpageName)
            webPageInstances.append(tempInstance)
        return webPageInstances

    #This function takes the query file name and then returns the list of strings
    #found in each line
    def createQueryList(self, queryFileName):
        queryList = []
        with open(queryFileName, 'r+', encoding="utf-8") as file:
            for line in file:
                temp = line
                temp = temp.replace('\n', '')
                queryList.append(temp)
        return queryList        

    '''
    This is the main process that prints all the file names or webpages that are relevant
    '''
    def mainProcess(self):
        for i in range(len(self.queryList)):
            if i == 0:
                print("\n______The top search results for " +  self.queryList[i] + "______\n")
                self.webPagePriorityQueue = WebpagePriorityQueue(self.queryList[i],self.webpageInstances)
                
                if self.specifiedLimit is None:
                    while (True):
                        topWebpageInstance = self.webPagePriorityQueue.poll()
                        if topWebpageInstance[1] == 0:
                           break
                        print(topWebpageInstance[0].getFileName())
                else:
                    for i in range(self.specifiedLimit):
                        topWebpageInstance = self.webPagePriorityQueue.poll()
                        if topWebpageInstance[1] == 0:
                           break
                        print(topWebpageInstance[0].getFileName())
            else:
                print("\n______The top search results for " +  self.queryList[i] + "______\n")
                self.webPagePriorityQueue.rehash(self.queryList[i])
                if self.specifiedLimit is None:
                    while (True):
                        topWebpageInstance = self.webPagePriorityQueue.poll()
                        if topWebpageInstance[1] == 0:
                           break
                        print(topWebpageInstance[0].getFileName())
                else:
                    for i in range(self.specifiedLimit):
                        topWebpageInstance = self.webPagePriorityQueue.poll()
                        if topWebpageInstance[1] == 0:
                           break
                        print(topWebpageInstance[0].getFileName())
                
#Here is some test code for each section to illustrate code functionality.
if __name__ == "__main__":
    print("________________Section 1.2________________")
    tree = AVLTreeMap()
    tree.put(15,"bob")
    tree.put(20,"anna")
    tree.put(24, "tom")
    tree.put(10, "david")
    tree.put(13, "david")
    tree.put(7, "ben")
    tree.put(30,"karen")
    tree.put(36, "erin")
    tree.put(25, "david")
    tree.put(13, "nancy")
    print("\nprinting values from AVL Tree that were inserted")
    tree.printTree()

    print("\nList of keys when searching for a specific key")
    print(tree.searchPath(36))
    print(tree.searchPath(20))
    print(tree.searchPath(1))
    print(tree.searchPath(50))
    print(tree.searchPath(14))

    print("\nRetreiving values from AVL tree if they exist")
    print(tree.get(13))
    print(tree.get(1))
    print(tree.get(50))
    print(tree.get(25))

    print("\n________________Section 1.3________________")
    webIndex = WebPageIndex("doc1-arraylist.txt")
    webIndexTree = webIndex.createWebIndexTree()
    
    print("Count of words from doc1")
    print(webIndex.Count('the'))
    print(webIndex.Count('hello'))
    print(webIndex.Count('at'))

    webIndex2 = WebPageIndex("doc2-binarytree.txt")
    webIndexTree = webIndex2.createWebIndexTree()
    
    print("Count of words from doc2")
    print(webIndex2.Count('the'))
    print(webIndex2.Count('nodes'))
    print(webIndex2.Count('at'))
    
    print("\n________________Section 1.4________________")
    webIndex3 = WebPageIndex("doc3-binarysearchtree.txt")
    webIndex4 = WebPageIndex("doc4-stack.txt")
    webIndex5 = WebPageIndex("doc5-queue.txt")
    webIndex6 = WebPageIndex("doc6-AVLtree.txt")

    listOfWeb = [webIndex,webIndex2,webIndex3,webIndex4,webIndex5,webIndex6]

    maxHeap = WebpagePriorityQueue("binary tree", listOfWeb)
    print(maxHeap.peek())
    print(maxHeap.poll())

    maxHeap.rehash("search")
    print(maxHeap.peek())

    print("\n________________Section 1.5________________")
    noLimitQueries = ProcessQueries("cisc235Folder","queries.txt")
    noLimitQueries.mainProcess()
    limitQueries = ProcessQueries("cisc235Folder","queries.txt", 2)
    print("\n_________________Limited Search Alternative_________________\n")
    limitQueries.mainProcess()
    
    
    
    
    
                
