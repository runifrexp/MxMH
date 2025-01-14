# MxMH 

## Descrizione
Questo progetto analizza i dati di un sondaggio per comprendere l'impatto della musica sul benessere psicologico. Attraverso tecniche di pulizia e analisi dei dati, abbiamo esplorato come la musica influisce su ansia, depressione e insonnia.

---

## Dataset
**`mxmh_survey_results.csv`**

### Variabili principali:
- `Age`: Età dei partecipanti.
- `Primary streaming service`: Piattaforma di streaming musicale principale.
- `Hours per day`: Ore dedicate all'ascolto della musica ogni giorno.
- `Fav genre`: Genere musicale preferito.
- `Anxiety`, `Depression`, `Insomnia`: Valori numerici che indicano la gravita di questi problemi psicologici.
- `Music effects`: Effetto percepito della musica sul benessere (Migliora, Peggiora, Nessun effetto).

---

## Data Cleaning
Il file `data_cleaning.py` contiene la logica per:
1. Rimuovere valori nulli o incoerenti.
2. Normalizzare le variabili numeriche.
3. Gestire le variabili categoriche (ad esempio, encoding delle preferenze di genere musicale).
4. Filtrare dati fuori dal range atteso (es: ore di ascolto giornaliere > 24).

Esempio di operazioni applicate:
```python
# Rimuove valori nulli
survey_data.dropna(inplace=True)

# Encoding di variabili categoriche
survey_data['Fav genre'] = survey_data['Fav genre'].astype('category').cat.codes
```

---

## Librerie Usate
- **[Polars](https://www.pola.rs/)**: Per manipolazione dei dati ad alta efficienza.
- **[Streamlit](https://streamlit.io/)**: Per creare un'interfaccia utente interattiva per visualizzare i risultati.

---

## Come Usare il Codice

1. **Requisiti:**
   - Python 3.8+
   - Librerie elencate in `pyproject.toml`.

2. **Setup Ambiente:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Esecuzione:**
   - **Pulizia Dati:** Esegui `data_cleaning.py`:
     ```bash
     python data_cleaning.py
     ```
   - **Visualizzazione:** Avvia l'app Streamlit:
     ```bash
     streamlit run hello.py
     ```

---

## Analisi
L'analisi ha rivelato:
1. I generi musicali preferiti variano significativamente con l'età e l'uso delle piattaforme di streaming.
2. La musica è percepita come un miglioramento per ansia, depressione e insonnia nel 70% dei partecipanti.
3. Gli effetti della musica sembrano dipendere dal tempo di ascolto giornaliero e dal genere preferito.

Un modello di regressione è stato utilizzato per prevedere lo stato psicologico basandosi sui dati del sondaggio.

