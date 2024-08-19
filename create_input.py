import pandas as pd
import numpy as np
import sys
import math

#############
# Arguments #
#############

# Data to change
sga = sys.argv[1]
sga_df = pd.read_csv(sga, sep = '\t')
print("Input scores read")

# Subset file
subset = sys.argv[2]
subset_set = set()
with open(subset, 'r') as file:
    for line in file:
        subset_set.add(line.strip())

# Output folder
output_dir = sys.argv[3]

# List of scoring systems to use (mult, min, cubed, log)
scoring_systems = []
for i in range(4, len(sys.argv)) :
    if sys.argv[i] not in ['min', 'mult', 'cubed', 'log'] :
        print(f'{sys.argv[i]} Scoring system unknown, ignoring. Use: min, mult, cubed, or log')
    else :
        scoring_systems.append(sys.argv[i])

####################
# Modify dataframe #
####################

sga_df['Query ID'] = sga_df['Query Strain ID'].str.split('_').str[0]
sga_df['Array ID'] = sga_df['Array Strain ID'].str.split('_').str[0]

sga_df = sga_df[['Query ID', 'Array ID', 'Query single mutant fitness (SMF)', 'Array SMF', 'Double mutant fitness']]
sga_df_subset = sga_df[sga_df['Query ID'].isin(subset_set)]
sga_df_subset = sga_df_subset[sga_df_subset['Array ID'].isin(subset_set)]
sga_df_subset = sga_df_subset.dropna()
sga_df_subset['Query SMF'] = sga_df_subset['Query single mutant fitness (SMF)'].astype(float)
sga_df_subset['Array SMF'] = sga_df_subset['Array SMF'].astype(float)

print("Dataframe processing complete")

#########################
# The scoring functions #
#########################

def convert_to_mult(qsmf, asmf, dmf) :
    return (dmf - (qsmf * asmf))

def convert_to_min(qsmf, asmf, dmf) :
    return (dmf - min(qsmf, asmf))

def convert_to_cubed(qsmf, asmf, dmf) :
    return 20 * ((dmf - min(qsmf, asmf) + 0.03) ** 3)

def convert_to_log(qsmf, asmf, dmf) :
    if dmf <= 0 :
        dmf = 0.0000001
    if asmf <= 0 :
        asmf = 0.0000001
    if dmf <= 0 :
        dmf = 0.0000001
    return (math.log2(dmf) - (math.log2(qsmf) + math.log2(asmf)))

###########
# Convert #
###########

print("Converting")

for system in scoring_systems :
    outfile = output_dir + system + '_'+ subset[-1] + '.gi'
    with open(outfile, 'w') as file:
        if system == 'min' :
            for i, row in sga_df_subset.iterrows() :
                result = convert_to_min(row['Query SMF'], row['Array SMF'], row['Double mutant fitness'])
                formatted_result = f"{result:.7f}"
                file.write(row['Query ID'] + '\t' + row['Array ID'] + '\t' + formatted_result + '\n')
        elif system == 'mult' :
            for i, row in sga_df_subset.iterrows() :
                result = convert_to_mult(row['Query SMF'], row['Array SMF'], row['Double mutant fitness'])
                formatted_result = f"{result:.7f}"
                file.write(row['Query ID'] + '\t' + row['Array ID'] + '\t' + formatted_result + '\n')
        elif system == 'cubed' :
            for i, row in sga_df_subset.iterrows() :
                result = convert_to_cubed(row['Query SMF'], row['Array SMF'], row['Double mutant fitness'])
                formatted_result = f"{result:.7f}"
                file.write(row['Query ID'] + '\t' + row['Array ID'] + '\t' + formatted_result + '\n')
        elif system == 'log' :
            for i, row in sga_df_subset.iterrows() :
                result = convert_to_log(row['Query SMF'], row['Array SMF'], row['Double mutant fitness'])
                formatted_result = f"{result:.7f}"
                file.write(row['Query ID'] + '\t' + row['Array ID'] + '\t' + formatted_result + '\n')