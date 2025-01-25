import matplotlib.pyplot as plt
import sys

# Finds the type of file
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        first_bytes = file.read(2)
    if first_bytes == b'\xff\xfe' or first_bytes == b'\xfe\xff':
        return 'utf-16'
    return 'utf-8'

# Every third line has the necessary information
def read_every_third_line(file_path):
    encoding = detect_encoding(file_path)
    lines = []
    with open(file_path, 'r', encoding=encoding) as file:
        for i, line in enumerate(file):
            if i % 4 == 3 and not "Not found" in line:
                lines.append(float(line.strip()))
    return lines

# Create the plot!
def plot_histograms(data1, data2, system, c, null, bins=30):
    plt.figure(figsize=(10, 6))
    null = null.capitalize()

    # Create the histograms
    plt.hist(data1, bins=bins, alpha=0.5, label=f'{system} {c}', color='blue', density = True)
    plt.hist(data2, bins=bins, alpha=0.5, label=f'{null}', color='red', density = True)

    plt.xlabel('BPM Correlation')
    plt.ylabel('Percentage')
    plt.title(f'Frequency of Correlations for {null} vs {system} {c}')
    plt.legend(loc='upper right')
    plt.grid(True)

    # Save the plot as a PNG file
    plt.savefig(output_name)
    plt.close()

#############
# Arguments #
#############

# Scoring system
system = sys.argv[1]
# value of c used
c = str(sys.argv[2])
# Null distribution to use
null = sys.argv[3]
# Output directory
output_dir = sys.argv[4]
# Can specify file paths if not standard
file1_path = sys.argv[5]
file2_path = sys.argv[6]

if "ns" in system[-2:] :
    system = system[:-2]
    output_name = output_dir + 'spell_correlations_'  + system + c + '_nosquare_' + null + '.png'
    system = system.capitalize()
    system = system + " (Not Squared)"

else :
    output_name = output_dir + 'spell_correlations_'  + system + c + '_' + null + '.png'
    system = system.capitalize()
    system = system + " (Squared)"


data1 = read_every_third_line(file1_path)
data2 = read_every_third_line(file2_path)

plot_histograms(data1, data2, system, c, null)
