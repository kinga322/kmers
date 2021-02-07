import pandas as pd
from db_engine import create
import numpy as np

engine = create()  # database connection created using SQLAlchemy library
"""
engine.execute("ALTER TABLE fantom ADD COLUMN (new_promo_start int, new_promo_end int,"
               "new_enh_start int, new_enh_end int, promoter_degree smallint, "
               "enhancer_degree smallint)")

engine.execute("UPDATE fantom "
               "SET new_promo_start=FLOOR(promoter_start+((promoter_end-promoter_start)/2))-500")
engine.execute("UPDATE fantom "
               "SET new_promo_end=FLOOR(promoter_start+((promoter_end-promoter_start)/2))+500")

engine.execute("UPDATE fantom "
               "SET new_enh_start=FLOOR(enhancer_start+((enhancer_end-enhancer_start)/2))-500")
print("start updated")
engine.execute("UPDATE fantom "
               "SET new_enh_end=FLOOR(enhancer_start+((enhancer_end-enhancer_start)/2))+500")
print("end updated")

for i in np.arange(10, 100, 0.25):
    start = int(i*1000000)
    end = int(i*2000000)
    query = "UPDATE fantom JOIN fantom_promo_per_enh " \
            "ON fantom.enhancer_start=fantom_promo_per_enh.enhancer_start " \
            "AND fantom.enhancer_end=fantom_promo_per_enh.enhancer_end " \
            "AND fantom.enhancer_chr=fantom_promo_per_enh.enhancer_chr " \
            "SET fantom.enhancer_degree=fantom_promo_per_enh.num " \
            "WHERE fantom.enhancer_start BETWEEN %s and %s " \
            "AND enhancer_degree is NULL" % (start, end)
    print(query)
    engine.execute(query)
    print(i)
    """
for i in np.arange(0, 251, 3):
    start = i*1000000
    end = start + 3000000
    query = "UPDATE fantom JOIN fantom_enh_per_promo " \
            "ON fantom.promoter_start=fantom_enh_per_promo.promoter_start " \
            "AND fantom.promoter_end=fantom_enh_per_promo.promoter_end " \
            "AND fantom.promoter_chr=fantom_enh_per_promo.promoter_chr " \
            "SET fantom.promoter_degree=fantom_enh_per_promo.num " \
            "WHERE fantom.promoter_start BETWEEN %s and %s " \
            "AND fantom.promoter_degree IS NULL" % (start, end)
    print(query)
    engine.execute(query)

