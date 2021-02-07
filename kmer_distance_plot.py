import matplotlib.pyplot as plt
import pandas as pd
from db_engine import create
import seaborn as sns
import numpy as np
import itertools


sns.set(color_codes=True)

engine = create()

binEdges = np.array(range(20, 290, 10))
print(binEdges)
bin_centers = 0.5 * (binEdges[1:] + binEdges[:-1])
print(bin_centers)


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

fig = plt.figure()
ax = fig.add_subplot(111)

dataframe = pd.DataFrame(columns=["degree", "avg_kmer_distance", "std"])

for i in nums:

    # query1 = "SELECT `AVG(similarity)` FROM sahlen_enhancers WHERE num={}".format(i)
    # print(query)
    # df1 = pd.read_sql(query1, con=engine)

    # print(df)
    
    query2 = "SELECT `AVG(similarity)` FROM sahlen_enhancers WHERE num={}".format(i)
    # print(query)
    df2 = pd.read_sql(query2, con=engine)
    """
    y, binEdges = np.histogram(df1, bins=binEdges)

    y_norm = y / y.sum()
    line, = ax.plot(bin_centers, y_norm, '-', marker='o')
    line.set_label("{}, średnia={}".format(i, round(np.average(df1), 2)))
    """
    y, binEdges = np.histogram(df2, bins=binEdges)
    y = y / y.sum()

    line, = ax.plot(bin_centers, y, '-', marker='o')
    line.set_label("{}, średnia={}".format(i, round(np.average(df2), 2)))

    dataframe = dataframe.append({"degree":i, "avg_kmer_distance":np.average(df2), "std":df2.std()[0]}, ignore_index=True)

dataframe.to_csv("enhancers.csv")

plt.xticks(bin_centers, pairwise(binEdges), rotation=80)
plt.xlim([20, 160])
plt.legend(title="Liczba enhancerów \n oddziałujących z promotorem")
# plt.title("Average k-mer distance promoter, grouped by enhancers")
plt.xlabel("Odległość k-merowa")
plt.ylabel("Odsetek sekwencji")
plt.show()

similarity_pe = pd.read_sql("SELECT kmer_distance FROM sahlen_promoter_enhancer", con=engine)
similarity_pp = pd.read_sql("SELECT similarity FROM sahlen_promoter_promoter", con=engine)
similarity_ee = pd.read_sql("SELECT similarity FROM sahlen_enhancer_enhancer", con=engine)

fig = plt.figure()
ax = fig.add_subplot(111)

y, bin_edges = np.histogram(similarity_pe, bins=20)
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
y = y / y.sum()
line, = ax.plot(bin_centers, y, '-')
line.set_label("K-mer distance for p-e")

y, bin_edges = np.histogram(similarity_pp, bins=bin_edges)
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
y = y / y.sum()
line, = ax.plot(bin_centers, y, '-')
line.set_label("K-mer distance for p-p")

y, bin_edges = np.histogram(similarity_ee, bins=bin_edges)
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
y = y / y.sum()
line, = ax.plot(bin_centers, y, '-')
line.set_label("K-mer distance for e-e")

plt.legend()
plt.xlim([0, 150])
plt.show()


enh_dist = pd.read_sql("SELECT `AVG(similarity)` FROM sahlen_enhancers", con=engine)
promo_dist = pd.read_sql("SELECT `AVG(similarity)` FROM sahlen_promoters", con=engine)

y, bin_edges = np.histogram(enh_dist, bins=range(0, 200, 10))
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
y_norm = y / y.sum()
line, = plt.plot(bin_centers, y_norm, "-")
line.set_label("Po enhancerach, średnia=" + str(round(np.average(enh_dist), 2)))

y, bin_edges = np.histogram(promo_dist, bins=bin_edges)
y_norm = y / y.sum()
line, = plt.plot(bin_centers, y_norm, "-")
line.set_label("Po promotorach, średnia=" + str(round(np.average(promo_dist), 2)))

plt.xticks(bin_centers, pairwise(bin_edges), rotation=80)

plt.xlim([0, 200])
plt.xlabel("Średnia odległość k-merowa")
plt.ylabel("Odsetek sekwencji")
plt.legend()
plt.show()
