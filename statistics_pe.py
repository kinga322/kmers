import pandas as pd
from db_engine import create

engine = create()  # database connection created using SQLAlchemy library

# Count distance on genome

engine.execute("ALTER TABLE sahlen_promoter_enhancer ADD COLUMN genome_distance INT")
engine.execute("UPDATE sahlen_promoter_enhancer SET genome_distance = "
               "ABS(Fragment_end_coordinate-(Fragment_end_coordinate-Fragment_start_coordinate)/2 "  # enhancer middle
               "- Promoter_TSS) WHERE Promoter_chr=Fragment_chromosome")


# Count degree of sequences

engine.execute("CREATE TABLE sahlen_promoters_from_pe "
               "SELECT Promoter_chr, new_promo_start, new_promo_end, "
               "count(distinct Fragment_chromosome, new_enh_start, new_enh_end) "
               "AS degree "
               "FROM sahlen_promoter_enhancer "
               "GROUP BY Promoter_chr, new_promo_start, new_promo_end")

engine.execute("CREATE TABLE sahlen_enhancers_from_pe "
               "SELECT Fragment_chromosome, new_enh_start, new_enh_end, "
               "count(distinct Promoter_chr, new_promo_start, new_promo_end) "
               "AS degree "
               "FROM sahlen_promoter_enhancer "
               "GROUP BY Fragment_chromosome, new_enh_start, new_enh_end")

