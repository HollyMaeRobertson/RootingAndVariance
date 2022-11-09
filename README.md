# RootingAndVariance
A program that midpoint roots trees then calculates and reports their root-to-tip variance. 


### Usage: 

```
python3 RootingAndVariance.py folder_of_genes outfile_prefix
```

For example, using the ExampleGenes folder to create the outputs example.csv and example.log as included here, the command was:

```
python3 RootingAndVariance.py ExampleGenes example
```

### Details
The output file \[outfile\_prefix\].csv lists the name of each file in the gene column and the corresponding root-to-tip variance, as calculated by the [phyx](https://github.com/FePhyFoFum/phyx) tool pxlstr, in the root\_tip\_var column. 

Phyx will also produce a log called phyx.logfile, and the program generates a file called temp.tre that can be deleted after running. 

### Dependencies
This program uses [DendroPy](https://dendropy.org/primer/index.html) to midpoint root unrooted trees and [phyx](https://github.com/FePhyFoFum/phyx) to calculate root-to-tip variance.
