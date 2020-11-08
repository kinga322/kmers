import pandas as pd
from db_engine import create
from arrays import make_array
from numpy.linalg import norm

engine = create()  # database connection created using SQLAlchemy library

dataset = "sahlen"
path = "/home/kinga/Dokumenty/Studia/licencjat_old/data/"

# Calculate k-mer distance

engine.execute("ALTER TABLE sahlen_enhancer_enhancer ADD kmer_distance FLOAT")

sahlen = pd.read_sql("SELECT new_enh_start, new_enh_end, new_enh1_start, new_enh2_end, "
                     "`Fragment chromosome`, `Fragment chromosome.1` from "
                     "sahlen_enhancer_enhancer", con=engine)


sahlen.columns = sahlen.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('.', '')

for row in sahlen.itertuples():
    print(row.Index)
    filename_promo1 = row.promoter_chr+"_"+str(row.new_promo_start)+"_" \
        + str(row.new_promo_end)+"_counts.fa"
    filename_promo2 = row.promoter_chr1 + "_" + str(row.new_promo2_start) + "_" \
        + str(row.new_promo2_end)+"_counts.fa"
    array_promo1 = make_array(path+dataset+"_promoters/counts/", filename_promo1, "p")
    array_promo2 = make_array(path+dataset+"_promoters/counts/", filename_promo2, "p")

    kmer_distance = norm(array_promo1-array_promo2)

    sql_query = "UPDATE sahlen_promoter_promoter SET kmer_distance=" + str(kmer_distance) + \
                " WHERE `Promoter chr`='" + str(row.promoter_chr) \
                + "' AND new_promo_start=" + str(row.new_promo_start) + \
                " AND new_promo_end=" + str(row.new_promo_end) +\
                " AND `Promoter chr.1`='" + str(row.promoter_chr1) \
                + "' AND new_promo2_start=" + str(row.new_promo2_start) + \
                " AND new_promo2_end=" + str(row.new_promo2_end)

    engine.execute(sql_query, con=engine)
