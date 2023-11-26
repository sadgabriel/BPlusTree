import time


MAX_SIZE = 32


class Node:
    def __init__(self):
        pass
    

class InternalNode(Node):
    def __init__(self, parent = None, children = list(), keys = list()):
        self.parent = parent
        self.children = children
        self.keys = keys
    
    def search(self, key):
        i = 0
        for k in self.keys:
            if key < k:
                break
            i += 1
        return i
    
    def split(self):
        if self.parent:
            new_node = InternalNode(parent=self.parent, children=self.children[MAX_SIZE//2:], keys=self.keys[MAX_SIZE//2:])
            
            self.children = self.children[:MAX_SIZE//2]
            self.keys = self.keys[:MAX_SIZE//2-1]
            
            pos = self.parent.search(self.keys[0])
            self.parent.keys.insert(pos, new_node.keys[0])
            self.parent.children.insert(pos+1, new_node)
            
            if len(self.parent.keys) >= MAX_SIZE:
                self.parent.split()
        else:
            new_node_l = InternalNode(parent=self, children=self.children[:MAX_SIZE//2], keys=self.keys[:MAX_SIZE//2-1])
            new_node_r = InternalNode(parent=self, children=self.children[MAX_SIZE//2:], keys=self.keys[MAX_SIZE//2:])
            
            self.children = [new_node_l, new_node_r]
            self.keys = [new_node_r.keys[0]]
    
    def reset_key(self, key):
        pos = self.search(key)
        
        if pos != 0 and self.keys[pos-1] >= key:
            self.keys[pos-1] = key
        
        if self.parent:
            self.parent.reset_key(key)
            

class LeafNode(Node):
    def __init__(self, parent = None, next = None, keys = list()):
        self.parent = parent
        self.next = next
        self.keys = keys
        
    def has(self, key):
        return key in self.keys
        
    def insert(self, key):
        if (self.has(key)):
            print(f'Error: the key {key} is already in tree')
            return
        
        self.keys.append(key)
        self.keys.sort()
        
        self.parent.reset_key(key)
                
        if len(self.keys) >= MAX_SIZE:
            self.split()
    
    
    def split(self):
        new_node = LeafNode(parent=self.parent, next=self.next, keys=self.keys[MAX_SIZE//2:])
        
        self.next = new_node
        self.keys = self.keys[:MAX_SIZE//2]
        
        pos = self.parent.search(self.keys[0])
        self.parent.keys.insert(pos, new_node.keys[0])
        self.parent.children.insert(pos+1, new_node)
        
        if len(self.parent.keys) >= MAX_SIZE:
            self.parent.split()
        
        
class BPlusTree:
    def __init__(self):
        self.root = InternalNode()
        self.root.children = [LeafNode(self.root)]
        
    def search(self, key):
        leaf = self.root
        
        while (isinstance(leaf, InternalNode)):
            pos = leaf.search(key)
            leaf = leaf.children[pos]
        
        return leaf
        
    def insert(self, key):
        self.search(key).insert(key)
    
    def range(self, begin, end):
        leaf = self.search(begin)
        l = []
        
        while leaf:
            for k in leaf.keys:
                if k < begin:
                    continue
                elif k > end:
                    return l
                else:
                    l.append(k)
            leaf = leaf.next
        
        return l
    
def print_help():
    print('------------')
    print('Vaild Commands')
    print('------------')
    print('insert {filepath}')
    print('range {start key} {end key}')
    print('exit')
    print('------------')
    
if __name__ == '__main__':
    tree = BPlusTree()
    
    print_help()
    
    while True:
        command = input().split()
        
        t = time.time()
        
        if command:
            if command[0] == 'insert' and len(command) == 2:
                with open(command[1], 'r') as f:
                    content = f.read()
                
                for key in map(int, content.split(', ')):
                    tree.insert(key)
                    
                print(f'insert completed: {1000 * (time.time() - t)}ms spent')
            elif command[0] == 'range' and len(command) == 3:
                print(tree.range(int(command[1]), int(command[2])))
                print(f'range completed: {1000 * (time.time() - t)}ms spent')
            elif command[0] == 'exit' and len(command) == 1:
                exit()
            else:
                print_help()
        else:    
            print_help()    