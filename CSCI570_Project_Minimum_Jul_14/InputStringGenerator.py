import sys
import os

def generate_strings(inputFile):
    str1 = ""
    str2 = ""
    try:
       with open(inputFile, 'r') as file:
        curr = ""
        all_lines = file.readlines()
        for line in all_lines:
            line = line.strip()
            if(line.isalpha()):
                if(curr != ""):
                    str1 = curr
                curr = line
            else:
                curr = curr[:(int)(line)+1]+curr+curr[(int)(line)+1:]
        str2 = curr
        print(str1)
        print(str2)
    except FileNotFoundError:
        print(f"Error: The file '{inputFile}' was not found.")
    return str1, str2

if __name__ == "__main__":

    s1, s2 = generate_strings(sys.argv[1])
    print(s1, s2)