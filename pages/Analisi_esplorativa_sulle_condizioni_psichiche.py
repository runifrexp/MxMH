import altair as alt
import polars as pl
import streamlit as st
import numpy as np
import data_cleaning

# Imposta il nome che viene fuori nel browser con emoji
st.set_page_config(
    page_title="MxMH",
    page_icon=":brain:"
)

# Importo i dati con la funzione definita in data_cleaning.py (get_data)
data = data_cleaning.get_data()

st.markdown("""
# Analisi esplorativa sulle condizioni psichiche

In questa sezione verranno studiati dati relativi alle **condizioni psichiche**. Gli aspetti che verranno indagati sono:

- La distribuzione delle condizioni psichiche: Ansia, Depressione, Insonnia e Disturbo Ossessivo-Compulsivo.
- La relazione tra età e livelli delle condizioni psichiche.
- Gli effetti che la musica ha sulle condizioni psichiche: Migliora, Nessun effetto, Peggiora.
- Eventuali correlazioni tra le varie condizioni.
  """)





### DENSITÀ PER LE CONDIZIONI 

# Titolo messo prima altrimenti uscirebbe prima il select per le condizioni
st.write("### Curve di Densità delle Condizioni Psichiche")

# Variabili delle condizioni psichiche
psych_conditions = ["Anxiety", "Depression", "Insomnia", "OCD"]
condition_dens_data = data.select(psych_conditions) # Seleziona solo le colonne delle condizioni

# Trasforma i dati in formato long per Altair
long_data = condition_dens_data.melt(
    value_vars=psych_conditions,
    variable_name="Condition", # Nome della variabile categoriale
    value_name="Value" # Nome della variabile numerica
).filter(pl.col("Value").is_not_null()) # Rimuove valori nulli

# Seleziona le condizioni da visualizzare
selected_conditions = st.multiselect(
    "Seleziona le condizioni da visualizzare:", # Titolo del selettore
    options=psych_conditions, # Opzioni disponibili
    default=psych_conditions, # Selezione predefinita
    key="condition_selector" # Chiave per Streamlit
)

# Filtra i dati in base alle condizioni selezionate
filtered_long_data = long_data.filter(pl.col("Condition").is_in(selected_conditions))

# Colori personalizzati per ogni condizione
custom_colors = ['#1f77b4', # Blu per Anxiety
                 '#ff7f0e', # Arancione per Depression
                 '#2ca02c', # Verde per Insomnia
                 '#d62728'] # Rosso per OCD

# Grafico delle curve di densità
condition_dens = (
    alt.Chart(filtered_long_data)
    .transform_density(
        'Value', # Variabile numerica da convertire in densità
        as_=['Value', 'density'], # Output della densità
        groupby=['Condition'] # Calcola la densità per ogni condizione
    )
    .mark_line(size=2) # Linea per rappresentare la densità
    .encode(
        alt.X('Value:Q', 
            title="Livello delle Condizioni",
            scale=alt.Scale(domain=[0, 10]) # Misurazioni delle condizioni da 0 a 10
            ),  
        alt.Y('density:Q', 
            title="Densità", 
            scale=alt.Scale(domain=[0, 0.25]) # Dato che le densità non superano il 0.25, per avere un buon impatto visivo
            ),              
        alt.Color(
            'Condition:N', # Colore in base alla condizione
            title="Condizione Psichica", # Titolo della legenda
            scale=alt.Scale(domain=["Anxiety", "Depression", "Insomnia", "OCD"], range=custom_colors)  # Colori personalizzati
        )
    )
    .properties(height=400) # Altezza del grafico
)

# Selezione interattiva sul grafico
nearest = alt.selection_single(
    fields=['Value'], # Campo per la selezione
    nearest=True, # Seleziona il punto più vicino
    on='mousemove', # Attivazione con il movimento del mouse
    empty='none' # Nessuna selezione se non si è sopra con il mouse
)

