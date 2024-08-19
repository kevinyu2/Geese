import os
import sys
import zipfile
import pandas as pd
import numpy as np

# Get file type
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        first_bytes = file.read(2)
    if first_bytes == b'\xff\xfe' or first_bytes == b'\xfe\xff':
        return 'utf-16'
    return 'utf-8'

# Recursively find files
def find_pcl_files(root_folder):
    """ Recursively find all .pcl files in the specified root folder, including within zip archives. """
    pcl_files = []
    
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.pcl'):
                pcl_files.append(file_path)
            elif file.endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    for zip_file in zip_ref.namelist():
                        if zip_file.endswith('.pcl'):
                            pcl_files.append((file_path, zip_file))
    
    return pcl_files

def process_pcl_files(pcl_files):
    """ Process each .pcl file and calculate correlations for each column being 'a'. """

    dfs = []

    for item in pcl_files:
        if isinstance(item, tuple):
            zip_path, file_name = item
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    with zip_ref.open(file_name) as file:
                        df = pd.read_csv(file, sep = "\t")
            except Exception as e:
                print(f"Error reading {zip_path} inside zip file: {file_name}. Skipping. Error: {e}")
                continue
        else:
            try:
                df = pd.read_csv(item, sep = "\t")
                
            except Exception as e:
                print(f"Error reading file: {item}. Skipping. Error: {e}")
                continue


        #print(item)
        df.set_index(df.columns[0], inplace = True)

        # if ("YORF" in df.columns) :
        #     df.set_index("YORF", inplace = True)
        # elif ("ID_REF" in df.columns) :
        #     df.set_index("ID_REF", inplace = True)
        # else :
        #     df.set_index("Name", inplace = True)

            
        
        # Drop the first and second columns
        if len(df.columns) > 2:
            df = df.drop("GWEIGHT", axis=1)
            #df = df.drop("NAME", axis=1)
            if "IDENTIFIER" in df.columns :
                df = df.drop("IDENTIFIER", axis=1)
            elif "NAME" in df.columns :
                df = df.drop("NAME", axis = 1)
            elif "Description" in df.columns :
                df = df.drop("Description", axis = 1)
            elif "Name" in df.columns :
                df = df.drop("Name", axis = 1)
            else :
                df = df.drop("GENE", axis = 1)
    
        dfs.append(df)

    return dfs


# Get dict of correlations
def calculate_correlations(dfs, rows) :
    correlations = {row: [] for row in rows}
    
    num_present = 0


    for df in dfs :
        for a in rows:
            if a in df.index:
                rows_to_check = [row for row in rows if row != a]
                if set(rows_to_check).issubset(df.index):
                    if a == rows[0] :
                        num_present += 1
                    # print(a)
                    # print(rows_to_check)
                    has_nan = False
                    row_correlations = []
                    for row in rows_to_check:
                        # Transpose the DataFrame and select rows a and row for correlation calculation
                        corr = df.loc[[a, row]].astype(float).T.corr().iloc[0, 1]

                        if not np.isnan(corr):
                            row_correlations.append(corr)
                        else : 
                            has_nan = True
                    if row_correlations and not has_nan:
                        avg_corr = sum(row_correlations) / len(row_correlations)
                        correlations[a].append(avg_corr)
    print("Datasets: " + str(num_present))

    return correlations

def main():
    if len(sys.argv) < 3:
        print("Usage: python spell_correlation.py [folder] [bpm file]")
        sys.exit(1)
    
    folder_name = sys.argv[1]
    bpm_file = sys.argv[2]
    
    pcl_files = find_pcl_files(folder_name)
    
    if not pcl_files:
        print("No .pcl files found.")
        sys.exit(1)

    encoding = detect_encoding(bpm_file)
    with open(bpm_file, 'r', encoding=encoding) as f:
    # with open(bpm_file) as f:
        bpms = f.readlines()

    dfs = process_pcl_files(pcl_files)

    bpm_correlations = []
    for line in bpms:
        line = line.strip()
        print()
        print(line)
        if "Module2" in line :
            module = line.split('Module2\t')[1]
        else :
            module = line.split('Module1\t')[1]

        module_arr = module.split('\t')

        correlations = calculate_correlations(dfs, module_arr)

        total_correlation = 0
        num_correlation = 0
    
        for a, corr_list in correlations.items():
            if corr_list:
                avg_correlation = sum(corr_list) / len(corr_list)
                total_correlation += avg_correlation
                num_correlation += 1
            #     print(f"Average correlation for '{a}': {avg_correlation}")
            # else:
            #     print(f"No valid dataframes with columns '{a}' and {line} found.")
        if num_correlation != 0:

            print(total_correlation/num_correlation)
            bpm_correlations.append(total_correlation/num_correlation)
        else :
            print("Not found")
    print()
    print("Average correlation: " + str(sum(bpm_correlations)/len(bpm_correlations)))
    

if __name__ == "__main__":
    main()
