## How to run the test
The test file is "CSCI570_Project_Minimum_Jul_14/alignment_test.py"
In the file there is a function test_all(full_test = True, details = True), details control the report length (details = flase generate pass/not pass result only), fulltest=true will run all test in Generated_strings, if false, only the first one will be evaluated
The program will generate a report like this:
```
Result: grade_GEN Pass |grade_BSC Pass |grade_EFF Pass |
Checking: 
        CCACCAGG
        CATGCATG
Alignment:
         GND X: CCAC_CA_GG
         GEN X: CCAC_CA_GG
         BSC X: CCAC_CA_GG
         EFF X: CCAC_CA_GG

         GND Y: C_ATGCATG_
         GEN Y: _CATGCAT_G
         BSC Y: _CATGCAT_G
         EFF Y: _CATGCAT_G

         Score GND:  168
         Score GEN:  168
         Score BSC:  168
         Score EFF:  168

         True score GND:  168
         True score GEN:  168
         True score BSC:  168
         True score EFF:  168
====================================================================================================

Error GEN: N/A
Error BSC: N/A
Error EFF: N/A
```

To run this test file, first you need to activate the virtual env, use 
```bash
source ./CSCI570_ENV/bin/activate
```
Then just change the test scale you want in the file and run it
```bash
python CSCI570_Project_Minimum_Jul_14/alignment_test.py
```

The test file use the python lib Bio to generate ground truth alignment and score, however, since the backtracking direction taught in this course is different than what is used in the general version, thus the alignment of the ground truth shall not be treated as a reference, the only thing matters is the ground truth score
