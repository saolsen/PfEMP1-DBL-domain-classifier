#   Bioinformatics Final Project
#   Author: Stephen Olsen
#   filename: 
#   -Takes a PfEMP1 DBL domain and determines if it is an alpha or alpha_1
#       DBL domain using a profile hmm created out of PfEMP1 IT4 var domains.
#   -Uses hmmer3 to check the DBL domain against pre-trained phmms
#       DBL_alpha.hmm and DBL_alpha_1.hmm
#   -A multiple alignment of known alpha and alpha_1 DBL domains from IT4
#       var genes of PfEMP1 was created with clustalW2 and an hmm was trained
#       with hmmer3
#   -At this time domain files must be in the FASTA format
#
#   -Requires hmmer3 to run.

import os

# Process Hmmer3 output file
# returns a dict of scores indexed by string names
def process_hmmer3(f) :
    scores = {}
    file_out = open(f, 'r')
    file_output = file_out.readlines()
    i = 14
    line = file_output[i]
    while line != '\n':
        # Process each line
        name = line[60:]
        name = name.strip()
        score = line[13:18]
        scores[name] = float(score)
        i += 1
        line = file_output[i]
    file_out.close()
    # Returns the dictionary
    return scores

# locate DBL_alpha.hmm and DBL_alpha_1.hmm
# find them in current directory
if (not(os.path.exists('./DBL_alpha.hmm') and
	    os.path.exists('./DBL_alpha_1.hmm'))):
    print "DBL_alpha.hmm and DBL_alpha_1.hmm don't exist in this directory."
    raise SystemExit
# Welcome message		
print "Welcome to the PfEMP1 DBL domain classifier"
print "Currently supports alpha and alpha_1 DBL domains"
# Get DBL sequence file
#file = raw_input("Please enter your domain file: ")
file = 'all_DBL_domains'
# Check file against hmms with hmmer
os.system('hmmsearch DBL_alpha.hmm ' + file + ' > a.out')
os.system('hmmsearch DBL_alpha_1.hmm ' + file + ' > a1.out')
# Process a1.out
a1_scores = process_hmmer3('./a1.out')
a_scores = process_hmmer3('./a.out')
# Print results
print 'Name\t\t\tA_1 score\tA score\ttype'
for sequence in a1_scores:
    if a1_scores[sequence] > a_scores[sequence]:
        DBL_type = 'alpha_1'
    else:
        DBL_type = 'alpha'
    print '%s\t%g\t\t%g\t\t%s' % (sequence, a1_scores[sequence], a_scores[sequence], DBL_type)

