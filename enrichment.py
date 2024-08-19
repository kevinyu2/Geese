# Enrichment stats for bpm files

from gprofiler import GProfiler
import sys

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

    # Enrichment Cutoff
    cutoff = 500
    if (len(sys.argv) > 2) :
        cutoff = int(sys.argv[2])

    # p-value used is 0.05
    # Tally info, prep BPM calcs
    module_GO_IDs = []
    modules_enriched = 0
    for i, module in enumerate(modules) :
        module_GO_IDs.append([])
        df = gp.profile(organism='scerevisiae', query= module)

        # Add if below the cutoff
        to_add = False
        for j, size in enumerate(df.term_size):
            if size <= cutoff and len(df.intersection_size) > 1 : # TODO: I'm assuming the size 1's are bad too
                to_add = True
                module_GO_IDs[i].append(df.native[j])
        if to_add :
            modules_enriched += 1

    # BPM stats
    one_mod_enriched = 0
    no_mod_enriched = 0
    enriched_for_same = 0
    enriched_for_different = 0

    for i, module in enumerate(modules) :
        if i % 2 == 0 :
            # Not both modules enriched
            if len(module_GO_IDs[i]) == 0 and len(module_GO_IDs[i + 1]) == 0 :
                no_mod_enriched += 1
            elif len(module_GO_IDs[i]) == 0 or len(module_GO_IDs[i + 1]) == 0 :
                one_mod_enriched += 1

            # Both modules enriched
            else :
                found_same = False
                for ID in module_GO_IDs[i] :
                    if ID in module_GO_IDs[i + 1] :
                        found_same = True
                
                if found_same :
                    enriched_for_same += 1
                else :
                    enriched_for_different += 1



    print("Modules Enriched: ", modules_enriched, "/", len(modules), "\nPercentage: ", modules_enriched/len(modules))
    print("\n BPMs: \n", "Enriched for Same: ", enriched_for_same, "\nEnriched for Different: ", enriched_for_different, "\nOne Module Enriched: ", one_mod_enriched, "\nNo Modules Enriched: ", no_mod_enriched)


