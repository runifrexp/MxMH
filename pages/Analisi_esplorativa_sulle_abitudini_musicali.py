import altair as alt
import polars as pl
import streamlit as st
import data_cleaning

# Imposta il nome che viene fuori nel browser con emoji
st.set_page_config(
    page_title="MxMH",
    page_icon=":musical_note:"
)

# Importo i dati con la funzione definita in data_cleaning.py (get_data)
data = data_cleaning.get_data()

st.title("Analisi esplorativa sulle abitudini musicali")
st.write("""
In questa sezione verranno analizzati alcuni dati relativi alla **musica**, alle **abitudini di ascolto** e agli **utenti**. 
L'idea è quella di esplorare diversi aspetti, come:
- La distribuzione dell'età degli ascoltatori (utenti)
- Quali sono le piattaforme di streaming sono più popolari
- Le ore di ascolto per i vari generi
- Le ore di ascolto medie in base all'età
- Rilevare i generi musicali preferiti dagli ascoltatori
- La frequenza di ascolto per ogni genere musicale

Questa analisi serve principalmente per capire meglio come le persone interagiscono con la musica e cosa emerge da queste abitudini.
""")





### ISTOGRAMMA PER OSSERVARE LA DISTRIBUZIONE DELLE ETÀ

# Filtraggio dei dati per escludere valori estremi, altrimenti l'istogramma avrebbe una serie di valori nulli 
# fino all'outlier 80 anni. 
data_age_hist = (
    data.filter(pl.col("Age") <= 70)  # Filtra le età <= 70
    .group_by("Age")  # Raggruppa per età
    .agg(pl.count().alias("Count"))  # Conta il numero di risposte per età
    .with_columns(
        (pl.col("Count") / pl.col("Count").sum() * 100).alias("Percentage")  # Calcola le percentuali
    )
)

# Creazione dell'highlight per evidenziare la colonna sulla quale si è con il mouse
highlight = (
    alt.selection_single( # Crea una selezione singola
        on='mouseover', # La selezione viene attivata quando il mouse passa sopra un elemento
        fields=['Age'], # La selezione si basa sulla variabile 'Age'
        empty='none' # Non mostra l'highlight quando non c'è una selezione
    )
)

# Creazione del grafico 
age_hist = (
    alt.Chart(data_age_hist)
    .mark_bar(stroke="black", strokeWidth=1) # Segna i contorni delle colonne
    .encode(
        x=alt.X("Age:O", title="Età", sort="ascending"), # Asse x: età in ordine crescente
        y=alt.Y("Count:Q", title="Frequenza"), # Asse y: frequenze assolute
        color=alt.condition( # Colore che cambia in base all'highlight (condition)
            highlight, 
            alt.value('yellow'), # Giallo quando la barra è evidenziata
            alt.value('blue') # Blu per il resto delle colonne (colori scelti in base alle assi dello spazio dei colori)
            ),
        tooltip=[ # Tooltip con età, frequenza assoluta e relativa
            alt.Tooltip("Age:O", title="Età"),
            alt.Tooltip("Count:Q", title="Frequenza"),
            alt.Tooltip("Percentage:Q", title="Percentuale (%)", format=".2f")
        ]
    )
    .properties(
        title = "Frequenza dei rispondenti per età",
        height=450
        )
    .add_selection(highlight) # Aggiunge la selezione interattiva al grafico, basata su 'highlight'
    .configure_title(fontSize=25)  # Imposta una dimensione maggiore per il titolo del grafico

)

st.altair_chart(age_hist, use_container_width=True) # Mostra il grafico, use_container_width per adattare il grafico alla larghezza della pagina web.

# Tabella per le età escluse (possibilità di mostrarla o meno)
age_hist_removed = data.filter(pl.col("Age") > 70)  # Filtro età > 70 anni

freq_removed = (
    age_hist_removed
    .group_by("Age") # Raggruppa per età
    .agg(pl.count().alias("Frequency")) # Conta le frequenze
    .sort("Age")  # Ordina per età in ordine crescente
)

if "show_table" not in st.session_state: # Verifica se la variabile "show_table" esiste nello stato della sessione.
    st.session_state["show_table"] = False

if st.button("Mostra i dati esclusi nell'istogramma"): # Bottone per mostrare o meno la tabella
    st.session_state["show_table"] = not st.session_state["show_table"]

if st.session_state["show_table"]: # Mostra la tabella se richiesto dall'utente
    st.write("**Dati esclusi dall'istogramma:**")
    st.dataframe(freq_removed)

