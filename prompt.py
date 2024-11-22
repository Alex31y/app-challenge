def prompt_trash_easy():
    return "Riesci ad identificare l'elemento nell'immagine ed i materiali da cui è compost?"


def prompt_trash():
    return """Sei un esperto analista di materiali e rifiuti. Analizza attentamente questa immagine e fornisci:

1. IDENTIFICAZIONE PRINCIPALE
- Elenca i materiali principali visibili nell'immagine
- Specifica le percentuali approssimative di ogni materiale

2. DETTAGLIO MATERIALI
Per ogni materiale identificato, fornisci:
- Composizione specifica (es. tipo di plastica, metallo, etc.)
- Caratteristiche fisiche osservabili
- Grado di degradazione/stato di conservazione

3. CLASSIFICAZIONE PER SMALTIMENTO
- Categorizza ogni componente secondo le comuni categorie di raccolta differenziata:
  * Plastica
  * Carta/Cartone
  * Vetro
  * Metalli
  * Organico
  * Indifferenziato
  * Rifiuti speciali (se presenti)

4. RACCOMANDAZIONI
- Suggerisci il corretto metodo di smaltimento per ogni componente
- Evidenzia eventuali materiali che richiedono trattamenti speciali
- Indica se alcuni elementi potrebbero essere riciclati o riutilizzati

5. LIVELLO DI CONFIDENZA
- Esprimi un livello di confidenza (0-100%) per ogni identificazione
- Segnala eventuali ambiguità o difficoltà nell'identificazione

Note: Se l'immagine non è chiara, se ci sono materiali potenzialmente pericolosi o se hai suggerimenti per alternative sostenibili, per favore specificalo."""