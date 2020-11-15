import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from db_engine import create

engine = create()  # database connection created using SQLAlchemy library

sahlen_pe = pd.read_sql("SELECT pandas_index, promoter_degree, enhancer_degree, kmer_distance "
                        "FROM sahlen_promoter_enhancer", con=engine)

max_promo = max(sahlen_pe["promoter_degree"])
max_enh = max(sahlen_pe["enhancer_degree"])

points = np.zeros([140, 140])

for promo_degree, enh_degree in [(x, y) for x in range(1, 11) for y in range(1, 11)]:
    print(promo_degree, enh_degree)
    kmer_distance_df = pd.read_sql("SELECT kmer_distance FROM sahlen_promoter_enhancer WHERE promoter_degree="
                                   + str(promo_degree) + " AND enhancer_degree=" + str(enh_degree), con=engine)
    try:
        kmer_distance_avg = np.average(kmer_distance_df["kmer_distance"])
    except ZeroDivisionError:
        kmer_distance_avg = 0
    print(kmer_distance_avg)
    points[promo_degree][enh_degree] = kmer_distance_avg
    """index = interaction.pandas_index
    print(index)
    promoters_degree[index] = interaction.promoter_degree
    enhancers_degree[index] = interaction.enhancer_degree
    colors[index] = interaction.kmer_distance
"""
plt.imshow(points, vmin=50, vmax=75, cmap="Greys", aspect="auto")
plt.xlabel("Enhancer degree")
plt.ylabel("Promoter degree")
plt.xlim([0.5, 10.5])
plt.ylim([0.5, 10.5])
plt.xticks(range(1, 11))
plt.yticks(range(1, 11))
plt.colorbar()
plt.savefig("heatmap1.svg", format="svg")

"""
create table sahlen_degrees
select promoter_degree, enhancer_degree, count(*) from sahlen_promoter_enhancer group by promoter_degree, enhancer_degree
"""

points = np.zeros([140, 140])
degrees = pd.read_sql("select * from sahlen_degrees", con=engine)

for row in degrees.itertuples():
    promo_degree = int(row.promoter_degree)
    enh_degree = int(row.enhancer_degree)
    points[promo_degree][enh_degree] = row.count/degrees["count"].sum()

a = np.ma.masked_where(points == 0, points)

#a = a[1:, 1:]
cmap = plt.cm.nipy_spectral
cmap.set_bad(color="red")
plt.imshow(a, cmap=cmap, aspect="auto")#, norm=colors.LogNorm())
plt.xlabel("Enhancer degree")
plt.ylabel("Promoter degree")
plt.xlim([0.5, 10.5])
plt.ylim([0.5, 10.5])
plt.xticks(range(1, 11))
plt.yticks(range(1, 11))
plt.colorbar()
plt.savefig("heatmap2.svg", format="svg")