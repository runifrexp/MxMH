import altair as alt
import polars as pl
import streamlit as st
import numpy as np
import plotly.express as px # Per il grafico 3D
import plotly.graph_objects as go # Per il grafico 3D
from sklearn.linear_model import LinearRegression # Per il piano nel grafico 3D
import data_cleaning

# Imposta il nome che viene fuori nel browser con emoji
st.set_page_config(
    page_title="MxMH",
    page_icon="🔀"
)

# Importo i dati con la funzione definita in data_cleaning.py (get_data)
data = data_cleaning.get_data()

# Titolo della pagina
st.title("Analisi Incrociate: Relazioni tra Musica e Benessere Psichico")

# Introduzione
st.write("""
In questa sezione dedicata all'**analisi incrociata** delle variabili legate alla **musica** e alle **condizioni psichiche**, si entra nel punto focale dell'indagine.  
Lo scopo è quello di esplorare e mettere in evidenza i pattern rilevanti presenti tra variabili riguardanti la musica e variabili riguardanti lo stato psichico. 

Ad esempio, è possibile osservare se il livello di depressione è in qualche modo legato al genere musicale preferito, o come la frequenza di ascolto di determinati generi possa essere legata a una condizione psichica.

""")





### ISTOGRAMMA SULL'EFFETTO DELLA MUSICA

# Rimuovi i valori mancanti nella colonna "Music effects"
filtered_data = data.filter(pl.col("Music effects").is_not_null())

# Calcola conteggi e percentuali
music_effects_counts = (
    filtered_data
    .group_by("Music effects")  # Raggruppa i dati per la colonna "Music effects"
    .count()  # Conta il numero di occorrenze per ogni categoria
    .rename({"count": "count"})  # Rinomina la colonna "count" per chiarezza
    .with_columns(
        (pl.col("count") / filtered_data.height).alias("percentage")  # Calcola la percentuale per il tooltip
    )
)

# Istogramma 
music_effects_histogram = (
    alt.Chart(music_effects_counts)
    .mark_bar() # Istogramma (grafico a barre)
    .encode(
        x=alt.X("Music effects:N", title="Effetti della Musica"),
        y=alt.Y("count:Q", title="Conteggio"),
        color=alt.Color("Music effects:N", title="Effetti della Musica"), # Colore in base alle modalità della variabile Music effects
        tooltip=[ # Tooltip con effetto, frequenze assolute e relative
            alt.Tooltip("Music effects:N", title="Effetto"),
            alt.Tooltip("count:Q", title="Conteggio"),
            alt.Tooltip("percentage:Q", title="Percentuale", format=".2%")
        ]
    )
    .properties(
        title="Distribuzione degli Effetti della Musica",
        height=500
    )
    .configure_title(fontSize=27)  # Imposta un font più grande per i titoli del grafico
)

# Mostra il grafico in Streamlit
st.altair_chart(music_effects_histogram, use_container_width=True)

st.write("""
Dal grafico emerge che una significativa maggioranza degli utenti, pari al **74.45%**, percepisce miglioramenti nelle proprie condizioni psichiche durante l'ascolto di musica.  
Questo risultato suggerisce che molti utenti tendano a scegliere brani che li mettono di buon umore o che aiutano a rilassarsi.

D'altro canto, una piccola percentuale degli utenti, il **2.34%**, segnala un peggioramento del proprio stato mentale.  
Questo potrebbe essere attribuito all'ascolto di brani che evocano ricordi tristi o traumatici.

Infine, il restante **23.21%** degli utenti dichiara di non percepire effetti significativi.  
È possibile che questa categoria utilizzi la musica come sottofondo mentre svolge altre attività, come lavorare o studiare, senza un coinvolgimento emotivo diretto.
""")





### GRAFICO 3D CHE INCROCIA ETÀ, LIVELLO DELLA CONDIZIONE SELEZIONATA E ORE DI ASCOLTO 

# Filtra i dati per eliminare eventuali NaN nelle variabili di interesse
data_cleaned = data.filter(
    (pl.col("Hours per day").is_not_null()) &
    (pl.col("Age").is_not_null())
)

# Conversione in Pandas per compatibilità Plotly (altrimenti non funziona)
data_pandas = data_cleaned.select([
    "Age", "Hours per day", "Depression", "Anxiety", "OCD", "Insomnia"
]).to_pandas() 

# Selezione della condizione
st.write("### Relazione tra età, ore di ascolto e condizione psichica")
condition = st.selectbox(
    "Seleziona la condizione psichica da analizzare:",
    ["Depression", "Anxiety", "OCD", "Insomnia"]
)

# Definizione delle variabili esplicative (age, hours per day) e della variabile risposta (condition)
X = data_pandas[["Age", "Hours per day"]]
y = data_pandas[condition]

# Creazione del modello lineare 
model = LinearRegression()
model.fit(X, y)

# Crea il grafico 3D
fig = go.Figure()

