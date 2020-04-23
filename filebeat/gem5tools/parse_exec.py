#!/usr/bin/env python2
# encoding: utf-8

import os
import re
from anytree import Node,RenderTree,NodeMixin,PostOrderIter

class ExecAll:
    def __init__(self, id, name, parent, size):
        self.id = id
        self.name = name
        self.parent = parent
        self.size = size

def write_ExecRelation(path_ExecAllFilebeat, final_list):
    with open(path_ExecAllFilebeat, 'w+') as f:
        for i in final_list:
            f.write(str(i.id)+' '+i.name+' '+str(i.parent)+' '+str(i.size)+'\n')

def add_size(exec_list):
    for i in exec_list:
        i.size = i.size + 1

def parse_ExecAll(path_ExecAll):
    with open(path_ExecAll, "r") as f:
        id = 1
        final_list = []
        exec_list = []
        pre_ins = ""
        while(True):
            line  = f.readline()
            if (line):
                line_split = re.split('\s*:\s*', line, maxsplit=4)
                if (len(line_split) >= 4):
                    if (line_split[3].find('+') != -1):
                        index = line_split[3].find('+')
                    elif (line_split[3].find('.') != -1):
                        index = line_split[3].find('.')
                    else:
                        index = len(line_split[3])
                    name = line_split[3][0:index]

                    if (len(exec_list) == 0):
                        exec_list.append(ExecAll(id, name, 0, 0))
                        add_size(exec_list)
                        id = id + 1
                    elif (name == exec_list[len(exec_list)-1].name):
                        add_size(exec_list)
                    else:
                        if (pre_ins.find("RET_") != -1):
                            final_list.append(exec_list.pop())
                            add_size(exec_list)
                        elif (pre_ins.find("CALL_") != -1):
                            exec_list.append(ExecAll(id, name, exec_list[len(exec_list)-1].id, 0))
                            add_size(exec_list)
                            id = id + 1
                        elif (pre_ins.find("JMP_") != -1):
                            parent = exec_list[len(exec_list)-1].parent
                            final_list.append(exec_list.pop())
                            exec_list.append(ExecAll(id, name, parent, 0))
                            add_size(exec_list)
                            id = id + 1

                    pre_ins = line_split[4]
                else:
                    continue
            else:
                break
        for i in exec_list:
            final_list.append(i)
        return final_list

#-------------------------------------------- tree -------------------------------------------------
class ExecAllTree(NodeMixin):
    def __init__(self, id, name, size, parent=None, children=None):
        self.id = id
        self.name = name
        self.parent = parent
        self.size = size
        if children:
            self.children = children

def print_exec_list2tree(final_list):
    nodes = {}
    sorted_list = sorted(final_list, key=lambda func: func.id)
    for i in sorted_list:
        if (i.parent == 0):
            nodes[i.id] = Node(i.id)
        else:
            nodes[i.id] = Node(i.id, parent=nodes[i.parent])
    for pre,fill,node in RenderTree(nodes[1]):
        print '%s%s' % (pre, node.name)

def print_exec_tree(root):
    for pre,fill,node in RenderTree(root):
        treestr = u"%s%s" % (pre, node.name)
        print treestr.ljust(8),node.size

def exec_list2tree(final_tree_list):
    nodes = {}
    sorted_list = sorted(final_list, key=lambda func: func.id)
    for i in sorted_list:
        if (i.parent == 0):
            nodes[i.id] = ExecAllTree(i.id, i.name, i.size)
        else:
            nodes[i.id] = ExecAllTree(i.id, i.name, i.size, parent=nodes[i.parent])
    return nodes[1]

def line_path_stack_flame(path_list):
    line_path = ''
    for i in path_list:
        line_path = line_path + i.name + ','
    return line_path

def shrink_stack_flame(path_list, size):
    for i in path_list:
        i.size = i.size - size

def make_stack_flame(path_list, path_dict):
    line_path = line_path_stack_flame(path_list)
    size = path_list[len(path_list)-1].size
    path_list.pop()
    shrink_stack_flame(path_list, size)
    if line_path in path_dict:
        path_dict[line_path] = path_dict[line_path] + size
    else:
        path_dict[line_path] = size

def print_stack_flame(path_dict):
    for key,value in path_dict.items():
        print key+'  '+str(value)

def exec_tree2flame(root, path_list, path_dict):
    for node in root.children:
        path_list.append(node)
        if (node.children):
            exec_tree2flame(node, path_list, path_dict)
            make_stack_flame(path_list, path_dict)
        else:
            make_stack_flame(path_list, path_dict)


# -----------------------------------------------------

def write_ExecBar(path_ExecBar, path_dict):
    with open(path_ExecBar, 'w+') as f:
        id = 1
        for key,value in path_dict.items():
            for i in range(value):
                line = str(id)
                id = id + 1
                num = len(key.split(','))
                line = line + ' ' + str(num) + '\n'
                f.write(line)


if __name__ == "__main__":
    gem5_path = os.getenv('GEM5_PATH')
    if (gem5_path):
        path_ExecAll = os.path.join(gem5_path, "m5out/ExecAll.txt")
        final_list = parse_ExecAll(path_ExecAll)
        path_ExecRelation = os.path.join(gem5_path, "m5out/ExecRelation.txt")
        write_ExecRelation(path_ExecRelation, final_list)

        #print_exec_list2tree(final_list)
        root = exec_list2tree(final_list)
        #print_exec_tree(root)
        path_dict = {}
        path_list = []
        exec_tree2flame(root, path_list, path_dict)
        #print_stack_flame(path_dict)

        path_ExecBar = os.path.join(gem5_path, "m5out/ExecBar.txt")
        write_ExecBar(path_ExecBar, path_dict)

    else:
        print "The GEM5_PATH is not set. Can not create ExecAllFilebeat.txt"
