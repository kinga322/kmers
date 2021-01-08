from db_engine import create

engine = create()  # database connection created using SQLAlchemy library

# Calculate average k-mer distance for all interactions, for every promoter and enhancer

engine.execute("CREATE TABLE sahlen_similarity_enhancers "
               "SELECT Fragment_chromosome, Fragment_start_coordinate, Fragment_end_coordinate, "
               "new_enh_start, new_enh_end, AVG(kmer_distance) as avg_kmer_distance"
               " FROM sahlen_promoter_enhancer "
               "GROUP BY Fragment_chromosome, new_enh_start, new_enh_end")

engine.execute("CREATE TABLE sahlen_similarity_promoters "
               "SELECT Promoter_chr, Promoter_TSS, new_promo_start, new_promo_end, "
               "AVG(kmer_distance) as avg_kmer_distance"
               " FROM sahlen_promoter_enhancer "
               "GROUP BY Promoter_chr, new_promo_start, new_promo_end")

engine.execute("CREATE TABLE sahlen_enhancers_from_pe "
               "SELECT sahlen_promo_per_frag.Fragment_chromosome, sahlen_promo_per_frag.Fragment_start_coordinate, "
               "new_enh_start, new_enh_end, sahlen_promo_per_frag.Fragment_end_coordinate,"
               " num as degree, avg_kmer_distance "
               "FROM sahlen_promo_per_frag "
               "INNER JOIN sahlen_similarity_enhancers "
               "ON sahlen_promo_per_frag.Fragment_chromosome=sahlen_similarity_enhancers.Fragment_chromosome "
               "AND sahlen_promo_per_frag.Fragment_end_coordinate=sahlen_similarity_enhancers.Fragment_end_coordinate "
               "and sahlen_promo_per_frag.Fragment_start_coordinate="
               "sahlen_similarity_enhancers.Fragment_start_coordinate")

engine.execute("CREATE TABLE sahlen_promoters_from_pe "
               "SELECT sahlen_frag_per_promo.Promoter_chr, sahlen_frag_per_promo.Promoter_TSS, "
               "new_promo_start, new_promo_end, "
               "num as degree, avg_kmer_distance "
               "FROM sahlen_frag_per_promo "
               "INNER JOIN sahlen_similarity_promoters "
               "ON sahlen_frag_per_promo.Promoter_chr=sahlen_similarity_promoters.Promoter_chr "
               "AND sahlen_frag_per_promo.Promoter_TSS=sahlen_similarity_promoters.Promoter_TSS ")