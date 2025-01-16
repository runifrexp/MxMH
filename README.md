# MxMH - Music x Mental Health 🎵🧠

## Descrizione
Questo progetto analizza i dati di un sondaggio per comprendere l'impatto della musica sulla condizione psichica di un individuo. In particolare le condizioni analizzate sono ansia, depressione, insonnia e disturbo ossessivo compulsivo.

---

## Dataset
Il dataset utilizzato è **`mxmh_survey_results.csv`**, (https://www.kaggle.com/datasets/catherinerasgaitis/mxmh-survey-results).
Il preprocessing dei dati è molto semplice e veloce (utilizzabilità 10 da Kaggle), in quanto è necessario soltanto specificare i tipi di alcune variabili numeriche 
e rimuovere un outlier (è stata rimossa l'unità statistica dell'utente di 89 anni e con 24 ore di ascolto per giorno).  
Nel link si trova tutto ciò che è necessario per la comprensione del dataset: dalla spiegazione delle variabili, al metodo di raccolta dei dati.  
In seguito verranno elencate le variabili principali per evitare di dover leggere la documentazione del dataset per capire l'analisi dati MxMH.

### Variabili utilizzate:
- `Age`: Età dell'utente.
- `Primary streaming service`: Piattaforma di streaming musicale principale (Spotify, Pandora, Youtube Music, Apple Music, I do not use a streaming service, Other streaming service).
- `Hours per day`: Ore dedicate all'ascolto della musica ogni giorno.
- `Fav genre`: Genere musicale preferito. Rilevati in tutto 16 generi: Jazz, K-pop, Latin, Lo-fi, Metal, Pop, R&B, Rap, Rock, Video Game Music, Classical, Country, EDM, Folk, Gospel, Hip-Hop
- `Frequency{genre}`: Frequenza di ascolto (Never, Rarely, Sometimes, Very frequently) dei 16 generi di musica rilevati.
- `Anxiety`, `Depression`, `Insomnia`, `OCD`: Valori numerici interi da 0 a 10 che quantificano le condizioni psichiche di ansia, depressione, insonnia e disturbo ossessivo compulsivo.
- `Music effects`: Effetto percepito della musica sul benessere (Improve, No effect, Worsen).

---

## Data Cleaning
Il file `data_cleaning.py` contiene la funzione **`get_data()`** che si occupa di:
1. Importare i dati dal file csv.
2. Specificare i tipi di alcune variabili numeriche che avevano difficoltà ad esser lette.
3. Rimuovere l'outlier sopracitato.

In ogni script i dati preprocessati vengono importati utilizzando la funzione **`get_data()`** del modulo `data_cleaning` per non doverli sistemare ogni volta.

---

## Librerie Usate
- **[Polars](https://www.pola.rs/)**: Per la manipolazione dei dati.
- **[Streamlit](https://streamlit.io/)**: Per creare un'interfaccia utente interattiva per visualizzare i risultati.
- **[Scikit-learn](https://scikit-learn.org/)**: Per poter fare la regressione lineare multipla (e molte altre cose...). (affrontata nel corso di Intelligenza Artificiale a Ingegneria Informatica)
- **[Altair](https://altair-viz.github.io/)**: Per creare grafici interattivi.
- **[NumPy](https://numpy.org/)**: Per calcolare correlazioni.
- **[Plotly](https://plotly.com/python/)**: Per il grafico 3D.


---

## Come Usare il Codice

L'utilizzo di **uv** consente di eseguire il codice in modo semplice, senza la necessità di attivare manualmente il virtual environment. Questo strumento permette di avviare direttamente l'applicazione o gli script associati al progetto.

1. **Scaricare la repository:**
   - Clonare la repository sul proprio PC:
     ```bash
     git clone https://github.com/runifrexp/MxMH.git
     ```

2. **Esecuzione:**
   - Avviare l'app Streamlit:
     ```bash
     uv run streamlit run Introduzione.py
     ```


---

## Analisi
Nella pagina `Introduzione.py` viene fornita un'overview dell'analisi e di alcuni riferimenti scientifici. 


---

## Note
Il modello di regressione utilizzato nell'analisi incrociata non è stato sottoposto a nessun test di significatività. È soltanto un punto di partenza per ulteriori analisi future.





