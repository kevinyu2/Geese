from gprofiler import GProfiler
import sys

# bpm_file, gi_file, smf_file

if __name__ == "__main__":

    # List of bpms
    modules = []

    gp = GProfiler(return_dataframe=True)

    gi_dict = {}

    # Create dictionary of gis
    gi_file = open(sys.argv[2])
    for gi in gi_file:
        info = gi.rstrip().split("\t")
        strings = [info[0], info[1]]
        strings.sort()
        key = strings[0] + " " + strings[1]
        gi_dict[key] = float(info[2])

    smf_dict = {}
    # Create dictionary of smfs
    smf_file = open(sys.argv[3], 'r', encoding='utf-16')
    for smf in smf_file:
        info = smf.rstrip().split("\t")
        #print(smf)
        smf_dict[info[0]] = info[1]

    # Fill in the list
    bpms_file = open(sys.argv[1])
    for bpm in bpms_file :
        if "Module1" in bpm :
            modules.append(bpm.split('Module1\t')[1])
        elif "Module2" in bpm :
            modules.append(bpm.split('Module2\t')[1])
        else :
            modules.append(bpm.split('-- ')[1])

    # Enrichment Cutoff
    cutoff = 500

    # number of terms max
    count = 5
    if (len(sys.argv) > 5) :
        count = int(sys.argv[4])


    for i,module in enumerate(modules) :

        if (i % 2 == 0) :
            print("------------------")
            print ("BPM ", int((i/2) + 1), ": ")
        
        # Get enriched, sort by p_value, report top 5
        df = gp.profile(organism='scerevisiae', query= module)
        p_values_all = df.p_value.tolist()
        sizes_all = df.term_size.tolist()
        go_labels_all = df.name.tolist()
        go_ids_all = df.native.tolist()


        p_values = []
        go_labels = []
        go_ids = []
        for num, size in enumerate(sizes_all) :
            if size <= 500 :
                p_values.append(p_values_all[num])
                go_labels.append(go_labels_all[num])
                go_ids.append(go_ids_all[num])
        
        combined = list(zip(p_values, go_labels, go_ids))
        sorted_combined_list = sorted(combined)


        # get labels
        convert = gp.convert(organism='scerevisiae', query= module)
        names = convert.name.tolist()

        print("\nModule: ", end = "")
        for num, name in enumerate(names) :
            print(name + " [" + str(smf_dict[module.rstrip().split('\t')[num]]) + "],", end = " ")
        print()

        print("Top GO Terms: ", end = "")
        for num,item in enumerate(sorted_combined_list) :
            if (num > count) :
                break
            formatted_value = f"{item[0]:.2e}"
            print(item[1]+ " (ID: "+ item[2]+ ", p: " + formatted_value + "), ", end = "")
        print()

        # Get top scores
        if (i % 2 == 1) :
            print()
            print("Top Scores:")
            scores = []
            module_1 = modules[i - 1].rstrip().split("\t")
            module_2 = modules[i].rstrip().split("\t")
            for a in module_1 :

                for b in module_2 :
                    strings = [a, b]
                    strings.sort()
                    key = strings[0] + " " + strings[1]
                    if key in gi_dict:
                        scores.append((gi_dict[key], key))

            sorted_scores= sorted(scores, key=lambda x: x[0])
            for num_scores, item in enumerate(sorted_scores) :
                if num_scores == 10 :
                    break
                convert_pair = gp.convert(organism='scerevisiae', query= item[1])
                pair_names = convert_pair.name.tolist()
                print(pair_names[0] + " " + pair_names[1] + ": " + str(item[0]))
            print()
                




