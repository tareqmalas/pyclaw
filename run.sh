#! /bin/bash

CUR_DIR=$PWD

OUT_DIR=results

#PROBLEM_PATH=apps/euler/2d/shockbubble/
#PROBLEM_NAME=shockbubble
#X_BASE=80
#Y_BASE=20
PROBLEM_PATH=apps/shallow/2d/
PROBLEM_NAME=shallow2D
X_BASE=50
Y_BASE=50

if [ ! -d $OUT_DIR ]; then
  mkdir $OUT_DIR
  echo "Created $OUT_DIR directory to store the results"
fi

for WENO_ORDER in 5 #7 9 17
do
for SIZE in 1 #2 4 6 8
do

let NX=$X_BASE*$SIZE
let NY=$Y_BASE*$SIZE

OUT_NAME=${CUR_DIR}/$OUT_DIR/${PROBLEM_NAME}_${WENO_ORDER}_${NX}x${NY}

echo `date` | tee $OUT_NAME
cd $PROBLEM_PATH
echo "Entering $PROBLEM_PATH" | tee -a $OUT_NAME

if [ -z "$CPU" ]; then
	echo "not running on shaheen"

  COMMAND="python $PROBLEM_NAME.py solver_type=sharpclaw lim_type=2 weno_order=$WENO_ORDER mx=$NX my=$NY"
  echo  $COMMAND  | tee -a $OUT_NAME
  $COMMAND 2>&1 | tee -a $OUT_NAME 

else 
	echo "running on tareq laptop"	
	# kslrun -t 20:00 -r -m VN -a k47 -n 1 "$BGP_PYTHON shallow2D.py solver_type=sharpclaw mx=100 my=100"

fi 
cd $CUR_DIR
echo "Leaving $PROBLEM_PATH" | tee -a $OUT_NAME

done
done


