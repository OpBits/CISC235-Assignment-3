#Author: Alexander Nechyporenko

import os

class AVLNode(object):
    def __init__(self, key, val = None):
        self.key = key
        if val is None:
            self.val = []
        else:
            self.val = val
        self.left = None
        self.right = None
        
class AVLTreeMap(object):
    def __init__(self):
        self.node = None
        self.height = 1
        self.balance = 0

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
 
    def setHeight(self):
        if self.node:
            if self.node.left:
                self.node.left.setHeight()
            if self.node.right:
                self.node.right.setHeight()
            self.height = 1 + max(self.node.left.height, self.node.right.height)
        else:
            self.height = 1

    def setBalances(self):
        if self.node:
            if self.node.left:
                self.node.left.setBalances()
            if self.node.right:
                self.node.right.setBalances()
            self.balance = self.node.left.height  - self.node.right.height
        else:
            self.balance = 0
    
    def leftRotate(self):
        root = self.node.right.node
        leftSubT = root.left.node
        oldRoot = self.node

        self.node = root
        oldRoot.right.node = leftSubT
        root.left.node = oldRoot
        
    def rightRotate(self):
        root = self.node.left.node
        leftSubT = root.right.node
        oldRoot = self.node

        self.node = root
        oldRoot.left.node = leftSubT
        root.right.node = oldRoot

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
    def printTree(self):
        if self.node is None:
            return
        if self.node.left:
            self.node.left.printTree()
        print("key :", self.node.key, ", val: ", self.node.val)
        if self.node.right:
            self.node.right.printTree()

class WebPageIndex(object):
    def __init__(self, fileName):
        self.fileName = fileName
        self.contents = self.readFromFile(fileName)
        self.AVLTree = self.createWebIndexTree()

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
    
    def createWebIndexTree(self):
        self.AVLTreeMap = AVLTreeMap()
        webIndex = self.contents

        for i in range(len(webIndex)):
            self.AVLTreeMap.put(webIndex[i], i)
        return self.AVLTreeMap

    def Count(self, word):
        listOfIndices = self.AVLTree
        listOfIndices = listOfIndices.get(word)

        if listOfIndices is None:
            return None
        else:
            return len(listOfIndices)
        
    def getFileName(self):
        return self.fileName
    
class WebpagePriorityQueue(object):
    def __init__(self, query, setOfWebInstances = None):
        self.query = query.lower()
        if setOfWebInstances == None:
            self.maxHeap = []
            self.setOfOriginalInstances = []
        else:
            self.setOfOriginalInstances = setOfWebInstances
            self.maxHeap = self.createMaxHeap(setOfWebInstances, query)

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
        
    def peek(self):
        return self.maxHeap[0]
    
    def poll(self):
        topWebInstance = self.maxHeap[0]
        del (self.maxHeap[0])
        return topWebInstance
        
    def rehash(self, newQuery):
        if self.query != newQuery:
            self.query = newQuery.lower()
            self.maxHeap = self.createMaxHeap(self.setOfOriginalInstances, newQuery)

class ProcessQueries(object):
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
    
    
    
    
    
                
