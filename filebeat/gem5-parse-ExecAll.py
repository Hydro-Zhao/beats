#!/usr/bin/env python2
# encoding: utf-8

import os
import re

class ExecAll:
    def __init__(self, id, name, parent, size):
        self.id = id
        self.name = name
        self.parent = parent
        self.size = size

def write_ExecAllFilebeat(path_ExecAllFilebeat, final_list):
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
                    pre_ins = line_split[4]
                    if (len(exec_list) == 0):
                        if (line_split[3].find('+') != -1 or line_split[3].find('.') != -1):
                            index = max(line_split[3].find('+'),line_split[3].find('.'))
                        else:
                            index = len(line_split[3])
                        name = line_split[3][0:index]
                        exec_list.append(ExecAll(id, name, 0, 0))
                        add_size(exec_list)
                        id = id + 1
                    elif (line_split[3].find(exec_list[len(exec_list)-1].name) == 0):
                        add_size(exec_list)
                    else:
                        if (len(exec_list) == 1):
                            if (pre_ins.find("JMP_") == -1):
                                if (line_split[3].find('+') != -1 or line_split[3].find('.') != -1):
                                    index = max(line_split[3].find('+'),line_split[3].find('.'))
                                else:
                                    index = len(line_split[3])
                                name = line_split[3][0:index]
                                exec_list.append(ExecAll(id, name, exec_list[0].id, 0))
                                add_size(exec_list)
                                id = id + 1
                            else:
                                final_list.append(exec_list.pop())
                        elif (line_split[3].find(exec_list[len(exec_list)-2].name) == 0):
                            if (pre_ins.find("JMP_") == -1):
                                final_list.append(exec_list.pop())
                                add_size(exec_list)
                            else:
                                final_list.append(exec_list.pop())
                        else:
                            if (pre_ins.find("JMP_") == -1):
                                if (line_split[3].find('+') != -1 or line_split[3].find('.') != -1):
                                    index = max(line_split[3].find('+'),line_split[3].find('.'))
                                else:
                                    index = len(line_split[3])
                                name = line_split[3][0:index]
                                exec_list.append(ExecAll(id, name, exec_list[len(exec_list)-1].id, 0))
                                add_size(exec_list)
                                id = id + 1
                            else:
                                final_list.append(exec_list.pop())
                else:
                    continue
            else:
                break
        for i in exec_list:
            final_list.append(i)
        #final_list.append(exec_list.pop())
        return final_list

if __name__ == "__main__":
    gem5_path = os.getenv('GEM5_PATH')
    if (gem5_path):
        path_ExecAll = os.path.join(gem5_path, "m5out/ExecAll.txt")
        final_list = parse_ExecAll(path_ExecAll)
        path_ExecAllFilebeat = os.path.join(gem5_path, "m5out/ExecAllFilebeat.txt")
        write_ExecAllFilebeat(path_ExecAllFilebeat, final_list)
    else:
        print "The GEM5_PATH is not set. Can not create ExecAllFilebeat.txt"
