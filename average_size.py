import sys

if __name__ == "__main__":

    # List of bpms
    modules = []

    # Fill in the list
    bpms_file = open(sys.argv[1])
    for bpm in bpms_file :
        if "Module1" in bpm :
            modules.append(bpm.split('Module1\t')[1])
        elif "Module2" in bpm :
            modules.append(bpm.split('Module2\t')[1])
        else :
            modules.append(bpm.split('-- ')[1])

    total_length = 0
    for module in modules :
        if "\t" in module :
            module_arr = module.split("\t")
        else :
            module_arr = module.split(" ")
        total_length += len(module_arr)

    print("Average: ", total_length/len(modules))