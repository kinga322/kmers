import pandas as pd
from numpy.linalg import norm
from arrays import make_array
from db_engine import create

engine = create()


engine.execute("CREATE TABLE sahlen_promo_per_promo SELECT `Promoter chr`, new_promo_start, new_promo_end, "
               "count(distinct `Promoter chr.1`, new_promo2_start, new_promo2_end) as "
               "num from sahlen_promoter_promoter group by `Promoter chr`, new_promo_start, new_promo_end", con=engine)

engine.execute("CREATE TABLE sahlen_range_promo_per_promo "
               "SELECT MAX(`Promoter TSS.1`)-MIN(`Promoter TSS.1`) "
               "AS promo_range, `Promoter TSS`, `Promoter chr` "
               "FROM sahlen_promoter_promoter "
               "GROUP BY `Promoter chr`, `Promoter TSS`")


dataset = "sahlen"
path = "/home/kinga/Dokumenty/Studia/licencjat_old/data/"

engine.execute("ALTER TABLE sahlen_promoter_promoter ADD kmer_distance FLOAT")

sahlen = pd.read_sql("SELECT new_promo_start, new_promo_end, new_promo2_start, new_promo2_end, "
                     "`Promoter chr`, `Promoter chr.1` from "
                     "sahlen_promoter_promoter "
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

    sql_query = "UPDATE sahlen_promoter_promoter SET kmer_distance=" + str(kmer_distance) + " WHERE `Promoter chr`='" \
                + str(row.promoter_chr) + "' AND new_promo_start=" + str(row.new_promo_start) + " AND new_promo_end=" \
                + str(row.new_promo_end) +\
                " AND `Promoter chr.1`='" + str(row.promoter_chr1) + "' AND new_promo2_start=" \
                + str(row.new_promo2_start) + \
                " AND new_promo2_end=" + str(row.new_promo2_end)

    engine.execute(sql_query, con=engine)
