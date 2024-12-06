# GUI_A2_SS23

pip3 install customtkinter

### Screens:
    - Loadingscreen
    - Login + Profil erstellen
    - Profil
    - Einstellungen
    - Hauptseite mit Tabelle und Filtern
    - Buchung einer Reise (extra Fenster)
        -> Auswahl der Kabinenart
        -> Zusammenfassung der Filter
    - Buchungsbestätigung

### Einstellungen
    - darkmode
    - smooth loading
    (- Sprache)

## Schiffsreise
### Attribute
    - Reisenummer
    Meeresart:
    - Ostsee
    - Nordsee
    - Mittelmeer
    - Nordpolarmeer
    - Nordpolarmeer mit Spezialflugtraining und Sonderbewachung
    Anzahl der Übernachtungen:
      - Bei N ausgewählten Überachtungen -> Anzeige von N-2 (min 0) bis N+2 Übernachtungen(Bsp. 3 Übernachtungen -> Anzeige von 1-5 Übernachtungen)
    Stadtbesuche:
      - Auswahl 0 bis allen verfügbaren Städte
    Schiffstyp:
      - A-I , X
### Zusatzanmerkungen:
    - selektiv nach Attributen filterbar
    - Wo ein Bild vorhanden ist , Bild anzeigen in einheitlicher Größe -> resize

## Nutzer:
### Kapital:
    - Startkapital 0€
    - Bei jeder Anmeldung -> 1000€ - 3000€ Kapital dazu (Zufallszahl)
    - Maximalkapital 20.000€
### Attribute:
    - Name
    - Nutzername
    - Passwort
    - Kontostand
### Zusatzanmerkungen:
    - Sichtbarer Name
    - Sichtbarer Kontostand

## Zusatzarbeit
    - Server + Update Data vom Server

### Weitere GUI-Funktionalitäten
    Die vom Nutzer vorausgewählten Reisen sollen ähnlich wie in der Excel-Datei in einer Art
    Liste erscheinen. Dabei soll die Reisenummer, Meerart, Anzahl Übernachtungen, etc.…der
    Reihe nach angezeigt werden. Falls mehrere Reisen auf die Nutzerauswahl zutreffen, sollen
    mehrere Reisen untereinander erscheinen. Falls alle Kabinenpreise einer Reise unetr dem
    Kontostand des Nutzers liegen, sollen diese nicht weiter anwählbar sein und ein Hinweis ind
    er GUI erscheinen, dass diese Reisen aufgrund von zu niedrigem Kontostand nicht weite
    rauswählbar sind. Der Nutzer soll sich dann für eine Reise (bei der er sich zumindest eine
    Kabinenart finanziell leisten kann) aus der Liste entscheiden können. Danach sollen die
    anderen Reisen aus der Liste verschwinden.

    Wenn der Nutzer sich für eine Reise entschieden hat, soll er auch hier bei einem Klick auf
    eine der 6 angezeigten Preiskategorien für die Kabinenarten ein Bild von der Kabine angezeigt
    bekommen. Da die ausgewählte Kabinenart den Kaufpreis der Reise bestimmt, soll der
    Nutzer eine Kabinenart für die ausgewiesene Reise mit einer Preiskategorie auswählen
    können. Dabei soll der Kontostand des Benutzers berücksichtigt werden: alle vorausgewählten
    Reisen (inklusive der zur Verfügung stehenden Kabinenpreise) sollen dem Benutzer zwar
    angezeigt werden, jedoch sollen die Reisen (inkl. Kabinenart), deren Preise über dem
    Kontostand des Benutzers liegen ausgegraut bzw. nicht weiter auswählbar sein. Dabei soll ein
    Hinweis in der GUI erscheinen, dass für diese Kabinenpreise der Kontostand des Nutzers nicht
    ausreicht.

    Nachdem die Kabinenart vom Nutzer festgelegt wurde (die er sich laut seinem Kontostand
    auch leisten kann), hat er sich für eine Reise entschieden. Dem Nutzer sollen dann alle
    besuchten Städte der Reise, der Schiffstyp und die Kabinenart gemeinsam mit dem zu
    zahlenden Endbetrag entweder in einem Bereich innerhalb der GUI oder in einem Extra-
    Fenster (z.B. mit dem Titel: „gekauftes Produkt“) angezeigt werden. Dabei sollen die Bilder
    übersichtlich angeordnet werden und die Aufteilung sich nach der Anzahl der anzuzeigenden
    Bilder orientieren. Diese finale Anzeige dient als bildbasierte Darstellung des gekauften
    Produkts durch den Nutzer.

    Beim GUI-Bereich bzw. im Extra-Fenster („gekauftes Produkt“) soll mit einem entsprechenden
    GUI-Steuerelement einstellbar sein, ob die besuchten Städte auf einmal erscheinen oder
    nacheinander einzeln angezeigt werden sollen. Wenn die besuchten Städte auf einmal
    erscheinen, dann sollen sie entsprechend ihrer Anzahl neben- bzw. untereinander
    übersichtlich angezeigt werden. Falls die besuchten Städte nacheinander erscheinen sollen,
    sollen sie einzeln angezeigt werden und mit entsprechenden GUI-Steuerelementen (z.B. mit
    Vorwärts- und Rückwärts-Buttons) durchiteriert werden können.

    Zum Schluss soll dem Nutzer ein Dialog angezeigt werden, in dem sein Name (Vor- und
    Zuname), die Reisenummer, die Kabinenart und der Reisepreis angezeigt wird. Der Nutzer soll
    in diesem Kaufdialog seine Adresse, Handynummer und seine Bankdaten eingeben können.
    Diese Daten sollen (quasi als Buchung für die ausgewählte Reise) in einer Textdatei
    abgespeichert werden. Nachdem die Reise vom Benutzer gekauft wurde, soll sein Kontostand
    um den Kaufbetrag erniedrigt werden, was in der entsprechenden Datei abgespeichert
    werden soll.
