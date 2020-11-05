"""
Import data from Supplementary Table 5
https://genomebiology.biomedcentral.com/articles/10.1186/s13059-015-0727-9
"""
import pandas as pd
from db_engine import create

engine = create()  # database connection created using SQLAlchemy library

sahlen_pe = pd.read_excel('home/kinga/Dokumenty/Studia/Licencjat/sahlen.xlsx',
                          sheet_name=1, skiprows=1)
sahlen_pe.columns = sahlen_pe.columns.str.strip().str.lower().str.replace(' ', '_')

sahlen_pe.to_sql(con=engine, name='sahlen_promoter_enhancer',
                 index_label='pandas_index')


# Calculate new start and end for fragments of length 1000


engine.execute("ALTER TABLE sahlen_promoter_enhancer ADD new_promo_start INT")
engine.execute("ALTER TABLE sahlen_promoter_enhancer ADD new_promo_end INT")
engine.execute("ALTER TABLE sahlen_promoter_enhancer ADD new_enh_start INT")
engine.execute("ALTER TABLE sahlen_promoter_enhancer ADD new_enh_end INT")

sql_query1 = "UPDATE sahlen_promoter_enhancer SET new_promo_start=`Promoter TSS`-500"
sql_query2 = "UPDATE sahlen_promoter_enhancer SET new_promo_end=`Promoter TSS`+500"

engine.execute(sql_query1)
engine.execute(sql_query2)


engine.execute("ALTER TABLE sahlen_promoter_enhancer ADD new_enh_start INT")
engine.execute("ALTER TABLE sahlen_promoter_enhancer ADD new_enh_end INT")

sql_query1 = "UPDATE sahlen_promoter_enhancer " \
            "SET new_enh_start = Fragment_start_coordinate+((Fragment_end_coordinate" \
             "-`Fragment_start_coordinate`)/2)-500"

sql_query2 = "UPDATE sahlen_promoter_enhancer " \
            "SET new_enh_end = Fragment_end_coordinate-((Fragment_end_coordinate" \
             "-Fragment_start_coordinate)/2)+500"

engine.execute(sql_query1)
engine.execute(sql_query2)


sahlen_pp = pd.read_excel('home/kinga/Dokumenty/Studia/Licencjat/sahlen.xlsx',
                          sheet_name=2, skiprows=1)

sahlen_pp.columns = sahlen_pp.columns.str.strip().str.lower().str.replace(' ', '_')

sahlen_pp.to_sql(con=engine, name='sahlen_promoter_promoter',
                 index_label='pandas_index')


engine.execute("ALTER TABLE sahlen_promoter_promoter ADD new_promo_start INT")
engine.execute("ALTER TABLE sahlen_promoter_promoter ADD new_promo_end INT")
engine.execute("ALTER TABLE sahlen_promoter_promoter ADD new_promo2_start INT")
engine.execute("ALTER TABLE sahlen_promoter_promoter ADD new_promo2_end INT")
sql1 = "UPDATE sahlen_promoter_promoter SET new_promo_start=`Promoter TSS`-500"
sql2 = "UPDATE sahlen_promoter_promoter SET new_promo_end=`Promoter TSS`+500"
sql3 = "UPDATE sahlen_promoter_promoter SET new_promo2_start=`Promoter TSS.1`-500"
sql4 = "UPDATE sahlen_promoter_promoter SET new_promo2_end=`Promoter TSS.1`+500"

for query in [sql1, sql2, sql3, sql4]:
    engine.execute(query)


sahlen_ee = pd.read_excel('home/kinga/Dokumenty/Studia/Licencjat/sahlen.xlsx',
                          sheet_name=3, skiprows=1)

sahlen_ee.columns = sahlen_pe.columns.str.strip().str.lower().str.replace(' ', '_')

sahlen_ee.to_sql(con=engine, name='sahlen_enhancer_enhancer',
                 index_label='pandas_index')

engine.execute("ALTER TABLE sahlen_enhancer_enhancer ADD new_enh_start INT")
engine.execute("ALTER TABLE sahlen_enhancer_enhancer ADD new_enh_end INT")

sql_query1 = "UPDATE sahlen_enhancer_enhancer " \
            "SET new_enh_start = `Fragment start coordinate`+" \
             "((`Fragment end coordinate`-`Fragment start coordinate`)/2)-501"

sql_query2 = "UPDATE sahlen_enhancer_enhancer " \
            "SET new_enh_end = `Fragment end coordinate`-" \
             "((`Fragment end coordinate`-`Fragment start coordinate`)/2)+499"

engine.execute(sql_query1)
engine.execute(sql_query2)

engine.execute("ALTER TABLE sahlen_enhancer_enhancer ADD new_enh2_start INT")
engine.execute("ALTER TABLE sahlen_enhancer_enhancer ADD new_enh2_end INT")

sql_query1 = "UPDATE sahlen_enhancer_enhancer " \
            "SET new_enh2_start = `Fragment start coordinate.1`+((`Fragment end coordinate.1`" \
             "-`Fragment start coordinate.1`)/2)-501"

sql_query2 = "UPDATE sahlen_enhancer_enhancer " \
            "SET new_enh2_end = `Fragment end coordinate.1`-((`Fragment end coordinate.1`" \
             "-`Fragment start coordinate.1`)/2)+499"

engine.execute(sql_query1)
engine.execute(sql_query2)