st.write("""
Come ci si poteva aspettare, l'istogramma evidenzia che la maggior parte degli utenti è giovane. \\
Dai 30 anni in poi la distribuzione tende verso valori sempre più bassi, mentre tra l'età adolescenziale 
e i 30 anni si concentra la maggior parte degli utenti.
""")





### GRAFICO A TORTA PER OSSERVARE QUALI SONO LE PIATTAFORME DI STREAMING MUSICALE PIÙ DIFFUSE

# Filtraggio per rilevare la distribuzione delle piattaforme
data_platform_pie = (
    data.filter(pl.col("Primary streaming service").is_not_null())  # Rimuove valori nulli
    .group_by("Primary streaming service")  # Raggruppamento per piattaforma
    .agg(pl.count().alias("Users"))  # Conteggio delle unità
    .with_columns((pl.col("Users") / pl.col("Users").sum() * 100).alias("Percentage"))  # Calcolo percentuali
    .with_columns((pl.col("Percentage").round(2).cast(str) + "%").alias("Percentage_Label"))  # Aggiunge il simbolo "%"
)

# Creazione di due selezioni separate
highlight_arc_and_label = alt.selection_single(
    fields=["Primary streaming service"],  # Campo per la selezione
    on="mouseover",  # Evento di evidenziazione
    clear="mouseout",  # Ripristina su mouse-out
    empty="all"  # Mostra tutto all'inizio
)

highlight_percentage = alt.selection_single(
    fields=["Primary streaming service"],  # Campo per la selezione
    on="mouseover",  # Evento di evidenziazione
    clear="mouseout",  # Ripristina su mouse-out
    empty="all"  # Mostra tutto all'inizio
)

# Grafico principale della torta
platform_pie = (
    alt.Chart(data_platform_pie)
    .mark_arc(radius = 205)
    .encode(
        theta=alt.Theta("Users:Q", stack=True),  # Grandezza degli archi
        color=alt.Color(
            "Primary streaming service:N",
            scale=alt.Scale(scheme="category10"),  # Schema colori
            title="Piattaforma di Streaming"
        ),
        opacity=alt.condition(
            highlight_arc_and_label, alt.value(1), alt.value(0.5)  # Modifica opacità in base alla selezione
        ),
        tooltip=[
            alt.Tooltip("Primary streaming service:N", title="Piattaforma"),
            alt.Tooltip("Users:Q", title="Numero di Utenti"),
            alt.Tooltip("Percentage:Q", title="Percentuale (%)", format=".2f")
        ]
    )
    .add_selection(highlight_arc_and_label)  # Aggiunge la selezione
    .properties(
        title="Distribuzione delle Piattaforme di Streaming",
        height=508
    )
)

# Etichette con il nome accanto alla torta
platform_pie_labels = (
    alt.Chart(data_platform_pie)
    .mark_text(radius=170, size=12, fontWeight="bold", dy=0)  # Imposta raggio e dimensione
    .encode(
        theta=alt.Theta("Users:Q", stack=True),
        text=alt.Text("Primary streaming service:N"),  # Nome della piattaforma
        color=alt.value("black"),
        opacity=alt.condition(
            highlight_arc_and_label,  # Stessa selezione per torta e nomi
            alt.value(1),  # Opacità completa per sezione evidenziata
            alt.value(0.5)  # Sbiadite per sezioni non evidenziate
        )
    )
    .add_selection(highlight_arc_and_label)  # Usa la stessa selezione
)

# Etichette di percentuale accanto alla torta
platform_pie_percentage_labels = (
    alt.Chart(data_platform_pie)
    .mark_text(radius=223, size=15, fontWeight="bold", dx=6)  # Configura le etichette
    .encode(
        theta=alt.Theta("Users:Q", stack=True),  # Usa il theta per posizionare le etichette
        text=alt.Text("Percentage_Label:N"),  # Usa la colonna con il simbolo '%'
        color=alt.Color(
            "Primary streaming service:N",
            scale=alt.Scale(scheme="category10"),  # Schema colori
            title="Piattaforma di Streaming"
        ),
        opacity=alt.condition(
            highlight_percentage,  # Selezione separata per evidenziare
            alt.value(1),  # Opacità completa durante l'evidenziazione
            alt.value(0.5)  # Sbiadito per le altre sezioni
        )
    )
    .add_selection(highlight_percentage)  # Selezione per il tooltip
)