# Aggiungi i punti delle osservazioni
fig.add_trace(
    go.Scatter3d(
        x=data_pandas["Age"],
        y=data_pandas["Hours per day"],
        z=data_pandas[condition],
        mode='markers',
        marker=dict(size=5, color=data_pandas[condition], colorscale="Plasma"),
        name="Dati"
    )
)

# Crea una gamma di valori uniforme per l'età
x_range = (
    np.linspace(
        data_pandas["Age"].min(), 
        data_pandas["Age"].max(), 
        10)
)  

# Crea una gamma di valori uniforme per le ore di ascolto
y_range = (
    np.linspace(
        data_pandas["Hours per day"].min(), 
        data_pandas["Hours per day"].max(), 
        10)
)  

# Genera una griglia 2D combinando x_range e y_range
x_grid, y_grid = np.meshgrid(x_range, y_range)  

# Predice i valori della condizione per ogni combinazione della griglia e la rimappa alla forma della griglia
z_grid = (
    model.predict(
        np.c_[x_grid.ravel(),
        y_grid.ravel()]
        )
        .reshape(x_grid.shape)
)  

# Aggiungi il piano di regressione 
fig.add_trace(
    go.Surface(
        x=x_grid,  # Griglia età
        y=y_grid,  # Griglia ore di ascolto
        z=z_grid,  # Valori stimati del piano
        colorscale=[[0, "lightblue"], [1, "lightblue"]],  # Colore uniforme (scala piatta)
        opacity=0.5,  # Trasparenza per vedere i punti sottostanti
        showscale=False,  # Rimuovi la barra del colore
        name="Piano di regressione"  # Etichetta del piano
    )
)

# Configura il grafico
fig.update_layout(
    title=f"Età, Ore di ascolto e {condition}",
    scene=dict(
        xaxis_title="Età",
        yaxis_title="Ore di ascolto",
        zaxis_title=f"Livello di {condition}"
    ),
    height=700
)

# Mostra il grafico in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Coefficienti del modello con la condizione selezionata
beta_0 = model.intercept_  # Intercetta
beta_1, beta_2 = model.coef_  # Coefficienti per "Age" (x1) e "Hours per day" (x2)

# Mostra l'equazione del piano di regressione per la condizione selezionata
st.latex(rf"\text{{Equazione del piano di regressione per {condition}: }} \hat{{y}} = {beta_0:.2f} + {beta_1:.2f} \cdot x_1 + {beta_2:.2f} \cdot x_2")

st.write("""
Dalla visualizzazione 3D si nota che la maggior parte degli utenti ascolta al massimo 10 ore al giorno di musica. 
Si nota una decina di outlier che vanno oltre la soglia delle 10 ore al giorno.

Parlando dell'età si nota come nei grafici esplorativi che la maggior parte degli utenti è tra l'età adolescenziale e i 50 anni.

Trattando invece le condizioni si nota, come nel grafico delle densità nella sezione esplorativa per le condizioni, che:
- **OCD** è concentrata principalmente nei valori bassi, indicando una bassa prevalenza tra gli utenti;
- **Insomnia** mostra una distribuzione più equilibrata con un leggero picco verso i valori medi;
- **Depression** presenta una distribuzione più eterogenea, con utenti che riportano valori sia bassi che alti, suggerendo una maggiore variabilità;
- **Anxiety** è simile a Depression, ma con una densità leggermente più alta nei valori attorno al 5.

Questi pattern suggeriscono che le condizioni psichiche hanno distribuzioni diverse tra gli utenti e potrebbero essere influenzate da variabili come età o frequenza di ascolto della musica.
""")

# Breve spiegazione della regressione multivariata usata per creare il piano di regressione
st.write("***Regressione Lineare Multivariata***")

# Introduzione
st.write("""
Il piano nel grafico 3D viene fatto tramite una regressione lineare multivariata, che analizza la relazione tra una variabile risposta $y$ e più variabili esplicative.\\
Questa analisi ci permette di tracciare un piano che serve a fare predizioni e a capire come sono relazionate tra loro le variabili. 
Nel nostro caso, il modello può essere espresso come segue:
""")

# Formula del modello
st.latex(r"\hat{y} = \beta_0 + \beta_1 x_1 + \beta_2 x_2")

# Spiegazione delle variabili
st.write("***Spiegazione delle Variabili:***")
st.write(r"""
- **$\hat{y}$**: Livello predetto della condizione psichica, ovvero la variabile dipendente.
- **Intercetta ($\beta_0$)**: Valore stimato della variabile $\hat{y}$ quando tutte le variabili indipendenti sono pari a zero.
- **Coefficiente per $x_1$ ($\beta_1$)**: Indica la variazione media di $\hat{y}$ per ogni anno aggiuntivo di età, mantenendo costanti le altre variabili.
- **Coefficiente per $x_2$ ($\beta_2$)**: Indica la variazione media di $\hat{y}$ per ogni ora aggiuntiva di ascolto, mantenendo costanti le altre variabili.
- **$x_1$**: Età dell'utente (variabile indipendente 1).
- **$x_2$**: Ore di ascolto giornaliere dell'utente (variabile indipendente 2).
""")