# Crea dinamicamente il tooltip in base alle condizioni selezionate
tooltip = [
    alt.Tooltip('Value:Q', title="Valore", format=".2f") # Tooltip per il valore
    ] + [
    alt.Tooltip(f'{condition}:Q', title=f"Densità {condition}", format=".4f") # Tooltip per la densità di ogni condizione
    for condition in selected_conditions
]

# Linea verticale interattiva con tooltip
rule = (
    alt.Chart(filtered_long_data)
    .transform_density(
        'Value',                               # Variabile numerica
        as_=['Value', 'density'],              # Output della densità
        groupby=['Condition']                  # Calcola la densità per ogni condizione
    )
    .transform_pivot(
        'Condition',                           # Trasforma la condizione in colonne
        value='density',                       # Valori per ogni condizione
        groupby=['Value']                      # Raggruppa per i valori
    )
    .mark_rule(color='black')                  # Linea verticale nera
    .encode(
        x='Value:Q',                           # Posizione sulla X
        tooltip=tooltip,                       # Tooltip dinamico
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))  # Opacità controllata dalla selezione
    )
    .add_selection(nearest)                    # Aggiunge la selezione interattiva
)

# Punti interattivi per ogni condizione con tooltip
points = (
    alt.Chart(filtered_long_data)
    .transform_density(
        'Value', # Variabile numerica da trasformare in densità
        as_=['Value', 'density'], # Output della densità
        groupby=['Condition'] # Calcola la densità per ogni condizione
    )
    .mark_circle(size=100) # Punti evidenziati
    .encode(
        x='Value:Q', # Posizione sulla X
        y='density:Q', # Posizione sulla Y
        color=alt.Color(
            'Condition:N', # Colore in base alla condizione
            title="Condizione", # Titolo della legenda
            scale=alt.Scale(domain=["Anxiety", "Depression", "Insomnia", "OCD"], range=custom_colors)  # Colori personalizzati
        ),
        tooltip=[
            alt.Tooltip('Value:Q', title="Valore", format=".2f"), # Tooltip per il valore
            alt.Tooltip('Condition:N', title="Condizione"), # Tooltip per la condizione
            alt.Tooltip('density:Q', title="Densità", format=".4f") # Tooltip per la densità
        ]
    )
    .transform_filter(nearest)                 # Mostra i punti solo vicino alla selezione
)

# Combina il grafico di densità, la linea verticale e i punti interattivi
interactive_chart_dens = condition_dens + rule + points

st.altair_chart(interactive_chart_dens, use_container_width=True)  # Ridimensionamento automatico

# Introduzione al grafico delle curve di densità
st.write("""
Questo grafico mostra le curve di densità per le quattro condizioni psichiche: **Ansia**, **Depressione**, **Insonnia** e **OCD**. 
Le linee colorate rappresentano la distribuzione stimata dei livelli di ciascuna condizione su una scala da 0 a 10. 
La linea verticale interattiva e i punti evidenziano i valori di densità specifici al passaggio del mouse, 
consentendo un'esplorazione dettagliata delle distribuzioni.
""")





### VIOLIN PLOT PER I LIVELLI DEI QUATTRO DISTURBI

# Trasforma i dati per il violin plot
violin_data = (
    long_data
    .filter(pl.col("Condition").is_in(psych_conditions))  # Filtra solo le condizioni selezionate
)

## Trasforma i dati per il violin plot
violin_data = (
    long_data
    .filter(pl.col("Condition").is_in(psych_conditions))  # Filtra solo le condizioni selezionate
)