# Combina torta, nomi e percentuali
platform_pie_combined = (
    platform_pie + platform_pie_labels + platform_pie_percentage_labels
).properties(
    title="Distribuzione delle Piattaforme di Streaming"  # Titolo del grafico combinato
).configure_title(
    fontSize=25,  # Imposta la dimensione del titolo
    anchor="start",  # Posiziona il titolo a sinistra
    color="black"  # Colore del titolo
)

# Mostra il grafico in Streamlit
st.altair_chart(platform_pie_combined, use_container_width=True)

st.write("""
**Spotify** si conferma come la piattaforma musicale più utilizzata (**62.31%**), dominando nettamente il panorama dello streaming musicale.  
Tuttavia, anche altre piattaforme si dimostrano rilevanti, come **YouTube Music**, che, nonostante sia un servizio relativamente nuovo (2015), ottiene un notevole successo con una quota pari al **12.79%**.

Un dato interessante e forse inaspettato è rappresentato dal **9.66%** degli utenti che dichiarano di non utilizzare alcuna piattaforma di streaming musicale.  
Questa percentuale potrebbe riflettere l'abitudine di ascoltare musica in modi più tradizionali, come vinili o la radio.
""")





### BOXPLOT PER VALUTARE LE ORE DI ASCOLTO PER GENERE PREFERITO

# Filtra i dati per il boxplot: rimuove i valori nulli e seleziona le colonne di interesse
data_hours_boxplot = (
    data.filter(
        pl.col("Hours per day").is_not_null() & 
        pl.col("Fav genre").is_not_null())
)

# Ordina i generi in base alla mediana
order = (
    data_hours_boxplot.group_by("Fav genre") # Raggruppa i dati per la variabile di interesse
    .agg(pl.median("Hours per day").alias("Median")) # Calcola la mediana
    .sort(["Median", "Fav genre"]) # Ordina prima per mediana appena calcolata, poi alfabeticamente (in quanto ci sono più generi che hanno mediana uguale)
    .select("Fav genre") # Seleziona solo i generi
    .to_series() # Converte in una serie
    .to_list() # Converte in una lista
) 
  
hours_boxplot = (
    alt.Chart(data_hours_boxplot)  
    .mark_boxplot(color="orange")  # Specifica il colore del boxplot (arancione)
    .encode(
        x=alt.X("Fav genre:N", title="Genere musicale preferito", sort=order),  # L'asse x rappresenta i generi musicali preferiti, ordinati secondo `order`
        y=alt.Y("Hours per day:Q", title="Ore di ascolto al giorno")  # L'asse y rappresenta le ore medie di ascolto al giorno
    )    
    .properties(
        title="Distribuzione delle ore di ascolto per genere musicale preferito",  # Titolo del grafico
        height=500  # Altezza del grafico
    )
    .configure_title(fontSize=25)  # Imposta una dimensione maggiore per il titolo del grafico
)

st.altair_chart(hours_boxplot, use_container_width=True)

st.write("""
Il grafico mostra la distribuzione delle ore di ascolto giornaliere per genere musicale. Si notano alcune tendenze interessanti:

- **Jazz** e **Latin** hanno la maggiore variabilità, con diversi outlier che superano le 18 ore di ascolto.
- **Gospel** e **Lofi** presentano una distribuzione compatta.
- Generi come **Pop**, **EDM** e **Hip Hop** mostrano una distribuzione uniforme, indicando abitudini di ascolto regolari.

Questi dati suggeriscono una varietà di comportamenti di ascolto tra i diversi generi musicali.
""")






### AREA PLOT: ORE MEDIE DI ASCOLTO PER ETÀ

# Prepara i dati
processed_data = (  
    data.group_by("Age")  # Raggruppa i dati per età
    .agg(pl.mean("Hours per day").alias("Avg hours per day"))  # Calcola la media delle ore per ogni gruppo
    .sort("Age")  # Ordina i dati per età (crescente)
)

# Crea una selezione interattiva
nearest = alt.selection_single(  
    name="age_selector", # Nome univoco per prevenire conflitti con altre selezioni
    fields=["Age"], # Campo per l'interazione
    nearest=True, # Attiva la selezione per il punto più vicino al cursore
    on="mousemove", # Seleziona il punto quando si muove il mouse 
    empty="none" # Nessuna selezione iniziale
)

