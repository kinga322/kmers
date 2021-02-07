from db_engine import create, get_cursor
import os
import itertools

engine = create()  # database connection created using SQLAlchemy library
connection, cursor = get_cursor()

bases = ['A', 'C', 'G', 'T']
dinucleotides = [''.join(c) for c in itertools.product(bases, repeat=2)]


def count_dinucleotides(dataset, seq_type, chromo_col):
    directory = "/home/kinga/Dokumenty/Studia/licencjat_old/data/%s_%s/sequences/" % (dataset, seq_type)
    files = os.listdir(directory)
    table_name = "%s_%s_dinucleotides" % (dataset, seq_type)
    for i, file in enumerate(files):
        print(i/len(files))
        chromo, start, end = file.strip(".fa").split("_")
        h = open(directory + file)
        next(h)
        seq = h.read().replace("\n", "").upper()
        kmers_dict = {}
        for di in dinucleotides:
            count = substr_count(seq, di)
            kmers_dict[di] = count
            if di not in kmers_dict.keys():
                kmers_dict[di] = 0
        stmt = ""
        for k, v in kmers_dict.items():
            stmt += "{}={}, ".format(k, v)
        stmt = stmt[:-2]
        if seq_type == "enhancers":
            query = "UPDATE %s SET %s WHERE %s='%s' " \
                    "AND new_enh_start=%s AND new_enh_end=%s" \
                    % (table_name, stmt, chromo_col, chromo, start, end)
        elif seq_type == "promoters":
            query = "UPDATE %s SET %s WHERE %s='%s' " \
                    "AND new_promo_start=%s AND new_promo_end=%s" \
                    % (table_name, stmt, chromo_col, chromo, start, end)
        print(query)
        engine.execute(query)


def substr_count(st, sub):

    _st = st[::]
    try:
        start = _st.index(sub)
    except:
        return 0
    cnt = 0

    while start is not None:
        cnt += 1
        try:
            _st = _st[start + len(sub) - 1:]
            start = _st.index(sub)
        except (ValueError, IndexError):
            return cnt

    return cnt


# count_dinucleotides("sahlen_promoters", "Promoter_chr")
# count_dinucleotides("sahlen_enhancers", "Fragment_chromosome")
# count_dinucleotides("fantom_enhancers", "enhancer_chr")
# count_dinucleotides("fantom_promoters", "promoter_chr")
# count_dinucleotides("rubin", "promoters", "bait_chr")
count_dinucleotides("rubin", "enhancers", "otherEnd_chr")


def count_gc_percentage(dataset, seq_type, chromo_col):
    directory = "/home/kinga/Dokumenty/Studia/licencjat_old/data/%s_%s/sequences/" % (dataset, seq_type)
    files = os.listdir(directory)
    table_name = "%s_%s_dinucleotides" % (dataset, seq_type)
    for i, file in enumerate(files):
        print(i, len(files), i / len(files))
        chromo, start, end = file.strip(".fa").split("_")
        h = open(directory + file)
        next(h)
        seq = h.read().replace("\n", "").upper()
        g = seq.count("G")
        c = seq.count("C")
        gc_perc = (g + c)/10
        if seq_type == "enhancers":
            query = "UPDATE %s SET GC_percentage=%s " \
                    " WHERE %s='%s' " \
                    "AND new_enh_start=%s AND new_enh_end=%s" \
                    % (table_name, gc_perc, chromo_col, chromo, start, end)
        elif seq_type == "promoters":
            query = "UPDATE %s SET GC_percentage=%s " \
                    " WHERE %s='%s' " \
                    "AND new_promo_start=%s AND new_promo_end=%s" \
                    % (table_name, gc_perc, chromo_col, chromo, start, end)
        print(query)
        cursor.execute(query)
        if i % 100 == 0:
            print("commit")
            connection.commit()


# count_gc_percentage("sahlen", "promoters", "Promoter_chr")
# count_gc_percentage("sahlen", "enhancers", "Fragment_chromosome")
# count_gc_percentage("fantom", "enhancers", "enhancer_chr")
# count_gc_percentage("fantom", "promoters", "promoter_chr")
# count_gc_percentage("rubin", "promoters", "bait_chr")
count_gc_percentage("rubin", "enhancers", "otherEnd_chr")
