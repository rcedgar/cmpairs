# cmpairs
Parse infernal cmscan tbl file to find pairs of hits to same model on different strands.

The script `run_cmpairs.bash` invokes `cmscan` (infernal search) and then `serratus_cmscan_pairs.py` to extract sequences having a complementary pair of hits.

You can clone the repo and run this script directly, or use the `Dockerfile` to create a container. See `Dockerfile` for dependencies if you run directly. Usage:

<pre>

run_cmpairs.bash fasta_file cm_file output_dir
  
      fasta_file is input sequences (typically contigs)
      cm_file is cm file for cmscan (specify - to use default dez.cm = DVR4 + hhrbz_dv4)
      output_dir is output directory (must not already exist)

</pre>

### Output files

Output files are `cmscan.tbl` and `pairs.fa`. The FASTA defline is updated with by appending a synopsis of the hits; here is an example:

<pre>
>NODE_290297_length_631_cov_5.012545 cm=hhrbz_dv4/499:582(4.4e-16)+,312:230(5.3e-16)-;
CTACACTCTTTCCCTACACGACGCTCTTCCGATCTCTTGGAACCACGGTCCAACTCCTTGACCTTAATCTCGATCTCATA
CAGGTCTTGCCAGGCGGCCCCCGCGGAAATTAGAACCTTCCGGTTCTTCTTTATCGCGAGAAGCTTCCTGAGAGCTTGTT
AAGAGAAACGGGATCGAGGGTTTGGAGAAAGACCAGGTTCTTAAGAAACTGTTCATTGGCTGCCTCGATTCGTTTCGTTG
GATCCCTTTCCAACTCATCAGTAGGTTTCAGACTATCTTCCATCTCGAAGAAATCCTTGGGTACCTATACGAATCTCCTT
CTTTATACCTTGCAACCGATTCGATGCGGATCCGGTTCTTGGAAAGCCACTTGCTTCCCGGCCAACGGCTTGGCGTTGCG
AGCACTTTGCTCGGCGCAGCCCCGCTTGGAACGCGAGAAGGGCAACCTTCCTCCCGAACCCGGTTCGAGGGTCGTTCGGA
GTAAAGAAAAAGGAGTTTCGATAATGGTAACCTTGGAAATTTTCTTGATGAAAGAAATTTCCGAAGCCATCCGAAGAGAA
GGATTGGGTCCCTTCGAAATCGAAAAGTGGCAACTAAGTTACAGAATCTTGGAACCACGGTCCAACTCCTT
</pre>

The defline is annotated by appending the model name(s) with paired hits. For each hit, the coordinates, strand and E-value are included. This will enable a short text "cartoon" with rbz and protein hits analagous to Serratus [p]summary files.

### EC2 workflow to build container and create AMI

AMI: Ubuntu Server 20.04 x86

Launch t2.micro instance and connect by ssh. Then run:

<pre>
sudo apt update
sudo snap install docker
sudo apt install awscli

git clone https://github.com/rcedgar/cmpairs.git

cd cmpairs
chmod +x *.bash
./build_container.bash
</pre>

Create AMI from EC2 console.

### Example EC2 workflow to run analysis on AMI

Launch the AMI created above.

Instance type: t2.micro works fine, typically takes from tens of minutes to a couple of hours per assembly.

<pre>
# Make directory /home/ubuntu/data
# Copy contigs from S3 to /home/ubuntu/data/SRR5252872.fa
# Delete directory /home/ubuntu/data/cmpairs/SRR5252872 if it already exists (error if it does)

sudo docker run \
  --mount type=bind,source=/home/ubuntu/data,target=/data \
  --rm -t rce-cmpairs \
  /cmpairs/run_cmpairs.bash /data/SRR5252872.fa - /data/cmpairs/SRR5252872
  
# Copy output directory /home/ubuntu/data/cmpairs/SRR5252872 to S3.
# Terminate instance.
</pre>
