#!/bin/bash -e

if [ $# != 3 ] ; then
	echo
	echo "This script has three required args:"
	echo "       $0 fasta_file cm_file output_dir"
	echo
	echo "  fasta_file is input sequences (typically contigs)"
	echo "  cm_file is cm file for cmscan (specify - to use default)"
	echo "  output_dir is output directory (must not already exist)"
	echo
	exit 1
fi

FastaFile=$1
CmFile=$2		# use - for default (dez.cm = DVR4 + hhrbz_dv4)
OutputDir=$3	

EVALUE=1e-3
THREADS=8

if [ ! -f $FastaFile ] ; then
	echo "Input FASTA file $FastaFile not found"
	exit 1
fi

if [ -d $OutputDir ] ; then
	echo "Output directory $OutputDir already exists"
	exit 1
fi

if [ $CmFile == - ] ; then
	CmFile=dez.cm
fi

if [ ! -f $CmFile ] ; then
	echo "CM file $CmFile not found"
	exit 1
fi

cmpress $CmFile

mkdir $OutputDir

TblFile=$OutputDir/cmscan.tbl
PairsFile=$OutputDir/pairs.fa

echo Running cmscan
cmscan \
  -E $EVALUE \
  --tblout $TblFile \
  --cpu $THREADS \
  $CmFile \
  $FastaFile \
  > /dev/null \
  2> $OutputDir/cmscan.stderr
rm -f $OutputDir/cmscan.stderr

ls -lh $TblFile
echo Making $PairsFile

python3 ./serratus_cmscan_pairs.py $TblFile $FastaFile \
  > $PairsFile \
  2> $OutputDir/serratus_cmscan_pairs.stderr

rm -f $OutputDir/serratus_cmscan_pairs.stderr

ls -lh $PairsFile
echo === done ===
