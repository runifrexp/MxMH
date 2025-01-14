import polars as pl

def get_data():
    file_name = "mxmh_survey_results.csv" # Nome del file
    dtypes = { # Definisco alcuni i tipi di alcune variabili perchè altrimenti danno problemi
        "Depression": pl.Float64,
        "Anxiety": pl.Float64,
        "OCD": pl.Float64,
        "Insomnia": pl.Float64,
        "Hours per day": pl.Float64,
        "Age": pl.Int64
    }
    data = pl.read_csv(file_name, dtypes=dtypes) # Carica il dataset
    data_filtered = data.filter(pl.col("Age") != 89) # Rimozione outlier
    return data_filtered
