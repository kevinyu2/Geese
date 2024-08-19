import sys
from gprofiler import GProfiler
from scipy.stats import hypergeom


if __name__ == "__main__":

    # List of bpms
    modules = []

    gp = GProfiler(return_dataframe=True)

    # Fill in the list
    bpms_file = open(sys.argv[1])
    for bpm in bpms_file :
        if "Module1" in bpm :
            modules.append(bpm.split('Module1\t')[1])
        elif "Module2" in bpm :
            modules.append(bpm.split('Module2\t')[1])
        else :
            modules.append(bpm.split('-- ')[1])


    ppi_dict = {} 
    # Set up dictionary of PPI's
    ppi_file = open(sys.argv[2])
    for line in ppi_file :
        protein_1 = line.split("\t")[0]
        protein_2 = line.split("\t")[1]
        key = [protein_1, protein_2]
        key.sort()
        key = protein_1 + protein_2
        ppi_dict[key] = 1

    num_bpms_sig_1std = 0
    num_bpms_sig_2std = 0
    
    # Iterate through the modules
    for i in range(len(modules)) :
        if i % 2 == 0 :
            module_1 = modules[i]
            module_2 = modules[i + 1]
            

            if "\t" in module_1 :
                module_1 = module_1.split("\t")
            else :
                module_1 = module_1.split(" ")

            if "\t" in module_2 :
                module_2 = module_2.split("\t")
            else :
                module_2 = module_2.split(" ")

            
            # Calculate these stats
            num_ppi_total = 0
            num_ppi_within_modules = 0
            num_edges_within_modules = 0
            num_edges_total = 0

            for i in range(len(module_1)) :
                for j in range(len(module_1)) :
                    if i != j :
                        num_edges_total += 1
                        num_edges_within_modules += 1

                        protein_1 = module_1[i]
                        protein_2 = module_1[j]
                        key = [protein_1, protein_2]
                        key.sort()
                        key = protein_1 + protein_2
                        if key in ppi_dict :
                            num_ppi_total += 1
                            num_ppi_within_modules += 1

            for i in range(len(module_2)) :
                for j in range(len(module_2)) :
                    if i != j :
                        num_edges_total += 1
                        num_edges_within_modules += 1

                        protein_1 = module_2[i]
                        protein_2 = module_2[j]
                        key = [protein_1, protein_2]
                        key.sort()
                        key = protein_1 + protein_2
                        if key in ppi_dict :
                            num_ppi_total += 1
                            num_ppi_within_modules += 1

            for i in range(len(module_1)) :
                for j in range(len(module_2)) :
                    num_edges_total += 1

                    protein_1 = module_1[i]
                    protein_2 = module_2[j]
                    key = [protein_1, protein_2]
                    key.sort()
                    key = protein_1 + protein_2
                    if key in ppi_dict :
                        num_ppi_total += 1

            # print(num_edges_within_modules)
            # print(num_edges_total)
            # print()
            # print(num_ppi_total)
            # print(num_ppi_within_modules)

            # Calculate if stdev away
            p_value = hypergeom.cdf(num_ppi_within_modules - 1, num_edges_total, num_ppi_total, num_edges_within_modules)
            # print()
            # print(p_value)
            # print()
            # print("Next:")
            if p_value > 0.84 and not num_ppi_total == 0:
                num_bpms_sig_1std += 1
            if p_value > 0.975 and not num_ppi_total == 0:
                # print(module_1)
                # print(module_2)
                # print()
                num_bpms_sig_2std += 1

    print("PPI Significant (1stdev): " +str(int(num_bpms_sig_1std) - int(num_bpms_sig_2std)) + " / " + str(int(len(modules)/2)))
    print("PPI Significant (2stdev): " +str(int(num_bpms_sig_2std)) + " / " + str(int(len(modules)/2)))
    print("PPI Unsignificant: " +str(int(len(modules)/2) - int(num_bpms_sig_1std)) + " / " + str(int(len(modules)/2)))

