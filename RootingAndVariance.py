import dendropy
import sys
import subprocess
import os

"""
This program is intended to take as input a folder of gene trees, midpoint root each of them, and then output a table containing each gene tree name with its root-to-tip variance (calculated using pxlstr in phyx). 
"""

# Checking inputs and getting the gene list - we expect a gene folder name and 
# a prefix for the output files. 
if len(sys.argv) == 3:
    folder_name = sys.argv[1]
    out_prefix = sys.argv[2]
else:
    print("\nUsage: python3 " + sys.argv[0] + " folder_of_genes outfile_prefix\n")
    sys.exit()

gene_tree_list = os.listdir(folder_name)


# When we write out to the .csv file, we want to include headers for the columns
# on the first line. 
firstTime = True

for gene in gene_tree_list:
    with open(folder_name + "/" + gene) as f:
        for line in f:
            tree_str = line

        # First we read the tree.
        tree = dendropy.Tree.get(
                data = tree_str,
                schema = "newick",
                rooting = "default-rooted")

        # Then remove outgroups
        #tree.prune_taxa_with_labels([OUTGROUPS])

        # Then we midpoint root.
        tree.reroot_at_midpoint()

        # Then we get the rooted tree and chop off the "[&R] " at the start.
        rooted_tree = tree.as_string(schema='newick')
        rooted_tree = rooted_tree[5:]

        # Now write the rooted tree out to a temporary file, as phyx takes a 
        # file as input.
        with open("temp.tre", 'w') as f:
            f.write(rooted_tree)

        # Getting root-to-tip variance with phyx. 
        cmd = ["pxlstr", "-v", "-t", "temp.tre"]

        var_process = subprocess.run(cmd, text = True, capture_output = True)
        root_tip_var = var_process.stdout
        
        root_tip_var = root_tip_var.strip()
        
        # Making the .csv file... 
        if firstTime:
            with open(out_prefix + ".csv", 'w') as f:
                f.write("gene,root_tip_var\n") # Column headers! 
                f.write(gene + "," + root_tip_var + "\n")
        else:
            with open(out_prefix + ".csv", "a") as f:
                f.write(gene + "," + root_tip_var + "\n")

        # ...and the log. 
        with open(out_prefix + ".log", 'a') as f:
            f.write("gene name: \n" + gene + "\n")
            f.write("original tree: \n" + tree_str)
            f.write("rooted tree: \n" + rooted_tree)
            f.write("getting root to tip variance: \n" + str(var_process) + "\n\n")

    firstTime = False
