import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as po
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import matplotlib.pyplot as plt
import dash
import plotly.express as px
import random
import plotly.figure_factory as ff
from plotly import tools
from plotly.subplots import make_subplots
from plotly.offline import iplot
import warnings
from sklearn import preprocessing 

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import datasets, linear_model, metrics
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import seaborn as sns


#df=pd.read_csv('Example02.csv');
df=pd.read_csv('D:\Thesis\Datasets\Step_datasets_14.csv');
print(df);

##########################

ax = df['ENTITY'].value_counts().head(10).plot(kind='bar', title='Top 10 Years Coasters Introduced')
ax.set_xlabel('Year Introduced')
ax.set_ylabel('Count')

# save the plot as PNG file
plt.savefig("Graph\seaborn_plot_1.png")

#######################

ax1 = df['D1'].plot(kind='hist',
                          bins=20,
                          title='Coaster Speed (mph)')
ax1.set_xlabel('Speed (mph)')
# save the plot as PNG file
plt.savefig("Graph\seaborn_plot_2.png")

#########################

ax2 = df['D1'].plot(kind='kde',
                          title='Coaster Speed (mph)')
ax2.set_xlabel('Speed (mph)')
# save the plot as PNG file
plt.savefig("Graph\seaborn_plot_3.png")

###########################
df.plot(kind='scatter',
        x='D1',
        y='KEY',
        title='Coaster Speed vs. Height')
#plt.show()
# save the plot as PNG file
plt.savefig("Graph\seaborn_plot_4.png")

#####################
df_corr = df[['D0','D1','D2','D3','D4','D5','D6','D7']].dropna().corr()
sns.heatmap(df_corr, annot=True)
# save the plot as PNG file
plt.savefig("Graph\seaborn_plot_5.png")

############################
ax3 = df.query('ENTITY != "Other"') \
    .groupby('ENTITY')['D1'] \
    .agg(['mean','count']) \
    .query('count >= 10') \
    .sort_values('mean')['mean'] \
    .plot(kind='barh', figsize=(12, 5), title='Average Coast Speed by Location')
ax3.set_xlabel('Average Coaster Speed')
#plt.show()
# save the plot as PNG file
plt.savefig("Graph\seaborn_plot_6.png")