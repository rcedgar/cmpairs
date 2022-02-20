#!/usr/bin/python3

import sys

MIN_EVALUE = 1e-3

'''
#target name         accession query name                            accession mdl mdl from   mdl to seq from   seq to strand trunc pass   gc  bias  score   E-value inc description of target
#------------------- --------- ------------------------------------- --------- --- -------- -------- -------- -------- ------ ----- ---- ---- ----- ------ --------- --- ---------------------
#                  0         1                                     2         3   4        5        6        7        8      9    10   11   12    13     14        15  16                    17
hhrbz_dv4            -         NODE_67741_length_1127_cov_9.528463 -          cm        1       70      632      579      -    no    1 0.48   0.0   26.7   7.5e-07 !   -
hhrbz_dv4            -         NODE_67741_length_1127_cov_9.528463 -          cm        1       70      214      286      +    no    1 0.51   0.0   22.0   1.9e-05 !   -
'''

TblFN = sys.argv[1]
FastaFN = sys.argv[2]

ModelToCoordStrs = {}
CurrentLabel = None
HitLabels = set()
HitLabelToInfoStr = {}

def Flush():
	global ModelToCoordStrs, HitLabels, CurrentLabel

	GoodCoordStrs = []
	GoodModels = []
	AnyHasBoth = False
	for Model in list(ModelToCoordStrs.keys()):
		HasPlus = False
		HasMinus = False
		CoordStrs = ModelToCoordStrs[Model]
		if len(CoordStrs) >= 2:
			for CoordStr in CoordStrs:
				if CoordStr.endswith("+"):
					HasPlus = True
				elif CoordStr.endswith("-"):
					HasMinus = True
				else:
					continue
			if HasPlus and HasMinus:
				GoodModels.append(Model)
	M = len(GoodModels)
	if M == 0:
		return

	InfoStr = "cm="
	for i in range(0, M):
		Model = GoodModels[i]
		InfoStr += Model + "/"
		CoordStrs = ModelToCoordStrs[Model]
		for j in range(0, len(CoordStrs)):
		# for CoordStr in CoordStrs:
			if j > 0:
				InfoStr += ","
			InfoStr += CoordStrs[j]
		InfoStr += ";"

	sys.stderr.write(CurrentLabel + " " + InfoStr + "\n")
	HitLabels.add(CurrentLabel)
	HitLabelToInfoStr[CurrentLabel] = InfoStr

for Line in open(TblFN):
	if Line.startswith('#'):
		continue
	Fields = Line.split()
	assert len(Fields) == 18
	Model = Fields[0]
	QueryLabel = Fields[2]
	SeqLo = Fields[7]
	SeqHi = Fields[8]
	Strand = Fields[9]
	Evalue = float(Fields[15])
	if Evalue > MIN_EVALUE:
		continue

	if QueryLabel != CurrentLabel:
		Flush()
		CurrentLabel = QueryLabel
		ModelToCoordStrs = {}

	CoordStr = "%s:%s%s" % (SeqLo, SeqHi, Strand)
	
	try:
		ModelToCoordStrs[Model].append(CoordStr)
	except:
		ModelToCoordStrs[Model] = [ CoordStr ]

Flush()

def WriteSeq(Label, Seq):
	global n
	n += 1
	sys.stdout.write(">" + Label + "\n")
	W = 80
	SeqLength = len(Seq)
	BlockCount = int((SeqLength + (W-1))/W)
	for BlockIndex in range(0, BlockCount):
		Start = BlockIndex*W
		Block = Seq[Start:Start+W]
		sys.stdout.write(Block + "\n")

def OnSeq(Label, Seq):
	global HitLabels
	if Label not in HitLabels:
		return
	
	InfoStr = HitLabelToInfoStr[Label]
	NewLabel = Label + " " + InfoStr
	WriteSeq(NewLabel, Seq)

Label = None
Seq = ""
N = 0
n = 0
File = open(FastaFN)
while 1:
	Line = File.readline()
	if len(Line) == 0:
		if Seq != "":
			N += 1
			OnSeq(Label, Seq)
		break
	Line = Line.strip()
	if len(Line) == 0:
		continue
	if Line[0] == ">":
		if Seq != "":
			N += 1
			OnSeq(Label, Seq)
		Label = Line[1:]
		Seq = ""
	else:
		Seq += Line.replace(" ", "")

sys.stderr.write("%d / %d sequences output\n" % (n, N))
