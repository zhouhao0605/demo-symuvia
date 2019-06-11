SymuGame.exe -seed 9 -rate 1 -method 1 "C:\SG\Lyon63V_007_BDT.csv" "C:\SG\Lyon63V_008.xml" > log1.log
echo "method 1 OK"

SymuGame.exe -seed 99 -rate 1 -method 2 "C:\SG\Lyon63V_007_BDT.csv" "C:\SG\Lyon63V_008.xml" > log2.log
echo "method 2 OK"

SymuGame.exe -seed 999 -rate 1 -method 3 "C:\SG\Lyon63V_007_BDT.csv" "C:\SG\Lyon63V_008.xml" > log3.log
echo "method 3 OK"