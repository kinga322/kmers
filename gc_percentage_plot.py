import pandas as pd
import matplotlib.pyplot as plt
from db_engine import create

engine = create()  # database connection created using SQLAlchemy library

fig = plt.figure()
ax = fig.add_subplot(111)

for dataset in ["sahlen", "fantom", "rubin"]:
    promoters = pd.read_sql("SELECT GC_percentage, promoter_degree as degree "
                            "FROM %s_promoters_dinucleotides" % dataset, con=engine)
    enhancers = pd.read_sql("SELECT GC_percentage, enhancer_degree as degree "
                            "FROM %s_enhancers_dinucleotides" % dataset, con=engine)

    enhancers_average = enhancers.groupby("degree", as_index=False).agg({"GC_percentage": ['mean', 'std']})
    enhancers_average.columns = ["_".join(x) for x in enhancers_average.columns.ravel()]

    enhancers_average.to_csv("GC_content_%s_enhancers.csv" % dataset)
    line, = ax.plot(enhancers_average.degree_, enhancers_average.GC_percentage_mean)
    line.set_label("%s enhancers" % dataset.capitalize())
    # plt.title("Average GC%% %s enhancers" % dataset.capitalize())
    # plt.savefig("GC_content_%s_enhancers.png" % dataset)
    # plt.xlim([1, 10])
    # plt.ylim([40, 60])
    # plt.title("Average GC%% %s enhancers - zoom" % dataset.capitalize())
    # plt.savefig("GC_content_%s_enhancers_zoom.png" % dataset)
    # plt.clf()

    promoters_average = promoters.groupby("degree", as_index=False).agg({"GC_percentage":['mean', 'std']})
    promoters_average.columns = ["_".join(x) for x in promoters_average.columns.ravel()]
    promoters_average.to_csv("GC_content_%s_promoters.csv" % dataset)
    line, = ax.plot(promoters_average.degree_, promoters_average.GC_percentage_mean)
    line.set_label("%s promoters" % dataset.capitalize())
    # plt.title("Average GC%% %s promoters" % dataset.capitalize())
    # plt.savefig("GC_content_%s_promoters.png" % dataset)
    # plt.xlim([1, 10])
    # plt.ylim([40, 60])
    # plt.title("Average GC%% %s promoters - zoom" % dataset.capitalize())
    # plt.savefig("GC_content_%s_promoters_zoom.png" % dataset)
    # plt.clf()

    joined = pd.concat([promoters, enhancers])
    average_df = joined.groupby("degree", as_index=False).agg({"GC_percentage":['mean', 'std']})
    average_df.columns = ["_".join(x) for x in average_df.columns.ravel()]
    average_df.to_csv("GC_content_%s_all.csv" % dataset)
    line, = ax.plot(average_df.degree_, average_df.GC_percentage_mean)
    line.set_label("%s all sequences" % dataset.capitalize())
    # plt.title("Average GC%% %s all sequences" % dataset.capitalize())
    # plt.savefig("GC_content_%s_all.png" % dataset)
    # plt.xlim([1, 10])
    # plt.ylim([40,60])
    # plt.title("Average GC%% %s all sequences - zoom" % dataset.capitalize())
    # plt.savefig("GC_content_%s_all_zoom.png" % dataset)
    # plt.clf()

    promoters.to_csv("%s_promoters")

plt.xlim([1, 10])
plt.ylim([40, 60])
plt.legend(bbox_to_anchor=(1.05, 0.5), fontsize='small')
plt.show()