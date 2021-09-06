# ML-python-TTT
Machine-Learning-Python-Tic-Tac-Toe

Dieses Repository stellt den Versuch dar, während des Mathecamps-2021 ohne Vorerfahrungen ein Multi-Layer-Perceptron zu implementieren ud mit der Fähigkeit Tic-Tac-Toe zu spielen zu trainieren.
Zudem enthält es den Code, der im Zirkel für die 7. Klasse (Künstliche Intelligenz) verwendet wurde.

Das verwenden von Bibliotheken war dabei verboten, wo bliebe denn sonst die Challenge.
Das Repository wird auch nach Ende des Camps noch weiter verwendet und geupdated.

Ich war/bin trotz längeren theoretischen Erfahrungen mit dem Thema, was die Praxis angeht ein kompletter Noob.
Daher stellt dieses Repository mehr meinen Lernprozess dar, als dass es eine perfekte Lösung vorgibt.

Von daher bin ich offen für Feedback, insbesondere, wenn jemand Fehler in meinem Spaghetti-Code findet.
Ich hab mir Mühe gegeben die Sacehn einigermaßen übersichtlich aufzuteilen, aber ich kann meist nur Nachts hier dran arbeiten und hab auch eigentlich nicht wirklich Zeit dafür.
Beides keine idealen Voraussetzungen für schönen Code, als habt Nachsicht (oder macht Pull-Requests und repariert mein Zeug).

# Verwendung

Für die Nutzung ist Python in der Version 3 notwendig. [Website](https://www.python.org/)

Die Grafische-Schnittstelle lässt sich mit "main.py" starten. Dort könnt ihr gegen den Computer spielen. 
In der "main.py" könnt ihr die jeweilige Strategie angeben, gegen die ihr spielen wollt (Zufällig, Minimax, Perceptron usw.)

Verschiedene Algorithmen könnt ihr in compare.py gegeneinander spielen lassen.
Auch dort könnt ihr die Gegner festlegen. 

ACHTUNG: der Minimax-Algorithmus ist in c implementiert, nicht in Python, weil Python viel zu langsam für Algorithmen ist.
Damit ich auf den C-Code zugreigfen kann, ist er als .dll Datei eingebunden. 
Diese funktionieren nur unter Windows. 
Auf Windows sollte alles einfach funktionieren, wenn ihr die notwendigen Python Pakete installiert habt (Bei Fehlermeldungen ist Google euer Freund).
Auf Linux müsste man die shared-Library nochmal mit anderen GCC-Parametern packen und dann entsprechend anders einbinden. 

Dafür hab ich grade keine Zeit, wenn jemand lust hat, gerne Pull-Request mit anleitung oder besserem Import.