# Violin plot per le condizioni psichiche
cond_violin_plot = (
    alt.Chart(violin_data, width=100) # Grafico base
    .transform_density(
        'Value', # Variabile su cui calcolare la densità
        as_=['Value', 'density'], # Colonne risultanti dalla trasformazione
        extent=[-3, 14], # Estensione dei valori (livelli delle condizioni)
        groupby=['Condition'] # Raggruppa per condizione
    )
    .mark_area(orient='horizontal') # Area per rappresentare i violini
    .encode(
        x = alt.X('density:Q') # Asse X: densità
                .stack('center') # Centra i violini
                .axis(None), # Configurazione dell'asse (no assi x in quanto non servono)
        y = alt.Y('Value:Q', title="Livello"), # Asse Y: livelli delle condizioni
        color = alt.Color(
                'Condition:N', # Colore in base alla condizione
                scale=alt.Scale(
                    domain=["Anxiety", "Depression", "Insomnia", "OCD"], 
                    range=custom_colors
            )
        ), # Colori personalizzati
        column = alt.Column(
                'Condition:N', # Facettatura per condizione
                spacing=0, # Spaziatura tra i facetti
                header=alt.Header(
                    titleOrient='bottom', 
                    labelOrient='bottom', 
                    labelPadding=5
            ) # Configurazione dell'header
        )
    )
    .configure_view(stroke=None) # Rimuove i bordi attorno ai violini
    .properties(
        height = 400,
        width = 140,
        title="Distribuzione delle Condizioni Psichiche"
    )
    .configure_title(fontSize=25) # Imposta un font più grande per i titoli del grafico

)

# Mostra il grafico in Streamlit
st.altair_chart(cond_violin_plot)

st.write("""

Questo grafico a violino mostra la distribuzione dei livelli per ogni condizione psichica: 
**Ansia**, **Depressione**, **Insonnia** e **OCD**. Ogni *violino* rappresenta la densità dei dati, 
e la larghezza indica la frequenza relativa dei livelli riportati. 

Ad esempio, si osserva che:
- **Anxiety** ha una distribuzione concentrata verso i livelli più alti, suggerendo una prevalenza di livelli significativi.
- **Depression** mostra una distribuzione più uniforme con un picco verso il valore 7.
- **Insomnia** tende ad avere una distribuzione che diminuisce all'aumentare del livello, con un picco attorno a valori bassi.
- **OCD** presenta una distribuzione molto concentrata verso valori molto bassi.


""")





### BUBBLE CHART PER ETÀ, NUMERO DI RISPONDENTI E LIVELLO DELLA CONDIZIONE SELEZIONATA

st.write("### Relazione tra Età e Livello Medio della condizione selezionata")

# Selezione della condizione con una chiave univoca
selected_condition = st.selectbox(
    "Seleziona una condizione da visualizzare:",
    options=psych_conditions,
    index=0,
    key="bubble_chart_condition"
)

# Aggregazione dei dati per età
aggregated_data = (
    data.group_by("Age")
    .agg([
        pl.col(selected_condition).mean().alias("mean_condition"),  # Media della condizione per età
        pl.col(selected_condition).count().alias("count")  # Numero di rispondenti per età
    ])
)

# Crea una selezione interattiva per l'highlight
highlight = alt.selection_single(
    on="mouseover",  # Attiva l'highlight al passaggio del mouse
    empty="none",  # Nessuna selezione di default
    fields=["Age", "mean_condition"]  # Campi su cui effettuare la selezione
)

# Creazione del grafico a bolle con highlight e contorno nero
bubble_chart = (
    alt.Chart(aggregated_data)
    .mark_circle(strokeWidth=2)  # Imposta lo spessore del contorno
    .encode(
        x=alt.X("Age:Q", title="Età"),  # Asse X con l'età
        y=alt.Y("mean_condition:Q", title=f"Media Livello di {selected_condition}"),  # Asse Y con la media
        size=alt.Size("count:Q", title="Numero di Rispondenti", scale=alt.Scale(range=[40, 450])),  # Dimensione delle bolle
        color=alt.Color(
            "count:Q",
            title="Numero di Rispondenti",
            scale=alt.Scale(scheme="cividis")  # Colore in base al numero di rispondenti (ottimizzato per daltonismo)
        ),
        opacity=alt.condition(
            highlight,  # Cambia l'opacità in base alla selezione
            alt.value(1),  # Opacità completa per la bolla evidenziata
            alt.value(0.7)  # Trasparenza per le altre bolle
        ),
        stroke=alt.condition(
            highlight,  # Cambia il colore del contorno in base alla selezione
            alt.value("black"),  # Contorno nero per la bolla evidenziata
            alt.value(None)  # Nessun contorno per le altre bolle
        ),
        tooltip=[
            alt.Tooltip("Age:Q", title="Età"),
            alt.Tooltip("mean_condition:Q", title=f"Media {selected_condition}", format=".2f"),
            alt.Tooltip("count:Q", title="Numero di Rispondenti")
        ]
    )
    .add_selection(highlight)  # Aggiunge la selezione interattiva
    .properties(height=500)
)

