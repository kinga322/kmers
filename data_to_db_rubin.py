from db_engine import create
import numpy as np
import pandas as pd

engine = create()  # database connection created using SQLAlchemy library

rubin_promoter_enhancer = pd.read_csv("/home/kinga/Dokumenty/Studia/licencjat_old/data/Rubin"
                                      "/GSE84660_CHiC_contacts_b2g.bed", sep="\t")
rubin_promoter_enhancer.rename(columns=lambda x: x.strip(), inplace=True)

engine.execute("CREATE TABLE rubin_promo_per_enh "
               "SELECT otherEnd_start, otherEnd_end, otherEnd_chr, "
               "count(DISTINCT bait_start, bait_end, bait_chr) as num "
               "FROM rubin_promoter_enhancer "
               "GROUP BY otherEnd_start, otherEnd_end, otherEnd_chr")

engine.execute("CREATE TABLE rubin_enh_per_promo "
               "SELECT bait_start, bait_end, bait_chr, " 
               "count(DISTINCT otherEnd_start, otherEnd_end, otherEnd_chr) as num "
               "FROM rubin_promoter_enhancer "
               "GROUP BY bait_start, bait_end, bait_chr")

engine.execute("ALTER TABLE rubin_promoter_enhancer ADD COLUMN (new_promo_start int, "
               "new_promo_end int, new_enh_start int, new_enh_end int)")
engine.execute("UPDATE rubin_promoter_enhancer SET new_promo_start=bait_start+((bait_end-bait_start)/2)-500")
engine.execute("UPDATE rubin_promoter_enhancer SET new_promo_end=bait_start+((bait_end-bait_start)/2)+500")
engine.execute("UPDATE rubin_promoter_enhancer SET new_enh_start=otherEnd_start+((otherEnd_end-otherEnd_start)/2)-500")
engine.execute("UPDATE rubin_promoter_enhancer SET new_enh_end=otherEnd_start+((otherEnd_end-otherEnd_start)/2)+500")

engine.execute("ALTER TABLE rubin_promoter_enhancer ADD COLUMN (promoter_degree smallint, "
               "enhancer_degree smallint)")

for i in np.arange(0, 250, 3):
    start = i * 1000000
    end = (i + 3) * 1000000
    query = "UPDATE rubin_promoter_enhancer JOIN rubin_promo_per_enh " \
            "ON rubin_promoter_enhancer.otherEnd_start=rubin_promo_per_enh.otherEnd_start " \
            "AND rubin_promoter_enhancer.otherEnd_end=rubin_promo_per_enh.otherEnd_end " \
            "AND rubin_promoter_enhancer.otherEnd_chr=rubin_promo_per_enh.otherEnd_chr " \
            "SET rubin_promoter_enhancer.enhancer_degree=rubin_promo_per_enh.num " \
            "WHERE rubin_promoter_enhancer.otherEnd_start BETWEEN %s and %s " \
            "AND enhancer_degree is NULL" % (start, end)
    print(query)
    engine.execute(query)
    print(i)

for i in np.arange(0, 250, 3):
    start = i * 1000000
    end = (i + 3) * 1000000
    query = "UPDATE rubin_promoter_enhancer JOIN rubin_enh_per_promo " \
            "ON rubin_promoter_enhancer.bait_start=rubin_enh_per_promo.bait_start " \
            "AND rubin_promoter_enhancer.bait_end=rubin_enh_per_promo.bait_end " \
            "AND rubin_promoter_enhancer.bait_chr=rubin_enh_per_promo.bait_chr " \
            "SET rubin_promoter_enhancer.promoter_degree=rubin_enh_per_promo.num " \
            "WHERE rubin_promoter_enhancer.bait_start BETWEEN %s and %s " \
            "AND promoter_degree is NULL" % (start, end)
    print(query)
    engine.execute(query)
    print(i)
