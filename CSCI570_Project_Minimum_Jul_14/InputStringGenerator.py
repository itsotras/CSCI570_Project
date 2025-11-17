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
    input_dir = "Datapoints"
    output_dir = "Generated_strings"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace(".txt", "_generated.txt"))

            print(f"Processing {filename} → {output_path}")

            s1, s2 = generate_strings(input_path)

            with open(output_path, "w") as out:
                out.write(s1 + "\n")
                out.write(s2 + "\n")

    print("Completed Generating the strings ! ")

    # if len(sys.argv) > 1:
    #     # Pass the first command-line argument to the main function
    #     main(sys.argv[1])
    # else:
    #     print("Error: No name provided.")
    # if len(sys.argv) > 1:
    #     # Pass the first command-line argument to the main function
    #     main(sys.argv[1])
    # else:
    #     print("Error: No name provided.")