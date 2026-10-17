class Stand:
    def __init__(self, codice, mq, padiglione, prezzo):
        self.codice=codice
        self.mq=float(mq)
        self.padiglione=int(padiglione)
        self.prezzo=float(prezzo)
        self.disponibile=True
        self.espositore=None

class StandStandard(Stand):
    def __str__(self):
        return f'{self.codice}: Standard | {self.mq} mq - Padiglione {self.padiglione} - Prezzo {self.prezzo:.2f}€'

class StandElettrici(Stand):
    def __init__(self, codice, mq, padiglione, prezzo, prese):
        prezzo=prezzo*(1+0.07*prese)
        super().__init__(codice, mq, padiglione, prezzo)
        self.prese=int(prese)

    def __str__(self):
        return f'{self.codice}: Elettrico | {self.mq} mq - Padiglione {self.padiglione} - Prezzo {self.prezzo:.2f}€ - N. Prese: {self.prese}'

class StandPremium(Stand):
    def __init__(self, codice, mq, padiglione, prezzo, posizione):
        prezzo=prezzo*1.30
        super().__init__(codice, mq, padiglione, prezzo)
        self.posizione=posizione

    def __str__(self):
        return f'{self.codice}: Premium | {self.mq} mq - Padiglione {self.padiglione} - Prezzo {self.prezzo:.2f}€ - Posizione: {self.posizione}'

class Espositori:
    def __init__(self, codice, nome, cognome):
        self.codice=codice
        self.nome=nome
        self.cognome=cognome
        self.stand_assegnato=None

    def __str__(self):
        return f'{self.codice}: Espositore | Nome: {self.nome} - Cognome: {self.cognome}'

class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self.nome=nome
        self.lista_stand=[]
        self.lista_espositori=[]

    """Aggiungere setter e getter se necessari"""
    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        with open(file_path, "r", encoding='utf-8') as file:
            for line in file:
                line=line.strip().split(',')
                if not line:
                    continue
                if line[0].startswith('ST'):
                    codice=line[0]
                    mq=float(line[1])
                    padiglione=int(line[2])
                    prezzo=float(line[3])
                    if len(line)==4:
                        stand=StandStandard(codice, mq, padiglione, prezzo)
                    elif len(line)>4:
                        if line[4].isdigit():
                            prese=int(line[4])
                            stand=StandElettrici(codice, mq, padiglione, prezzo, prese)
                        else:
                            posizione=line[4]
                            stand=StandPremium(codice, mq, padiglione, prezzo, posizione)
                    self.lista_stand.append(stand)
                elif line[0].startswith('ES'):
                    codice=line[0]
                    nome=line[1]
                    cognome=line[2]
                    espositore=Espositori(codice, nome, cognome)
                    self.lista_espositori.append(espositore)

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        stand=None
        espositore=None
        for s in self.lista_stand:
            if s.codice==codice_stand:
                stand=s
                break
        for e in self.lista_espositori:
            if e.codice==codice_espositore:
                espositore=e
                break

        if not stand:
            raise ValueError(f"Stand non trovato.")
        if not espositore:
            raise ValueError(f"Espositore non trovato.")
        if not stand.disponibile:
            raise ValueError(f"Lo stand non è disponibile.")
        if espositore.stand_assegnato is not None:
            raise ValueError(f"L'espositore ha già uno stand assegnato.")

        stand.disponibile=False
        stand.espositore=espositore
        espositore.stand_assegnato=stand

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        for e in self.lista_espositori:
            if e.stand_assegnato:
                print(f"{e}: Espositore assegnato allo Stand {e.stand_assegnato.codice}")
            else:
                print(f"{e}: Espositore NON assegnato")

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.lista_stand, key=lambda x: x.prezzo)