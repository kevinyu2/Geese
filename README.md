# Geese Suite

## Pre-processing

### create_input.py

Creates many input data files for Genecentric

Usage : python ./create_input.py [SGA Format Data] [List of Genes] [Output Folder] [List of Scoring Systems]

Example :
```python ./create_input.py ./Data/SGA_NxN.txt ./Data/cluster0 ./Data/ min mult cubed log```

## BPM File Stats

### beautify_bpm.py

Annotates BPMs with gi scores, GO enrichment, and the single mutant fitnesses. Outputs to stdout

Usage : python ./beautify_bpm.py [BPM File] [Genetic Interaction File] [SMF File] {Count of GO Terms}

Example :
```python ./beautify_bpm.py ./Output/min_90.bpm ./Data/min_0.gi ./smf.txt 5 > Output/min_90.bbpm```

### enrichment.py

Generates enrichment counting data for a set of BPMs. Outputs to stdout

Usage : python ./encrichment.py [BPM File]

Example :
```python ./enrichment.py ./Output/min_90.bpm```

### ppi_enrichment.py

Calculates PPI based enrichment statistics

Usage : python ./ppi_enrichment.py [BPM File] [PPI File]

Example :
```python ./ppi_enrichment ./Output/log_90.bpm ./Data/ppi_data.txt```

### average_size.py

Calculates average size of module

Usage : python ./average_size.py [BPM File]

Example :
```python ./average_size.py ./Output/log_90.bpm```

## SPELL Pipeline

### randomize_within_file.py

Randomizes a BPM file in two different ways: either randomizes each gene or shuffles the genes within the file (ensuring that no genes were repeated in a BPM). If no second file is given then the latter occurs. Outputs to standard output

Usage : python ./random_within_file.py [BPM File] {List of Genes}

Example :
```python ./randomize_within_file.py ./Output/mult_80.bpm ./Data/cluster0 > Output/randomized_mult_80.bpm```

### spell_correlation.py

Calculates SPELL dataset gene expression correlations between different BPMs. Outputs to standard output

Usage : python ./spell_correlation.py [SPELL Folder (Downloaded)] [BPM file]

Example :
```python ./spell_correlation.py ../CScripts/all_spell_datasets/ ./Output/mult_90.bpm > ../CScripts/spell_results/spell_mult90.txt```

### spell_graphs.py

Creates a histogram from the SPELL results using a null distribution from a randomized file

Usage : python ./spell_graphs.py [Scoring System] [Value of C] [Null (shuffled or random)] [Output Directory] [SPELL Non-Null] [SPELL Null]

Example :
```python ./spell_graphs.py mult 90 shuffled ./Output/ ./Data/spell_mult90.txt ./Data/spell_mult90_shuffled.txt```