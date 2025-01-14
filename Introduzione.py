import streamlit as st

# Imposta il nome che viene fuori nel browser
st.set_page_config(
    page_title="MxMH",
    page_icon=":bar_chart:"
)
	
st.title("Analisi dell'Impatto della Musica sul Benessere Psichico")

st.write("""
La musica rappresenta un elemento essenziale della vita umana. Numerosi studi scientifici hanno esplorato il suo 
impatto sul benessere psichico, dimostrando che l'ascolto della musica può migliorare significativamente la qualità 
della vita, ridurre lo stress e promuovere il rilassamento. Tuttavia, in alcune circostanze, può anche portare a un peggioramento delle condizioni psichiche.

### Riferimenti Scientifici

- Uno studio pubblicato su *Frontiers in Psychology* ha mostrato che l'ascolto consapevole della musica può aiutare i giovani con tendenze depressive 
  a regolare l'umore, migliorando lo stato emotivo e promuovendo il benessere psichico.

- Ricercatori dell'*International Institute of Information Technology of Hyderabad* hanno analizzato 
  come un intervento basato sulla musica, combinato con stimolazione sensoriale ritmica, possa migliorare i sintomi depressivi. Questo suggerisce che la musica può avere un ruolo 
  terapeutico nell'affrontare la depressione.

- L'*Organizzazione Mondiale della Sanità (OMS)* ha riconosciuto ufficialmente la musicoterapia (e in generale le pratiche artistiche) come uno strumento efficace per affrontare 
disturbi mentali, come ansia e depressione. Ha inoltre sottolineato l'importanza della musica nei programmi di salute mentale.

Questi risultati rafforzano l'idea che la musica possa rappresentare una preziosa risorsa per migliorare il benessere mentale, 
oltre a ispirare ulteriori ricerche sull'interazione tra musica e psicologia.

### Obiettivi del Progetto
Questo progetto si propone di analizzare il ruolo della musica nella vita quotidiana e il suo impatto sul benessere psichico, utilizzando un dataset che raccoglie informazioni 
anonime sulle abitudini musicali e le condizioni mentali degli utenti. 

L'analisi si suddivide in tre parti:

1. **Analisi esplorativa sulle abitudini musicali**: Un'analisi dettagliata sui generi musicali ascoltati, le abitudini e su informazioi riguardanti gli utenti.
2. **Analisi esplorativa sulle condizioni psichiche**: Uno studio sui dati relativi al benessere mentale, in specifico sulle condizioni di ansia, depressione, disturbo ossessivo 
compulsivo e insonnia.
3. **Analisi incrociata**: Un'indagine sulle relazioni tra abitudini musicali e stati mentali per identificare correlazioni significative.

Per visitare le varie sezioni, aprire il menù sulla sinistra.

### Importanza del Progetto
Con l'aumento dei disturbi mentali su scala globale, specialmente dopo la pandemia di COVID-19, comprendere il potenziale della musica come strumento terapeutico rappresenta 
una strada promettente per migliorare la qualità della vita e il benessere psichico.

**Fonti Utilizzate**:
- [_Frontiers in Psychology_](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.01199/full)
- [_International Institute of Information Technology of Hyderabad_](https://arxiv.org/pdf/2009.13685)
- [_Organizzazione Mondiale della Sanità_](https://www.nbst.it/571-benessere-salute-arte-oms-health-evidence-network-revisione-evidenze.html)
- [_Dataset_](https://www.kaggle.com/datasets/catherinerasgaitis/mxmh-survey-results/data)
""")
