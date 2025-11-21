from Bio.Align import PairwiseAligner
from Bio.Align.substitution_matrices import Array

from efficient import align_memory_efficient
from basic import basic_align
import os
import numpy as np
import traceback
    
def score_alignment(seqX, seqY, M):
    score = 0
    for a, b in zip(seqX, seqY):
        if a == '_' or b == '_':      # gap
            score += -30
        else:
            score += M[a, b]
    return int(abs(score))

def align(s1, s2, M):
    # characters in alphabet
    alphabet = ["A", "C", "G", "T"]
    # custom substitution matrix
        # Create a matrix with explicit alphabet

    aligner = PairwiseAligner()
    aligner.mode = "global"

    # Set substitution scores
    aligner.substitution_matrix = M
    #aligner.alphabet = alphabet

    # Gap penalties
    aligner.gap_score = -30
    alignments = aligner.align(s1, s2)

    seqX = str(alignments[0][0]).replace("-", "_")
    seqY = str(alignments[0][1]).replace("-", "_")
    score = int(abs(alignments.score))
    return (seqX, seqY, score)


def test_all(full_test = True, details = True):
    # source dir: ./CSCI570_Project
    M = Array("ACGT", dims=2)

    M["A","A"] = 0
    M["A","C"] = -110
    M["A","G"] = -48
    M["A","T"] = -94

    M["C","A"] = -110
    M["C","C"] = 0
    M["C","G"] = -118
    M["C","T"] = -48

    M["G","A"] = -48
    M["G","C"] = -118
    M["G","G"] = 0
    M["G","T"] = -110

    M["T","A"] = -94
    M["T","C"] = -48
    M["T","G"] = -110
    M["T","T"] = 0

    output_dir = "CSCI570_Project_Minimum_Jul_14/Outputs"
    input_dir = "CSCI570_Project_Minimum_Jul_14/Generated_strings"
    if full_test:
        all_entries = os.listdir(input_dir)

        for input_file in all_entries:
            output = output_dir+"/"+input_file.strip(".txt")+"_out.txt"
            input = input_dir+"/"+input_file
            single_test(input, output, M, details=details)

    else:
        input = "CSCI570_Project_Minimum_Jul_14/Generated_strings/in1_generated.txt"
        output = "CSCI570_Project_Minimum_Jul_14/Outputs/in1_generated_out.txt"
        single_test(input, output, M, details=details)


def single_test(input, output, M, details=True):
    states = ["Fail","Pass", "Bug"]
    with open(input, "r") as f:
        DNAs = f.readlines()

    grades = {}
    X = DNAs[0].strip("\n")
    Y = DNAs[1].strip("\n")
    # Ground-Truth, produced by global alignment in Bio package 
    seqX_GND, seqY_GND, score_GND = align(X,Y,M)
    
    try:
        with open(output, "r") as f:
            Aligned = f.readlines() 
        seqX_GEN, seqY_GEN, score_GEN = Aligned[1].strip("\n"), Aligned[2].strip("\n"), Aligned[0].strip("\n")
        score_GEN = int(score_GEN)
        score_test_GEN = score_alignment(seqX_GEN, seqY_GEN, M)
        grades["grade_GEN"] = int((score_GEN==score_GND) and (score_test_GEN==score_GEN))
        err_GEN = "N/A"
    except Exception as e:
        # Mark as bug
        seqX_GEN, seqY_GEN, score_GEN, score_test_GEN = "N/A", "N/A", "N/A", "N/A"
        grades["grade_GEN"] = 2
        err_GEN = traceback.format_exc()

    try:
        score_BSC, seqX_BSC, seqY_BSC = basic_align(X, Y)
        score_test_BSC = score_alignment(seqX_BSC, seqY_BSC, M)
        grades["grade_BSC"] = int((score_BSC==score_GND) and (score_test_BSC==score_BSC))
        err_BSC = "N/A"
    except Exception as e:
        # Mark as bug
        seqX_BSC, seqY_BSC, score_BSC, score_test_BSC = "N/A", "N/A", "N/A", "N/A"
        grades["grade_BSC"] = 2
        err_BSC = traceback.format_exc()

    try:
        seqX_EFF, seqY_EFF, score_EFF = align_memory_efficient(X, Y)
        score_test_EFF = score_alignment(seqX_EFF, seqY_EFF, M)
        grades["grade_EFF"] = int((score_EFF==score_GND) and (score_test_EFF==score_EFF))
        err_EFF = "N/A"
    except Exception as e:
        # Mark as bug
        seqX_EFF, seqY_EFF, score_EFF, score_test_EFF = "N/A", "N/A", "N/A", "N/A"
        grades["grade_EFF"] = 2
        err_EFF = traceback.format_exc()
    
    message = ""
    for grade in grades.keys():
        message += grade + " " + states[grades[grade]] + " |"
    print("Result: "+message)
    if details:
        print("Checking: \n\t"+ X + "\n\t" + Y)
        print("Alignment:")
        print("\t GND X: " + seqX_GND)
        print("\t GEN X: " + seqX_GEN)
        print("\t BSC X: " + seqX_BSC)
        print("\t EFF X: " + seqX_EFF)
        print()

        print("\t GND Y: " + seqY_GND)
        print("\t GEN Y: " + seqY_GEN)
        print("\t BSC Y: " + seqY_BSC)
        print("\t EFF Y: " + seqY_EFF)
        print()

        print("\t Score GND: ", score_GND)
        print("\t Score GEN: ", score_GEN)
        print("\t Score BSC: ", score_BSC)
        print("\t Score EFF: ", score_EFF)
        print()

        print("\t True score GND: ", score_GND)
        print("\t True score GEN: ", score_test_GEN)
        print("\t True score BSC: ", score_test_BSC)
        print("\t True score EFF: ", score_test_EFF)
        print("="*100 + "\n")
    
        print("Error GEN: "+ err_GEN)
        print("Error BSC: "+ err_BSC)
        print("Error EFF: "+ err_EFF)

    print("Score: " + str(score_GND) + "\n"+"-"*50 + "\n")

test_all(full_test=False)
# test_all(details=False)
# test_all(full_test=False, details=False)