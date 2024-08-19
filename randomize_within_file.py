###
# Randomizes within a BPM file either based on random genes from pool or shuffles within the file
###


import random
import sys

# Get BPM file read n
with open(sys.argv[1]) as f :
    content = f.readlines()
    for i in range(len(content)) :
        if i % 2 == 0 :
            content[i] = content[i].split('Module1\t')[1]
        else :
            content[i] = content[i].split('Module2\t')[1]

# If doing it from a large gene file
if len(sys.argv) > 2 :
    with open(sys.argv[2]) as f :
        genes = f.readlines()


    # Randomly choose for each gene
    for line_num,line in enumerate(content) :
        mod_size = line.count('\t') + 1
        indices = random.sample(range(len(genes)), mod_size)
        new_module = [genes[idx] for idx in indices]

        string_to_add = ""
        for i in new_module :
            string_to_add += i.rstrip() + "\t"
        string_to_add.rstrip()
        if (line_num % 2 == 0) :
            print("BPM" + str(int(line_num/2)) + "\Module1\t" + string_to_add)
        else :
            print("BPM" + str(int(line_num/2)) + "\Module2\t" + string_to_add)

# Shuffle the genes in the file
else :
    genes_arr = []

    for line in content :
        line_arr = line.split('\t')
        for gene in line_arr :
            gene = gene.rstrip()
            genes_arr.append(gene)

    random.shuffle(genes_arr)

    shuffled_index = 0
    for line_num,line in enumerate(content) :
        string_to_add = ""
        for module_index in range(line.count('\t') + 1) :
            gene_to_add = genes_arr[shuffled_index]
            # Prevent duplicates
            while gene_to_add in string_to_add :
                gene_to_add = random.choice(genes_arr)
            string_to_add += gene_to_add + "\t"
            shuffled_index += 1
        string_to_add.rstrip()

        if (line_num % 2 == 0) :
            print("BPM" + str(int(line_num/2)) + "\Module1\t" + string_to_add)
        else :
            print("BPM" + str(int(line_num/2)) + "\Module2\t" + string_to_add)
        


    







    
    



