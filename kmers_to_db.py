import itertools
import pandas as pd
from db_engine import get_cursor, create

engine = create()

bases = ['A', 'C', 'G', 'T']
kmers = [''.join(c) for c in itertools.product(bases, repeat=4)]
"""
for kmer in kmers:
    engine.execute("ALTER TABLE sahlen_enhancers_from_pe ADD COLUMN " + kmer + " INT")

for kmer in kmers:
    engine.execute("ALTER TABLE sahlen_promoters_from_pe ADD COLUMN " + kmer + " INT")
"""
path = "/home/kinga/Dokumenty/Studia/licencjat_old/data/sahlen_promoters/counts/"
connection, cursor = get_cursor()


def from_filename(filename):
    print(filename)
    chromo, start, end, a = filename.split("_")
    from_file_to_db(chromo, str(start), str(end), filename)


def from_dataframe(row):
    chromo = row[1]
    start = str(row.new_promo_start)
    end = str(row.new_promo_end)
    filename = chromo + "_" + start + "_" + end + "_counts.fa"
    from_file_to_db(chromo, start, end, filename)


def from_file_to_db(chromo, start, end, filename):
    h = open(path + filename)
    kmers_dict = kmers_dict_from_file(h)
    kmers_to_db(chromo, start, end, kmers_dict)


def kmers_dict_from_file(h):
    kmers_dict = {}
    for line1, line2 in itertools.zip_longest(*[h] * 2):
        kmer = line2.strip()
        count = int(line1.strip().lstrip(">"))
        kmers_dict[kmer] = count
    for kmer in kmers:
        if kmer not in kmers_dict.keys():
            kmers_dict[kmer] = 0
    return kmers_dict


def kmers_to_db(chromo, start, end, kmers_dict):
    stmt = ""
    for k, v in kmers_dict.items():
        stmt += "{}={}, ".format(k, v)

    stmt = stmt[:-2]
    query = "UPDATE sahlen_promoters_from_pe SET " + stmt + " WHERE Promoter_chr='" + chromo + \
            "' AND new_promo_start=" + start + " AND new_promo_end=" + end
    print(query)
    cursor.execute(query)


enhancers = pd.read_sql("SELECT Promoter_chr, new_promo_start, new_promo_end FROM sahlen_promoters_from_pe",
                        con=engine)
for row in enhancers.itertuples():
    print(row[0]*100/len(enhancers))
    try:
        from_dataframe(row)
    except FileNotFoundError:
        print(row)
    if row[0] % 100 == 0:
        connection.commit()
