import os
import csv

# change directory
os.chdir('/Users/Dustin/iCloud/Power_ROIs')

# ROI size 1, subcortical
r1 = 3.5
# ROI size 2, cortical
r2 = 5

# read in the corrdinates
f = open('coords_ALL.csv') # CHANGE TO UNIX LINE ENDINGS!!
csv_f = csv.reader(f)

# create containers for the relevant parameters
roi = [] # roi ID
size = [] # size
x = [] # x coordinate
y = [] # y coordinate
z = [] # z coordinate

# now parse the CSV data into the containers
for row in csv_f:
    x.append(row[0])
    y.append(row[1])
    z.append(row[2])
    roi.append(row[4])
    size.append(row[5])

# convert to integer
x = map(int, x)
y = map(int, y)
z = map(int, z)
roi = map(int, roi)
size = map(int,size)

# invert the coordinates (because of how 3dcalc works, see help file)
inv_x = [-i for i in x]
inv_y = [-i for i in y]
inv_z = [-i for i in z]

# square the resolution (because of hoe 3dcalc works, see help file)
r1 = str(r1**2)
r2 = str(r2**2)

# begin to assemble the 3dcalc command
# NB: -a needs to be a dataset that you have the the script's directory and on the grid that you want to pull your ROIS from
pre = "3dcalc -a RED_RL_166_V292_1.pb04.scale+tlrc'[0]' -overwrite -SPM -prefix ALL_rois_1st -expr "
# empty container for the -expr that will define the ROIs
expr = ''

# for each ROI, add a term that creates that ROI
for i in range(0,132):
	# decide what resolution to use
	if i+1 <= 14:
		r = r1
	else:
		r = r2
	# build the command for each ROI
	# note that i is the index for the ROI but it is also used in defining the ROI label
	res = "("+(str(i+1))+"*step("+r+"-" # resolution and common aspects
	xc = "(x"+'{:+}'.format(inv_x[i])+")" # x coordinate
	yc = "(y"+'{:+}'.format(inv_y[i])+")" # y coordinate
	zc = "(z"+'{:+}'.format(inv_z[i])+")" # z coordinate
	# create the sphere command
	sphere = res+xc+"*"+xc+"-"+yc+"*"+yc+"-"+zc+"*"+zc+"))"
	# assemble the entire expression in sequential order
	expr = expr+"+"+sphere

# put the whole command together
cmd = pre+"'"+expr+"'"

# write command to a shell script
with open('ALL_ROIs_1st_half.sh', 'w') as f:
	f.write(cmd)
	f.close()

# 2nd half, steps are the same as above
pre = "3dcalc -a RED_RL_166_V292_1.pb04.scale+tlrc'[0]' -overwrite -SPM -prefix ALL_rois_2nd -expr "
expr = ''

for i in range(132,len(roi)):
	r = r2
	res = "("+(str(i+1))+"*step("+r+"-"
	xc = "(x"+'{:+}'.format(inv_x[i])+")"
	yc = "(y"+'{:+}'.format(inv_y[i])+")"
	zc = "(z"+'{:+}'.format(inv_z[i])+")"
	sphere = res+xc+"*"+xc+"-"+yc+"*"+yc+"-"+zc+"*"+zc+"))"
	expr = expr+"+"+sphere

cmd = pre+"'"+expr+"'"

with open('ALL_ROIs_2nd_half.sh', 'w') as f:
	f.write(cmd)
	f.close()