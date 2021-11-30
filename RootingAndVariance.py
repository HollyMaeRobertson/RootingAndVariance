import dendropy
import sys
import subprocess
import os

"""
This program is intended to take as input a folder of gene trees, midpoint root each of them, and then output a table containing each gene tree name with its root-to-tip variance (calculated using pxlstr in phyx). 
"""


if len(sys.argv) == 3:
    folder_name = sys.argv[1]
    out_prefix = sys.argv[2]
else:
    print("\nUsage: " + sys.argv[0] + " folder_of_genes outfile_prefix\n")
    sys.exit()

gene_tree_list = os.listdir(folder_name)

firstTime = True

for gene in gene_tree_list:
    with open(folder_name + "/" + gene) as f:
        for line in f:
            tree_str = line

        # First we read the tree
        tree = dendropy.Tree.get(
                data = tree_str,
                schema = "newick",
                rooting = "default-rooted")

        # Then remove outgroups
        #tree.prune_taxa_with_labels([OUTGROUPS])

        # Then we midpoint root
        tree.reroot_at_midpoint()

        # Then we get the rooted tree and chop off the [&R] bit
        rooted_tree = tree.as_string(schema='newick')
        rooted_tree = rooted_tree[5:]

        # Now write the rooted tree out to a new directory
        with open("temp.tre", 'w') as f:
            f.write(rooted_tree)

        # Now use phyx to get the root to tip variance
        cmd = ["pxlstr", "-v", "-t", "temp.tre"]

        var_process = subprocess.run(cmd, text = True, capture_output = True)
        root_tip_var = var_process.stdout
        
        root_tip_var = root_tip_var.strip()
        
        # Writing the variance out to the file with the gene names
        if firstTime:
            with open(out_prefix + ".csv", 'w') as f:
                f.write("gene,root_tip_var\n")
                f.write(gene + "," + root_tip_var + "\n")
        else:
            with open(out_prefix + ".csv", "a") as f:
                f.write(gene + "," + root_tip_var + "\n")

        if firstTime:
            with open(out_prefix + ".log", 'w') as f:
                f.write("gene name: \n" + gene + "\n")
                f.write("original tree: \n" + tree_str + "\n")
                f.write("rooted tree: \n" + rooted_tree + "\n")
                f.write("getting root to tip variance: " + str(var_process) + "\n")

        else:
            with open(out_prefix + ".log", 'a') as f:
                f.write("gene name: \n" + gene + "\n")
                f.write("original tree: \n" + tree_str + "\n")
                f.write("rooted tree: \n" + rooted_tree + "\n")
                f.write("getting root to tip variance: \n" + str(var_process) + "\n")


    firstTime = False
