import sys

def main(inputFile):
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
    if len(sys.argv) > 1:
        # Pass the first command-line argument to the main function
        main(sys.argv[1])
    else:
        print("Error: No name provided.")