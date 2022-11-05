######################################
# Preparing & Analysing Data
######################################

# region install, import & read

# !pip install statsmodels
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest
import openpyxl

# region get the names of sheets

df = openpyxl.load_workbook("Measurement_Problems/AB_Testing/CaseStudy/dataset/ab_testing.xlsx")
df.sheetnames  # ['Control Group', 'Test Group']

# endregion

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_control = pd.read_excel('Measurement_Problems/AB_Testing/CaseStudy/dataset/ab_testing.xlsx', sheet_name= 'Control Group')
df_test =  pd.read_excel('Measurement_Problems/AB_Testing/CaseStudy/dataset/ab_testing.xlsx', sheet_name= 'Test Group')

# endregion

# region Columns Names

df_control.head()
df_test.head()

df_control.describe().T
df_test.describe().T

df_control.columns = [col + "_C" for col in df_control.columns]
df_test.columns = [col + "_T" for col in df_test.columns]

# endregion

# region Confidance Interval

sms.DescrStatsW(df_control["Purchase_C"]).tconfint_mean()
sms.DescrStatsW(df_test["Purchase_T"]).tconfint_mean()

# endregion

# region df_control + df_test with concat method

df_CT = pd.concat([df_control, df_test], axis=1)
df_CT.head()

# endregion

######################################
# A/B Test Hypothesis
######################################

# H0 : M1 = M2 (There is no statistically significant difference between the purchase mean values of average bidding & maximum bidding.)
# H1 : M1 != M2 (There is a statistically significant difference between the purchase mean values of average bidding & maximum bidding.)

# region Analysing Purchase Variable for Control and Test Groups

df_CT.describe().T

# Purchase_C    mean :  550.89406
#               max  :  801.79502
#               std  :  134.10820

# Purchase_T    mean :  582.10610
#               max  :  889.91046
#               std  :  161.15251

# endregion

######################################
# Defining Hypothesis Testing
######################################

# region Normality Test :

# H0 : The assumption of normal distribution is provided.
# H1 : Normal distribution assumption not provided.

# p-value < ise 0.05'ten H0 REJECT.
# p-value > 0.05 H0 FAIL TO REJECT.

# Purchase_C from Control Group : p-value = 0.5891

test_stat, pvalue = shapiro(df_CT["Purchase_C"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value = 0.5891 > 0.05, H0 : FAIL TO REJECT

# Purchase_T from Test Group : p-value = 0.1541

test_stat, pvalue = shapiro(df_CT["Purchase_T"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value = 0.1541 > 0.05, H0 : FAIL TO REJECT

# H0 cannot be rejected as the assumption of normal distribution is satisfied.

# endregion

# region Homogeneity of Variance :

# H0 : Variances are homogeneous.
# H1 : Variances are not homogeneous.

# for p-value < 0.05, H0 : REJECT.
# for p-value > 0.05, H0 : FAIL TO REJECT.

test_stat, pvalue = levene(df_CT['Purchase_C'],
                           df_CT['Purchase_T'])
print("Test stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

# p-value = 0.1083 > 0.05 H0 : FAIL TO REJECT
# Variances are homogeneous.

# endregion

# Since 
# - 1. Normality Assumption
# - 2. Variance Homogeneity provided in assumption control:

# region Two-Sample t-Test (Parametric Test) :

test_stat, pvalue = ttest_ind(df_CT['Purchase_C'],
                              df_CT['Purchase_T'],
                              equal_var=True)
print('Test stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value = 0.3493 > 0.05, H0 : FAIL TO REJECT

# endregion

# region Conclusion

# Considering the p_value obtained as a result of the test, since H0 is non-rejectable,
# There is no statistically significant difference between Purchase mean for Control and Test Groups.

# endregion
