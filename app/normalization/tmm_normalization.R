#Trimmed Mean of M-values

library(readr)
library(edgeR)

df <- read.csv('tissue_localization_count.tsv', sep='\t')
gene_names <- df[,1]
expression_raw <- data.matrix(df[,-1])
head(expression_raw)

group <- factor(c(
  'leaf_bud', 'leaf_bud','leaf_bud',
  'large_pod', 'large_pod','large_pod',
  'leaf', 'leaf', 'leaf', 
  'medium_pod','medium_pod','medium_pod', 
  'flower','flower','flower',
  'petiole','petiole','petiole', 
  'root','root','root', 
  'small_pod', 'small_pod', 'small_pod', 
  'stem','stem','stem', 
  'mature_nodule','mature_nodule','mature_nodule', 
  'nodule_0', 'nodule_0', 'nodule_0', 
  'nodule_10','nodule_10','nodule_10', 
  'nodule_14', 'nodule_14', 'nodule_14', 
  'no3_nodule_12','no3_nodule_12','no3_nodule_12',
  'no3_nodule_48', 'no3_nodule_48', 'no3_nodule_48', 
  'nodule_4', 'nodule_4', 'nodule_4'
))
y <- DGEList(counts = expression_raw, group = group)
# Normalize for library size by calculating scaling factor using TMM (Default method)
y <- calcNormFactors(y)
# Normalization factors for each library
y$samples

# Count per million read (Normalized count)
norm_counts <- cpm(y)
head(norm_counts)

expression_tmm <- data.frame(norm_counts)
expression_tmm$gene_names <- gene_names
head(expression_tmm)
write_tsv(expression_tmm, file = 'tissue_expression_tmm.txt')
