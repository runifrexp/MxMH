
import polars as pl

file_name = "mxmh_survey_results.csv"

#in quanto leggendo "normalmente" i dati si verificano errori bisogna specificare che i valori delle seguenti colonne sono dei float
dtypes = {
    "Depression": pl.Float64,
    "Anxiety": pl.Float64,
    "OCD": pl.Float64, 
    "Insomnia": pl.Float64 
}

data = pl.read_csv(file_name, dtypes=dtypes)

print(data.head())
#i dati sembrano esser letti correttamente ora


### il filtering per costruire le varie rappresentazioni grafiche, in data_processing.py verranno filtrati ed elaborati i dati statici, 
### ossia che non cambiano in base alle scelte dell'utente, mentre i dati che dipendono dalle scelte dell'utente verranno elaborati direttamente in grafici.py


#dati per il grafico ,
music_effects_counts = data.select(
    pl.col("Music effects").value_counts().alias("Music effects_counts")
)
sorted_counts = music_effects_counts.sort("Music effects_counts", descending=True)
print(sorted_counts)
