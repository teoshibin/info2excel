# info2excel
A small script written for AI method coursework, to speed up the process of copying delta f target values
The values were retrieve directly from .info thats generated by [BBOB](https://coco.gforge.inria.fr/doku.php?id=bbob-2010-downloads) or [numbbo](https://github.com/numbbo/coco/) framework

<p align="center" float="left">
  <img src="screenshots/1.png" width="179"/>
  <img src="screenshots/2.png" width="179"/>
  <img src="screenshots/3.png" width="179"/>
  <img src="screenshots/4.png" width="179"/>
</p>

## Previous issue
### Problem
retrieving negative and zeros values   
```
precision = 1e-8   
global_best = foptimal = 50   
ftarget = foptimal + precision   
delta fitness = fbest - ftarget   
```
Therefore, if fbest reached the global minimum, say at `50`, `ftarget = 50 + 1e-8`   
```
delta_fitness = 50 - 50 - 1e-8
delta fitness = -1e-8
```
### Solution   
replace values beyond the bound with threshold values
```
maximum_delta = 1e+3
minimum_delta = 1e-14
```
## Installation
### Windows (cmd Batch)
1. clone and navigate into the repository

	```Sh
		cd [REPO]
	```
2. create virtual environment
	```Sh
		python -m venv info2excel\venv
	```
3. activate virtual environment (a prefix of "(venv)" will be displayed in your command prompt when succesfully activated)
	```Sh
		info2excel\venv\Scripts\activate
	```
4. install dependencies
	```Sh
		pip install -r info2excel\requirements.txt
	```
### Mac (terminal Bash)
1. clone and navigate into the repository

	```Bash
		cd [REPO]
	```	
2. create virtual environment
	```Bash
		python -m venv info2excel/venv
	```
3. activate virtual environment (a prefix of "(venv)" will be displayed in your command prompt when succesfully activated)
	```Bash
		source info2excel/venv/bin/activate
	```
4. install dependencies
	```Bash
		pip3 install -r info2excel/requirements.txt
	```	
## Generate Delta ftarget Excel Score
### Execution
1. place datasets into [Datasets](Datasets) folder
2. activate virtual environment (step 3 of installation)
3. generate excel
	
	```Sh
		info2excel\info2excel.py -i [DATASET] 								# or
		info2excel\info2excel.py -i [DATASET] -d [DIMENSION] -o [EXCELNAME] -u [UPPER_BOUND] -l [LOWER_BOUND]
		# OPTIONAL ARGUMENTS
		# d by default 5
		# o by default "[ALGONAME]_[DIMENSION]D"
		# u by default 1e+3
		# l by default 1e-14
	```
	Example command
	```Sh
		info2excel\info2excel.py -i CMAES 				#or
		info2excel\info2excel.py -i CMAES -d 5 -o CMAES_5D -u 1e+3 -l 1e-14
		# both output same content : CMAES_5D.xlsx
	```
4. generated excel is in [ExcelScore](ExcelScore)

	> **NOTE**   
	> Always remove pre-existing dataset when rerunning the experiment
