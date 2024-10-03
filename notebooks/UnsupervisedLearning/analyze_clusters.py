import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler


import sys
import os

# Add the parent directory to the sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

# Now you can import the function from the Python file in the parent directory
from standardize_visuals import generate_cmap_theme, generate_hex 


def standardize_row_wise(data):
    '''
    Standardize each row of the data using StandardScaler().
    Parameters: 
        data: dataframe with the columns we would like to apply the standard scalar 
    '''
    scaler = StandardScaler()
    return pd.DataFrame(scaler.fit_transform(data), index=data.index, columns=data.columns)

def split_features(df, features_to_analyze):
    ''' 
    Splits and identifies the numerical and categorical columns based on the datatype

    Paramters:
        df: dataframe with the features columns in there 
        features_to_analyze: the list of feeatures given that we would like to analyze
    '''
    numerical_features = df[features_to_analyze].select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = df[features_to_analyze].select_dtypes(exclude=[np.number]).columns.tolist()
    return numerical_features, categorical_features

def plot_numerical_features(df, numerical_features, cluster_column='k_means_cluster'):
    '''
    Visualize the numerical features mean within each cluster 

    Parameters: 
        df: dataframe with the numerical features in it 
        numerical_features: list of features that we would like to visualize 
        cluster_column: name column with the cluster 
    '''
    # Group by cluster and calculate the mean for numerical features
    cluster_means = df.groupby(cluster_column)[numerical_features].mean()
    
    # Standardize the values, add in the cluster column, and then calculate the mean for these standardized numerical features 
    standardized_values_df = standardize_row_wise(df[numerical_features])
    standardized_values_df[cluster_column] = df[cluster_column]
    standardized_value_means = standardized_values_df.groupby(cluster_column)[numerical_features].mean()

    # Raw Visual
    plt.figure(figsize=(10, 6))
    sns.heatmap(cluster_means, annot=True, cmap= generate_hex(), linewidths=0.5)
    plt.title('Numerical Feature Mean Values per Cluster')
    plt.ylabel('Cluster')
    plt.xlabel('Features')
    plt.show()

    # Standardized Visual 
    plt.figure(figsize=(10, 6))
    sns.heatmap(standardized_value_means, annot=True, cmap= generate_hex(color_name='maize'), linewidths=0.5)
    plt.title('Numerical Feature (Normalized) Mean Values per Cluster')
    plt.ylabel('Cluster')
    plt.xlabel('Features')
    plt.show()

def plot_stacked_bar_chart(df, feature, cluster_column='k_means_cluster'):
    '''
    Visualize a categroical features within each cluster 

    Parameters: 
        df: dataframe with the categorical features in it 
        feature: categorical feature name
        cluster_column: name of the column with the cluster 
    '''
    # Create a contingency table of clusters and categorical values -normalized within each cluster (row)
    crosstab = pd.crosstab(df[cluster_column], df[feature], normalize='index')
   
    crosstab.plot(kind='bar', stacked=True, figsize=(10, 6), cmap=generate_cmap_theme())
    plt.title(f'Stacked Bar Chart for {feature} by Cluster')
    plt.ylabel('Proportion')
    plt.xlabel('k_means_cluster')
    plt.legend(title=feature, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_categorical_features(df, categorical_features, cluster_column='k_means_cluster'):
    '''
    Visualize all the categroical features within each cluster 

    Parameters: 
        df: dataframe with the categorical features in it 
        categorical_features: list of categorical feature names
        cluster_column: name of the column with the cluster 
    '''
    # Iterate through the categorical feature to plot a stacked bar chart
    for feature in categorical_features:
        plot_stacked_bar_chart(df, feature, cluster_column)

def plot_feature_distribution_per_cluster(df, features_to_analyze, cluster_column='k_means_cluster'):
    '''
    Runs all the fun visualization for the numerical and categorical features 

    Parameters: 
        df: dataframe with the features and cluster name
        features_to_analyze: llist of the features we are looking to anlayze
        cluster_column: name of the cluster name
    '''
    numerical_features, categorical_features = split_features(df, features_to_analyze)
    
    if numerical_features:
        print("Numerical Features:")
        plot_numerical_features(df, numerical_features, cluster_column)
    
    if categorical_features:
        print("Categorical Features:")
        plot_categorical_features(df, categorical_features, cluster_column)

