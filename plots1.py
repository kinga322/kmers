import pandas as pd
import matplotlib.pyplot as plt
from db_engine import create

engine = create()  # database connection created using SQLAlchemy library

dist = pd.read_sql_query("SELECT ABS(`Promoter_TSS`-`Fragment_start_coordinate`) "
                         "from sahlen_promoter_enhancer", engine)
dist.hist(bins=8000)
plt.xlim([0, 250000])
plt.title("Sahlen promoter-enhancer distance")
plt.show()

enh_length = pd.read_sql_query("SELECT ABS(Fragment_end_coordinate-Fragment_start_coordinate) "
                               "from sahlen_promoter_enhancer", engine)
enh_length.hist(bins=7000)
plt.xlim([0, 4000])
plt.title("Sahlen enhancer length")
plt.show()

frag = pd.read_sql_query('SELECT num FROM sahlen_frag_per_promo', engine)

frag.hist(bins=30)
plt.xlim([0, 60])
plt.title('Sahlen fragments per promoter')
plt.show()

promo = pd.read_sql_query("SELECT num FROM sahlen_promo_per_frag", engine)

promo.hist(bins=40)
plt.xlim([0, 15])
plt.title("Sahlen promoters per fragment")
plt.show()

enh_per_enh = pd.read_sql("SELECT num FROM sahlen_enh_per_enh", con=engine)
enh_per_enh.hist(bins=40)
plt.title("Sahlen enhancers per enhancer")
plt.xlim([0, 25])
plt.show()

enh_range_per_enh = pd.read_sql("SELECT MAX(`Fragment end coordinate.1`)-MIN(`Fragment start coordinate.1`) "
                                "AS enh_range "
                                "from sahlen_enhancer_enhancer "
                                "GROUP BY `Fragment chromosome`, `Fragment start coordinate`, "
                                "`Fragment end coordinate`", con=engine)

enh_range_per_enh.hist(bins=500)
plt.xlim([0, 500000])
plt.title("Sahlen enhancer range per enhancer (zoom)")
plt.show()

promo_range_per_promo = pd.read_sql("SELECT MAX(`Promoter TSS.1`)-MIN(`Promoter TSS.1`) AS promo_range "
                                    "from sahlen_promoter_promoter "
                                    "GROUP BY `Promoter chr`, `Promoter TSS`", con=engine)

promo_range_per_promo.hist(bins=300)
plt.xlim([0, 2000000])
plt.title("Sahlen promoter range per promoter (from TSS)")
plt.show()

enh_length = pd.read_sql_query("SELECT (Fragment_end_coordinate-Fragment_start_coordinate) as length "
                               "FROM sahlen_promoter_enhancer", engine)

enh_length.hist(bins=500)
plt.xlim([0, 4000])
plt.title("Enhancers length")
plt.show()