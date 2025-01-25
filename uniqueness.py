# How many BPMs does one method have that are unique 

import numpy as np
import pandas as pd
import sys

def similar(module1, module2):
    if "\t" in module1 :
        list1 = module1.split('\t')
        list2= module2.split('\t')
    else :
        list1 = module1.split(' ')
        list2= module2.split(' ')
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    mins = min(len(list1), len(list2))
    return float(intersection) / mins

if __name__ == "__main__":

    # List of bpms
    all_modules = []
    names = []
    
    outfile = sys.argv[len(sys.argv) - 1]

    for i in range(len(sys.argv) - 2) :
    # Fill in the list
        bpms_file = open(sys.argv[i + 1])
        names.append(sys.argv[i + 1])
        modules = []

        for num, bpm in enumerate(bpms_file) :
            if "Module1" in bpm :
                modules.append(bpm.split('Module1\t')[1])
            elif "Module2" in bpm :
                modules.append(bpm.split('Module2\t')[1])
            else :
                modules.append(bpm.split('-- ')[1])

            # Make it bpms
            if num % 2 == 1 :
                if '\t' in modules[0] :
                    modules[len(modules) - 2] = modules[len(modules) - 2].rstrip() + '\t' + modules[len(modules) - 1]
                    modules.pop()
                else :
                    modules[len(modules) - 2] = modules[len(modules) - 2].rstrip() + ' ' + modules[len(modules) - 1]
                    modules.pop()



        all_modules.append(modules)

   # print(all_modules[0])

    df = pd.DataFrame(names, columns = ['Filename'])
    df.set_index('Filename', inplace=True)
    df['0.1'] = np.nan
    df['0.2'] = np.nan
    df['0.3'] = np.nan
    df['0.4'] = np.nan
    df['0.5'] = np.nan
    df['0.6'] = np.nan
    df['0.7'] = np.nan
    df['0.8'] = np.nan
    df['0.9'] = np.nan
    df['1.0'] = np.nan

    # Compare all of each file with all of all other files, count number of unique
    for similarity_threshold in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0] :
        for i in range(len(all_modules)) :
            num_unique = 0
            curr_modules = all_modules[i]
            for j in range(len(curr_modules)) :
                is_unique = True
                for other_module_no in range(len(all_modules)) :
                    if other_module_no != i :
                        other_module = all_modules[other_module_no]
                        for k in range(len(other_module)) :
                            if similar(curr_modules[j], other_module[k]) >= similarity_threshold :
                                is_unique = False
                if is_unique :
                    num_unique += 1
            df.loc[names[i], str(similarity_threshold)] = int(num_unique + 0.1)
            

df.to_csv(outfile, sep = '\t')

            

    