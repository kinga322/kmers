import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from db_engine import create

engine = create()  # database connection created using SQLAlchemy library

enh_range_per_enh = pd.read_sql("SELECT sahlen_range_frag_per_frag.frag_range FROM sahlen_enh_per_enh "
                                "JOIN sahlen_range_frag_per_frag "
                                "ON sahlen_enh_per_enh.`Fragment chromosome`=sahlen_range_frag_per_frag.`Fragment chromosome` "
                                "and sahlen_enh_per_enh.`Fragment start coordinate`=sahlen_range_frag_per_frag.`Fragment start coordinate` "
                                "WHERE num>1", con=engine)
enh_range_per_promo = pd.read_sql("SELECT sahlen_range_frag_per_promo.pos_range FROM sahlen_frag_per_promo "
                                  "JOIN sahlen_range_frag_per_promo "
                                  "ON sahlen_frag_per_promo.Promoter_chr=sahlen_range_frag_per_promo.Promoter_chr "
                                  "AND sahlen_frag_per_promo.Promoter_TSS=sahlen_range_frag_per_promo.Promoter_TSS "
                                  "WHERE num>1", con=engine)
promo_range_per_enh = pd.read_sql("SELECT promo_range FROM sahlen_promo_per_frag "
                                  "JOIN sahlen_range_promo_per_frag "
                                  "ON sahlen_promo_per_frag.Fragment_chromosome=sahlen_range_promo_per_frag.Fragment_chromosome "
                                  "and sahlen_promo_per_frag.Fragment_start_coordinate=sahlen_range_promo_per_frag.Fragment_start_coordinate "
                                  "WHERE num>1", con=engine)
promo_range_per_promo = pd.read_sql("SELECT promo_range FROM sahlen_promo_per_promo "
                                    "JOIN sahlen_range_promo_per_promo "
                                    "ON sahlen_promo_per_promo.`Promoter TSS`=sahlen_range_promo_per_promo.`Promoter TSS` "
                                    "and sahlen_promo_per_promo.`Promoter chr`=sahlen_range_promo_per_promo.`Promoter chr` "
                                    "WHERE num>1", con=engine)

fig = plt.figure()
ax = fig.add_subplot(111)

y, binEdges = np.histogram(enh_range_per_enh, bins=2000)
print(binEdges)
bin_centers = 0.5 * (binEdges[1:] + binEdges[:-1])

y_norm = y / y.sum()
line, = ax.plot(bin_centers, y_norm, '-')
line.set_label("Zakres enhancerów dla e-e")  # , średnia {}".format(round(np.average(enh_range_per_enh), 0)))

y, binEdges = np.histogram(enh_range_per_promo, bins=binEdges)
y_norm = y / y.sum()
line, = ax.plot(bin_centers, y_norm, '-')
line.set_label("Zakres enhancerów dla p-e")  # , średnia {}".format(round(np.average(enh_range_per_promo), 0)))

y, binEdges = np.histogram(promo_range_per_enh, bins=binEdges)
y_norm = y / y.sum()
line, = ax.plot(bin_centers, y_norm, '-')
line.set_label("Zakres promotorów dla p-e")  # , średnia {}".format(round(np.average(promo_range_per_enh), 0)))

y, binEdges = np.histogram(promo_range_per_promo, bins=binEdges)
y_norm = y / y.sum()
line, = ax.plot(bin_centers, y_norm, '-')
line.set_label("Zakres promotorów dla p-p")  # , średnia {}".format(round(np.average(promo_range_per_promo), 0)))

plt.xlim([0, 500000])
plt.xlabel("Odległość (bp)")
plt.ylabel("Odsetek sekwencji")
plt.legend()
plt.show()
