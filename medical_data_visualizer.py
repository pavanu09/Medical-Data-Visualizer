import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
df['overweight'] = (df['weight']/((df['height']/100)**2) > 25).astype('int8')

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = (df['cholesterol'] != 1).astype('int8')
df['gluc'] = (df['gluc'] != 1).astype('int8')


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df0 = df[df['cardio'] == 0]
    df0long = pd.melt(df0, value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])
    df1 = df[df['cardio'] == 1]
    df1long = pd.melt(df1, value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])
    

    # Draw the catplot with 'sns.catplot()'
    fig, axs = plt.subplots(ncols=2, figsize=(15, 5))
    plot0 = sns.countplot(data=df0long, x='variable', hue='value', ax=axs[0]).set(title='cadio = 0', ylabel="total")
    axs[0].legend([],[], frameon=False)
    plot1 = sns.countplot(data=df1long, x='variable', hue='value', ax=axs[1]).set(title='cadio = 1', ylabel="total")
    sns.move_legend(axs[1], "right", bbox_to_anchor=(1.15, 0.5))

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    global df
    df = df[df['ap_lo'] <= df['ap_hi']]
    df = df[(df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975))]
    df = df[(df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    def abs_zero(x):
        for i in range(len(x)):
            if x[i] == 0:
                x[i] = abs(x[i])
        return x
    corr = df.corr().round(decimals=1).transform(abs_zero)

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))


    # Set up the matplotlib figure
    fig, axs = plt.subplots(ncols=1, figsize=(10, 10))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask=mask, annot=True, fmt=".1f")


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
