import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from db_engine import create

engine = create()  # database connection created using SQLAlchemy library

enh_degree_ee = pd.read_sql("SELECT num FROM sahlen_enh_per_enh", con=engine)
p_degree_pp = pd.read_sql("SELECT num FROM sahlen_promo_per_promo", con=engine)
p_degree_pe = pd.read_sql("SELECT num FROM sahlen_frag_per_promo", con=engine)
e_degree_pe = pd.read_sql("SELECT num FROM sahlen_promo_per_frag", con=engine)

fig = plt.figure()
ax = fig.add_subplot(111)

binEdges = [i for i in range(60)]
y, binEdges = np.histogram(enh_degree_ee, bins=binEdges)
# bin_centers = 0.5 * (binEdges[1:] + binEdges[:-1])
y = y / y.sum()
line, = ax.plot(binEdges[1:59], y[1:], '-')
line.set_label("Enhancer degree in e-e, average=" + str(round(np.average(enh_degree_ee), 2)))

y, binEdges = np.histogram(e_degree_pe, bins=binEdges)
# bin_centers = 0.5 * (binEdges[1:] + binEdges[:-1])
y = y / y.sum()

line, = ax.plot(binEdges[1:59], y[1:], '-')
line.set_label("Enhancer degree in p-e, average=" + str(round(np.average(e_degree_pe), 2)))

y, binEdges = np.histogram(p_degree_pe, bins=binEdges)
# bin_centers = 0.5 * (binEdges[1:] + binEdges[:-1])
y = y / y.sum()

line, = ax.plot(binEdges[1:59], y[1:], '-')
line.set_label("Promoter degree in p-e, average=" + str(round(np.average(p_degree_pe), 2)))

y, binEdges = np.histogram(p_degree_pp, bins=binEdges)
# bin_centers = 0.5 * (binEdges[1:] + binEdges[:-1])
y = y / y.sum()

line, = ax.plot(binEdges[1:59], y[1:], '-')
line.set_label("Promoter degree in p-p, average=" + str(round(np.average(p_degree_pp), 2)))

plt.xlim([0, 15])
plt.legend()
plt.xlabel("Degree")
plt.ylabel("Sequences fraction")
plt.show()