# Grafico ad area
area = (  
    alt.Chart(processed_data) 
    .mark_area(  
        line={"color": "darkgreen"}, # Linea verde scuro sopra l'area
        color=alt.Gradient( # Gradiente per riempire l'area
            gradient="linear",
            stops=[
                alt.GradientStop(color="white", offset=0), # Bianco alla base
                alt.GradientStop(color="darkgreen", offset=1) # Verde scuro in alto
            ],
            x1=0, x2=0, y1=1.7, y2=0 # Configura la direzione del gradiente
        )
    )
    .encode(
        x=alt.X("Age:Q", title="Età", scale=alt.Scale(domain=[10, 80])), # Asse x per l'età
        y=alt.Y("Avg hours per day:Q", title="Ore Medie di Ascolto") # Asse y per la media delle ore
    )
)

# Linea verticale interattiva
vertical_line = (  
    alt.Chart(processed_data)  
    .mark_rule(color="black") # Linea verticale nera
    .encode(
        x="Age:Q",  # Posizionata sull'asse x
        opacity=alt.condition(nearest, alt.value(1), alt.value(0)),  # Appare solo se il punto è selezionato
        strokeDash=alt.value([5, 5]),  # Linea tratteggiata (5 pixel tratto, 5 pixel spazio)
        tooltip=[  # Aggiunge il tooltip per mostrare informazioni dettagliate
            alt.Tooltip("Age:Q", title="Età"),  # Mostra l'età
            alt.Tooltip("Avg hours per day:Q", title="Ore Medie", format=".2f")  # Mostra le ore medie formattate
        ]
    )
    .add_selection(nearest)  # Aggiunge l'interattività definita in `nearest`
)

# Linea orizzontale interattiva
horizontal_line = (  
    alt.Chart(processed_data)  # Usa gli stessi dati
    .mark_rule(color="black")  # Linea orizzontale nera
    .encode(
        y="Avg hours per day:Q",  # Posizionata sull'asse y
        opacity=alt.condition(nearest, alt.value(1), alt.value(0)),  # Appare solo se il punto è selezionato
        strokeDash=alt.value([5, 5])  # Linea tratteggiata (5 pixel tratto, 5 pixel spazio)
    )
)

# Punto interattivo per evidenziare i valori
point = (  
    alt.Chart(processed_data) 
    .mark_circle(size=95, color="red")  # Punto evidenziato in rosso
    .encode(
        x="Age:Q",  # Posizionato sull'asse x in base all'età
        y="Avg hours per day:Q"  # Posizionato sull'asse y in base alle ore medie
    )
    .transform_filter(nearest)  # Mostra solo il punto selezionato con `nearest`
)

# Combina i grafici
interactive_chart = (  
    alt.layer(area, vertical_line, horizontal_line, point)  # Combina i layer
    .resolve_scale(x='shared', y='shared')  # Condivide le scale tra i grafici
    .properties(
        title="Ore Medie di Ascolto Musicale al Giorno in Funzione dell'Età",  # Titolo del grafico
        height=450  # Altezza del grafico
    )
    .configure_title(fontSize=25)  # Dimensione del font per il titolo
)

# Mostra il grafico in Streamlit
st.altair_chart(interactive_chart, use_container_width=True)  # Adatta il grafico alla larghezza del container


# Aggiungi una descrizione
st.write("""
Il grafico mostra le ore medie di ascolto al giorno per ogni età. Si osserva una certa 
stabilità nelle ore medie di ascolto tra i 15 e i 50 anni, con oscillazioni relativamente contenute. 
Tuttavia, emerge un picco notevole intorno ai 55 anni, suggerendo che questa fascia potrebbe 
includere individui con abitudini di ascolto particolarmente elevate.

Dopo il picco, le ore medie di ascolto si ristabilizzano, anche se con un'alta varianza. 

Nel complesso, il grafico evidenzia come l'età influenzi le abitudini di ascolto, con variazioni 
interessanti in determinate fasce di età.
""")





### GRAFICO A BARRE PER OSSERVARE LA DISTRIBUZIONE DEL GENERE PREFERITO

total_users = data.shape[0] # Misuro il totale delle righe (non ci sono dati mancanti quindi non serve filtrare)

# Conta il numero di preferenze per ciascun genere musicale nella colonna 'Fav genre'
genre_counts = (
    data.group_by('Fav genre')
    .agg(pl.count().alias('Conteggio'))
    .with_columns(
        (pl.col('Conteggio') / total_users * 100).alias('Percentuale')
    )
    .sort('Conteggio', descending=True)
)

# Crea una selezione per evidenziare una barra quando viene passata con il mouse
highlight = alt.selection_single(on='mouseover', fields=['Fav genre'], empty='none')

