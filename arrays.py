import itertools
import numpy as np
import subprocess
from os.path import join
from os import listdir
from os.path import isfile

bases = ['A', 'C', 'G', 'T']
kmer = [''.join(c) for c in itertools.product(bases, repeat=4)]

mouse = "/home/kinga/Dokumenty/Studia/licencjat_old/mm9.2bit"


def make_array(path, filename, seq_type):
    mer_count = np.zeros_like(kmer)
    kmers_dict = {}
    print(filename)
    filepath = join(path, filename)
    get_sequence_and_4mers(filename, seq_type)
    h = open(filepath)

    for line1, line2 in itertools.zip_longest(*[h] * 2):
        mer = line2.strip("\n")
        count = int(line1.strip("\n").lstrip(">"))
        kmers_dict[mer] = count

    for i, mer2 in enumerate(kmer):
        if mer2 in kmers_dict:
            mer_count[i] = int(kmers_dict[mer2])
        else:
            mer_count[i] = 0
    return mer_count.astype(int)


def get_sequence_and_4mers(filename, seq_type):
    path2 = "/home/kinga/Dokumenty/Studia/licencjat_old/data/"
    lista = filename.split("_")
    chromo, start, end, sth = lista
    start = int(start)
    end = int(end)
    middle = start+((end-start)/2)
    if seq_type == "e":
        out = join(path2, "sahlen_enhancers/sequences/", filename[0:-10] + ".fa")
        out_jf = join("/home/kinga/Dokumenty/Studia/licencjat_old/data/sahlen_enhancers/jelly",
                      filename[0:-10] + ".jf")
        out_fasta = "/home/kinga/Dokumenty/Studia/licencjat_old/data/sahlen_enhancers/counts" \
                    + filename
    else:
        out = path2 + "sahlen_promoters/sequences/" + filename[0:-10] + ".fa"
        out_jf = join(path2, "sahlen_promoters/jelly", filename[0:-10] + ".jf")
        out_fasta = join(path2, "sahlen_promoters/counts", filename[0:-10] + "_counts.fa")

    if not isfile(out):
        subprocess.Popen(["/home/kinga/twoBitToFa", mouse, "stdout", "-seq=" + str(chromo),
                         "-start=" + str(int(middle - 500)), "-end=" + str(int(middle + 500))],
                         stdout=open(out, "w+"))
    if not isfile(out_jf):
        subprocess.Popen(["jellyfish count -m 4 -s 997 -o" + out_jf + " " + out], shell=True)
        subprocess.Popen(["jellyfish dump " + out_jf + " > " + out_fasta], shell=True)

    if not isfile(out_fasta):
        subprocess.Popen(["jellyfish dump " + out_jf + " > " + out_fasta], shell=True)
