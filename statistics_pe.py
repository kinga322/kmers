import pandas as pd
from db_engine import create
from arrays import make_array
from numpy.linalg import norm

engine = create()  # database connection created using SQLAlchemy library

# Count distance on genome

engine.execute("ALTER TABLE sahlen_promoter_enhancer ADD COLUMN genome_distance INT")
engine.execute("UPDATE sahlen_promoter_enhancer SET genome_distance = "
               "ABS(Fragment_end_coordinate-(Fragment_end_coordinate-Fragment_start_coordinate)/2 "  # enhancer middle
               "- Promoter_TSS) WHERE Promoter_chr=Fragment_chromosome")


# Count degree of sequences

engine.execute("CREATE TABLE sahlen_frag_per_promo "
               "SELECT Promoter_chr, Promoter_TSS, new_promo_start, new_promo_end, "
               "count(distinct Fragment_chromosome, new_enh_start, new_enh_end) "
               "AS degree "
               "FROM sahlen_promoter_enhancer "
               "GROUP BY Promoter_chr, new_promo_start, new_promo_end")

engine.execute("CREATE TABLE sahlen_promo_per_frag "
               "SELECT Fragment_chromosome, Fragment_start_coordinate, Fragment_end_coordinate, "
               "new_enh_start, new_enh_end, "
               "count(distinct Promoter_chr, new_promo_start, new_promo_end) "
               "AS degree "
               "FROM sahlen_promoter_enhancer "
               "GROUP BY Fragment_chromosome, new_enh_start, new_enh_end")

engine.execute("ALTER TABLE sahlen_promoter_enhancer ADD (promoter_degree INT, enhancer_degree INT)")

engine.execute("UPDATE sahlen_promoter_enhancer JOIN sahlen_promo_per_frag "
               "ON sahlen_promoter_enhancer.new_enh_start=sahlen_promo_per_frag.new_enh_start "
               "AND sahlen_promoter_enhancer.new_enh_end=sahlen_promo_per_frag.new_enh_end "
               "AND sahlen_promoter_enhancer.Fragment_chromosome=sahlen_promo_per_frag.Fragment_chromosome "
               "SET sahlen_promoter_enhancer.enhancer_degree=sahlen_promo_per_frag.num")

engine.execute("UPDATE sahlen_promoter_enhancer JOIN sahlen_frag_per_promo "
               "ON sahlen_promoter_enhancer.new_promo_start=sahlen_frag_per_promo.new_promo_start "
               "AND sahlen_promoter_enhancer.new_promo_end=sahlen_frag_per_promo.new_promo_end "
               "AND sahlen_promoter_enhancer.Promoter_chr=sahlen_frag_per_promo.Promoter_chr "
               "SET sahlen_promoter_enhancer.promoter_degree=sahlen_frag_per_promo.num")

dataset = "sahlen"
path = "/home/kinga/Dokumenty/Studia/licencjat_old/data/"

engine.execute("ALTER TABLE sahlen_promoter_enhancer ADD kmer_distance FLOAT")

sahlen = pd.read_sql("SELECT new_promo_start, new_promo_end, new_enh_start, new_enh_end, "
                     "Promoter_chr, Fragment_chromosome from "
                     "sahlen_promoter_enhancer"
                     # where kmer_distance is null or kmer_distance=0
                     , con=engine)

sahlen.columns = sahlen.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('.', '')

for row in sahlen.itertuples():
    print(row.Index)
    filename_promo1 = row.promoter_chr+"_"+str(row.new_promo_start)+"_"+str(row.new_promo_end)+"_counts.fa"
    filename_promo2 = row.promoter_chr1 + "_" + str(row.new_promo2_start) + "_" + str(row.new_promo2_end)+"_counts.fa"
    array_promo1 = make_array(path+dataset+"_promoters/counts/", filename_promo1, "p")
    array_promo2 = make_array(path+dataset+"_promoters/counts/", filename_promo2, "p")

    kmer_distance = norm(array_promo1-array_promo2)

    sql_query = "UPDATE sahlen_promoter_enhancer SET kmer_distance=" + str(kmer_distance) + " WHERE Promoter_chr ='" \
                + str(row.promoter_chr) + "' AND new_promo_start=" + str(row.new_promo_start) + " AND new_promo_end=" \
                + str(row.new_promo_end) +\
                " AND Fragment_chromosome='" + str(row.promoter_chr1) + "' AND new_enh_start=" \
                + str(row.new_promo2_start) + \
                " AND new_enh_end=" + str(row.new_promo2_end)

    engine.execute(sql_query, con=engine)