# Metodo di stima
st.write("***Metodo di Stima: Minimi Quadrati Ordinari (OLS)***")
st.write(r"""
I parametri $\beta_0$, $\beta_1$, $\beta_2$ sono stimati minimizzando la somma dei quadrati degli errori ($SSE$):
""")
st.latex(r"\text{SSE} = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2")

st.write("""
Dove:
- **$y_i$**: Valore osservato della condizione psichica.
- **$\hat{y}_i$**: Valore predetto dal modello.
- **$n$**: Numero totale di osservazioni.
""")

# Obiettivo del modello
st.write("***Obiettivo del Modello***")
st.write(r"""
Il modello ha i seguenti obiettivi:
- Quantificare la relazione tra variabili esplicative ($x_1$, $x_2$) e la risposta ($\hat{y}$).
- Prevedere il livello della condizione psichica ($\hat{y}$) per valori specifici di età ($x_1$) e ore di ascolto ($x_2$).
""")





# Filtra i dati: rimuove i valori nulli
filtered_data = data.filter(
    (pl.col("Fav genre").is_not_null()) &
    (pl.col("Depression").is_not_null()) &
    (pl.col("Anxiety").is_not_null()) &
    (pl.col("OCD").is_not_null()) &
    (pl.col("Insomnia").is_not_null())
)

# Trasforma i dati in long data per creare la heatmap
data_long = filtered_data.melt(
    id_vars=["Fav genre"],
    value_vars=["Depression", "Anxiety", "OCD", "Insomnia"],
    variable_name="Condition",
    value_name="Level"
)

# Calcola la media dei livelli per combinazione di genere musicale e condizione
heatmap_data = data_long.group_by(["Fav genre", "Condition"]).agg(
    pl.col("Level").mean().alias("Average Level")
).to_pandas()  # Converti in Pandas per Altair

# Ordina i generi musicali in base alla media generale dei livelli
heatmap_order = (
    heatmap_data.groupby("Fav genre")["Average Level"]
    .mean()
    .sort_values(ascending=False)
    .index.tolist()
)

# Heatmap
heatmap = (
    alt.Chart(heatmap_data)
    .mark_rect()
    .encode(
        x=alt.X("Fav genre:N", title="Genere Musicale", sort=heatmap_order),
        y=alt.Y("Condition:N", title="Condizione Psichica"),
        color=alt.Color(
            "Average Level:Q",
            title="Livello Medio",
            scale=alt.Scale(scheme="spectral"),  # Migliora leggibilità
        ),
        tooltip=[
            alt.Tooltip("Fav genre:N", title="Genere Musicale"),
            alt.Tooltip("Condition:N", title="Condizione Psichica"),
            alt.Tooltip("Average Level:Q", title="Livello Medio", format=".1f"),
        ],
    )
    .properties(height=600)
)

# Aggiungi i valori numerici alle celle
text = (
    alt.Chart(heatmap_data)
    .mark_text(baseline="middle")
    .encode(
        x=alt.X("Fav genre:N", sort=heatmap_order),
        y=alt.Y("Condition:N"),
        text=alt.Text("Average Level:Q", format=".1f"),
        color=alt.value("black"),  # Testo leggibile
    )
)

# Combina la heatmap con i valori numerici
combined_chart = (heatmap + text).properties(
    title="Condizioni psichiche per genere musicale preferito"
).configure_title(fontSize=27)

# Mostra il grafico in Streamlit
st.altair_chart(combined_chart, use_container_width=True)

st.write("""
Dal grafico emerge che:

1. **Anxiety**: I livelli medi di ansia sono più alti per generi come *Hip hop* (6.6) e *Rock* (6.6), mentre risultano più bassi per *Latin* (4.3) e *Gospel* (4.8).
2. **Depression**: La depressione raggiunge i valori più elevati per *Lofi* (6.6) e *Hip hop* (5.9), mentre generi come *Latin* (3.0) e *Gospel* (2.7) mostrano valori più contenuti.
3. **Insomnia**: L'insonnia registra valori alti per *Lofi* (5.6) e *Gospel* (5.3), ma livelli significativamente più bassi per *Country* (2.7) e *Latin* (3.3).
4. **OCD**: Il disturbo ossessivo-compulsivo ha livelli medi generalmente bassi, con valori più alti per *Lofi* (3.4) e *Hip hop* (2.7), mentre *Gospel* (0.3) si distingue per valori molto bassi.

Il genere *Lofi* sembra associato a livelli più elevati di ansia, depressione e insonnia, suggerendo una possibile preferenza da parte di utenti con queste condizioni. 
Al contrario, generi come *Latin* e *Gospel* mostrano valori più bassi in tutte le condizioni, specialmente per l'OCD. 
""")

