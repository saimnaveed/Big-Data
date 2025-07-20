import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

#pd.options.display.width= None
#pd.options.display.max_columns= None
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', 30)


#Reading the CSV file using Pandas

df=pd.read_csv(r'C:\Users\naveesai\Downloads\movies\movies.csv',sep=',',header=0)
print(df.head(10))

#Getting count of Missing Values in different columns

for col in df.columns:
    count=0
    missing_count=np.mean(df[col].isna().sum())
    #print('{} - {}'.format(col,missing_count))

#Checking the datatype of different columns

types=df.dtypes
#print("Data types of different columns are:")
#print(types)

#Filling the Missing Values
df['budget'] = df['budget'].fillna(0)
df['gross'] = df['gross'].fillna(0)
df['released']=df['released'].fillna('abcd 00, 0000 (xyx)')
#df['gross'] = df['gross'].fillna(np.mean(df['gross']))

#Another Options of dropping the rows which are missing values

# df['budget'] = df['budget'].dropna()
# df['gross'] = df['gross'].dropna()

#Changing datatype of Columns
df['budget']=df['budget'].astype('int64')
df['gross']=df['gross'].astype('int64')

#df['released']=pd.to_datetime(df['released'])


#creating a new column yearcorrect because of difference of year in the column year and released
#For extracting the required value regex pattern is used
df['yearcorrect'] = df['released'].str.extract(pat = '([0-9]{4})').astype(int)
#print(df.columns)

#Sorting the data based on gross amount
df=df.sort_values(by=['gross'], inplace=False, ascending=False)
#print(df)

# Checking for duplicate values
distinct_companies=df['company'].drop_duplicates().sort_values(ascending=False)
# df= df.drop_duplicates()
# print(distinct_companies.size)
# print(dc.size)

#Checking the correlation between the between different fields  via plots
# 1- Relation between the budget and the gross

x= df['budget']
y= df['gross']
plt.title("Gross Vs Budget")
plt.xlabel("Budget")
plt.ylabel("Gross")
plt.scatter(x,y,color='g')
#plt.show()

# Regression Plot using Seaborn for Gross v.s Budget

sns.set_style('whitegrid')
sns.regplot(x='budget',y='gross',data=df,scatter_kws={"color":"red"},line_kws={"color":"blue"})
#plt.show()

#Checking correlation between the only numeric quantities of the dataframe on the scale of 0-1
correlation=df.corr(method='pearson') #spearman, pearson, kendall
#print(correlation)
#corr_mat= df.corr(method='spearman')

#sns.heatmap(correlation, annot=True)
plt.title("Correlation Matrix")
plt.xlabel("Movie Features")
plt.ylabel("Movie Features")
#plt.show()

#Converting the non-numeric value to numeric ones
df_n=df
for col in df_n.columns:
    if df_n[col].dtype==object:
        df_n[col]=df_n[col].astype("category")
        df_n[col]=df_n[col].cat.codes

corr_matn= df_n.corr()
sns.heatmap(corr_matn, annot=True)
plt.title("Correlation Matrix")
plt.xlabel("Movie Features")
plt.ylabel("Movie Features")
#plt.show()

#unstacking or reordering the correlation matrix so see or analyze it easily
relation_pairs=corr_matn.unstack()
ordered_pairs=relation_pairs.sort_values()

#Checking for Highly correlated values
high_cor=ordered_pairs[(ordered_pairs)>0.5]
print(high_cor)

#Correlation Analysis Results

# 1- Votes and budget are highly related
# 2- Gross and budget are highly related
# 3- Company and gross are not related to each other
