import os
# Read data
def read_sort(path):
    dic = {}
    with open(path) as infile:
        next(infile)
        for line in infile:
            currentline = line.split(",")
            drug_name = currentline[3]
            drug_cost = float(currentline[4].replace('\n',''))
            prescriber_name = currentline[2] + currentline[1]
            if drug_name not in dic:
                dic[drug_name] = [set([prescriber_name]), drug_cost]
            else:
                if prescriber_name not in dic[drug_name][0]:
                    dic[drug_name][0].add(prescriber_name)
                dic[drug_name][1] += drug_cost
    printout = [ [k, len(v[0]), v[1]] for (k,v) in sorted(dic.items(), key=lambda d:d[1][1], reverse = True)]

    return printout

def check_same_cost(printout):
    cost_list = [i[2] for i in printout]
    return len(cost_list) != len (set(cost_list))

def arrange_repeat(printout):
    end = 0
    for i in range(len(printout)):
        total_cost = printout[i][2]

        if (i+1 < len(printout) and total_cost == printout[i+1][2] and i >= end):
            start, end = i, i
            while (end != len(printout) and printout[end][2] == total_cost):
                end += 1
            printout[start:end] = [ k for k in sorted(printout[start:end], key=lambda d:d[0])]
    return printout

def print_text(path, printout):
    if path == None or printout==None:
        print("There is no result to write")
    file  = open(path, 'w')
    file.writelines("drug_name,num_prescriber,total_cost\n")
    for i in range(len(printout)):
        file.writelines(str(printout[i][0]) + ',' + str(printout[i][1]) + ',' + str(printout[i][2]) + '\n')

if __name__ == '__main__':
    master_dir = os.getcwd()
    #master_dir = os.path.abspath(os.path.dirname(os.getcwd()))
    for root, dirs, files in os.walk(master_dir + '/input'):
        input_path_list = [master_dir + '/input/' + filename for filename in files]
        output_path_list = [master_dir + '/output/' + filename for filename in files]

    for i in range(len(input_path_list)):
        printout = read_sort(input_path_list[i])
        if check_same_cost(printout):
            printout = arrange_repeat(printout)
        print_text(output_path_list[i],printout)
            
