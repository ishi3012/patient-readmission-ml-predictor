import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import json

def load_data(file_path):
    return pd.read_csv(file_path)

def scale_features(df, features):
    scaler = StandardScaler()
    df[features] = scaler.fit_transform(df[features])
    return df

def encode_features(df, features):
    encoder = OneHotEncoder(sparse=False)
    encoded = encoder.fit_transform(df[features])
    df = df.drop(columns=features)
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(features))
    df = pd.concat([df, encoded_df], axis=1)
    return df

def impute_features(df, features, strategy='mean'):
    imputer = SimpleImputer(strategy=strategy)
    df[features] = imputer.fit_transform(df[features])
    return df

def preprocess_data(df, config_path):
    with open(config_path, 'r') as file:
        config = json.load(file)
        
    for step, features in config['features'].items():
        if step == 'scaling':
            df = scale_features(df, features)
        elif step == 'encoding':
            df = encode_features(df, features)
        elif step == 'imputation_mean':
            df = impute_features(df, features, strategy='mean')
        elif step == 'imputation_median':
            df = impute_features(df, features, strategy='median')
    
    return df