# Mostra il grafico in Streamlit
st.altair_chart(bubble_chart, use_container_width=True)

st.write("""
Questo grafico a bolle aggrega i dati per età e mostra la relazione tra 
l'età e il livello medio della condizione selezionata. La dimensione delle bolle 
indica il numero di rispondenti, mentre il colore rappresenta una scala crescente 
in base al numero di rispondenti stessi.
""")





### HEATMAP CON CORRELAZIONI TRA LE CONDIZIONI

# Calcolo della matrice di correlazione
conditions_data = data.select(psych_conditions)  # Estrai solo le condizioni psichiche
correlation_matrix = np.corrcoef(
    [conditions_data[col] for col in psych_conditions]
)

# Creazione del DataFrame per la heatmap
correlation_df = pl.DataFrame({
    "Condition1": np.repeat(psych_conditions, len(psych_conditions)),
    "Condition2": np.tile(psych_conditions, len(psych_conditions)),
    "Correlation": correlation_matrix.flatten()
})

# Heatmap con i valori di correlazione
heatmap = (
    alt.Chart(correlation_df)
    .mark_rect()
    .encode(
        x=alt.X("Condition1:N", title="Condizione Psichica", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Condition2:N", title="Condizione Psichica"),
        color=alt.Color(
            "Correlation:Q",
            scale=alt.Scale(scheme="redyellowgreen", domain=[-1, 1]),
            title="Correlazione"
        )
    )
    .properties(
        title="Matrice di Correlazione tra le Condizioni Psichiche",
        height=400
    )
)

# Aggiunta dei valori di correlazione come testo
text = (
    alt.Chart(correlation_df)
    .mark_text()
    .encode(
        x=alt.X("Condition1:N", title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Condition2:N", title=None),
        text=alt.Text("Correlation:Q", format=".2f"),  # Valori di correlazione con 2 decimali
        color=alt.condition(
            "datum.Correlation > 0.5 || datum.Correlation < -0.5",
            alt.value("white"),  # Testo bianco per forti correlazioni (per renderlo leggibile)
            alt.value("black")   # Testo nero per deboli correlazioni (per renderlo leggibile)
        )
    )
)

# Grafico combinato
correlation_chart = (heatmap + text).configure_title(fontSize=25) # Imposta un font più grande per i titoli del grafico

# Mostra il grafico in Streamlit
st.altair_chart(correlation_chart, use_container_width=True)

st.write("""
La matrice di correlazione evidenzia la relazione tra le diverse condizioni psichiche. 

- **Anxiety** e **Depression** mostrano una correlazione positiva relativamente alta (**0.52**), suggerendo una frequente co-occorrenza di queste due condizioni.
- **Insomnia** presenta correlazioni più moderate con le altre condizioni, come Anxiety (**0.29**) e Depression (**0.38**), indicando un possibile legame ma meno intenso.
- **OCD** ha una correlazione positiva bassa con le altre condizioni, in particolare con Depression (**0.20**) e Insomnia (**0.23**), il che suggerisce una minore interdipendenza.

È importante notare che tutte le correlazioni sono positive, ciò significa che tra tutte le condizioni c'è un legame che può essere più o meno forte.

Questi risultati evidenziano l'importanza di indagare ulteriormente le relazioni più forti, come quella tra Anxiety e Depression, per comprendere meglio le dinamiche delle condizioni psichiche.
""")