# Crea il grafico a barre per la distribuzione dei generi preferiti
fav_genre_bar_chart = (
    alt.Chart(genre_counts)
    .mark_bar(stroke="black", strokeWidth=1) # Segna i contorni delle colonne
    .encode(
        y=alt.X('Fav genre:N', title='Genere Musicale', sort='-x'),
        x=alt.Y('Percentuale:Q', title='Percentuale (%)', scale=alt.Scale(domain=[0, 26])),
        color=alt.condition(
            highlight, 
            alt.value('green'), # Colore quando evidenziato
            alt.value('red') # Colore normale
        ),
        tooltip=[
            alt.Tooltip('Fav genre:N', title='Genere Musicale'),
            alt.Tooltip('Conteggio:Q', title='Numero di Utenti'),
            alt.Tooltip('Percentuale:Q', title='Percentuale (%)', format=".2f")
        ]
        )
    .properties(
        title='Distribuzione dei Generi Musicali Preferiti',
        height=450
        )
    .add_selection(highlight)  # Aggiunge la selezione per l'evidenziazione
    .configure_title(fontSize=25) # Imposta un font più grande per i titoli del grafico
)

st.altair_chart(fav_genre_bar_chart, use_container_width=True)


st.write("""
Il grafico evidenzia i generi musicali più apprezzati dagli utenti. Il Rock emerge chiaramente come il genere preferito, 
seguito dal Pop e dal Metal. 
Questi tre generi dominano la classifica (assieme rappresentano i generi preferiti di più del **50%** degli utenti), 
suggerendo una forte popolarità tra una vasta gamma di ascoltatori.

Generi come Classical e Video Game Music occupano posizioni centrali, dimostrando una nicchia significativa di ascoltatori dedicati.

Al contrario, generi come Gospel e Latin risultano i meno rappresentati, indicando una preferenza minore tra gli utenti. 
Questa distribuzione riflette una diversità di gusti musicali, con una marcata concentrazione verso i tre generi più ascoltati.
""")





### GRAFICO A BARRE PER OSSERVARE LA FREQUENZA DI ASCOLTO PER OGNI GENERE 

# Mostra il titolo principale sopra il selettore
st.write("### Frequenze di Ascolto per Genere Musicale")

# Filtra solo le colonne dei generi musicali (quelle che iniziano con "Frequency")
frequency_columns = [col for col in data.columns if col.startswith("Frequency [")]
frequencies = data.select(frequency_columns)

# Ottieni l'elenco dei generi
genres = [col.replace("Frequency [", "").replace("]", "") for col in frequency_columns]

# Aggiungi un selectbox per selezionare il genere musicale
selected_genre = st.selectbox("Seleziona un genere musicale:", genres)

# Filtra i dati per il genere selezionato
selected_column = f"Frequency [{selected_genre}]"
genre_counts = frequencies.group_by(selected_column).count()

# Calcola il totale e aggiungi la percentuale
total_count = genre_counts["count"].sum()
genre_counts = genre_counts.with_columns(
    (pl.col("count") / total_count * 100).alias("Percentuale")
)

# Converte in un DataFrame compatibile con Altair
genre_data = genre_counts
genre_data.columns = ['Frequenza', 'Conteggio', 'Percentuale']  # Rinomina le colonne

# Crea un grafico a barre orizzontale
genre_frequency_chart = (
    alt.Chart(genre_data)  
    .mark_bar()  # Disegna un grafico a barre
    .encode(
        x=alt.X('Conteggio:Q', title='Conteggio', scale=alt.Scale(domain=[0, 600])),  # Asse x rappresenta i conteggi con un limite massimo di 600
        y=alt.Y(
            'Frequenza:O',  # Asse y rappresenta le categorie di frequenza
            title="Frequenza"  # Titolo dell'asse y
        ),
        color=alt.Color('Frequenza:O', scale=alt.Scale(scheme='inferno')),  # Colore basato sulla frequenza, con scala `inferno`
        tooltip=[  # Tooltip che mostra la frequenza, il conteggio e la percentuale
            alt.Tooltip('Frequenza:O', title="Frequenza"),
            alt.Tooltip('Conteggio:Q', title="Conteggio"),
            alt.Tooltip('Percentuale:Q', title="Percentuale (%)", format=".2f")
        ]
    )
    .properties(
        height=500  # Imposta l'altezza del grafico
    )
)

# Mostra il grafico
st.altair_chart(genre_frequency_chart, use_container_width=True)

# Aggiungi la descrizione testuale
st.write("""
Il grafico mostra la distribuzione delle frequenze di ascolto per il genere musicale selezionato. 

Questo tipo di visualizzazione aiuta a capire meglio la popolarità e le abitudini di ascolto relative a 
ciascun genere musicale.
""")
