# Quellen zu Sumanth Reddy Settipalli

## Lebenslauf

### Person
- Name: Sumanth Reddy Settipalli
- Rolle: Machine Learning Engineer · Maschinenbau und Simulation
- Ort: Reutlingen
- E-Mail: sumanthreddy.settipalli@gmail.com
- LinkedIn: linkedin.com/in/sumanthreddys (https://www.linkedin.com/in/sumanthreddys/)
- GitHub: github.com/Sumanthreddy-DE (https://github.com/Sumanthreddy-DE)
- Website: sumanthreddy.de (https://sumanthreddy.de)
- Verfügbarkeit: sofort verfügbar
- Status: Studium abgeschlossen (Master 08/2026), sucht eine Festanstellung; übt täglich 15 Minuten Deutsch im Gespräch mit einer KI
- Aktuell: Neben der Stellensuche freiberuflich: ein Buchungs-Bot, der seit 04/2026 jeden Morgen läuft, und ein KI-Telefonassistent für lokale Betriebe in Entwicklung; dazu Weiterentwicklung von SimReady
- Zielrollen (in dieser Reihenfolge): Machine Learning Engineer für Engineering · Simulationsingenieur · Maschinenbauingenieur (FEM, CAD)
- Stärkstes Projekt: SimReady, weil es Maschinenbau und KI in einem funktionierenden Werkzeug verbindet: STEP-Geometrie prüfen, für die Simulation heilen und die Befunde mit einem LLM-Agenten erklären; die Masterarbeit zu physikinformierten neuronalen Netzen (PINNs) zeigt dazu die wissenschaftliche Tiefe.
- Umzug: Umzugsbereit (deutschlandweit)

### Berufserfahrung

#### KI-Entwicklung und Automatisierung · Freiberuflich (04/2026 – heute, Reutlingen)
- Programmierung eines Buchungs-Bots in Python und Playwright, der die Küchenbuchungen eines Wohnhauses täglich über GitHub Actions per E-Mail an den Hausmeister sendet
- Entwicklung eines deutschsprachigen KI-Telefonassistenten für lokale Unternehmen und Auswahl von Spracherkennung (Deepgram) und Sprachausgabe (ElevenLabs) nach Antwortzeit und Sprachqualität

#### Wissenschaftliche Hilfskraft und Tutor · FAU Erlangen-Nürnberg (11/2023 – 08/2026, Erlangen)
Parallele Tätigkeiten an vier Lehrstühlen während des Masterstudiums

##### Lehrstuhl für Konstruktionstechnik (KTmfk) (04/2025 – 02/2026)
Werkzeuge: Python, Siemens NX, PTC Creo, NXOpen API, MATLAB Simscape/Simulink, TensorFlow, Transformers
- Entwicklung eines Werkzeugs in Python mit der NXOpen API zur automatischen Überführung von Baugruppen aus Siemens NX in XML-Dateien für MATLAB Simscape, in Kooperation mit Siemens
- Training eines Transformer-Modells in TensorFlow in Kooperation mit Siemens, das Zwangsbedingungen aus Siemens NX den passenden Gelenken in PTC Creo zuordnet und so die Übertragung von CAD-Baugruppen in die Simulation automatisiert
- Aufbau eines eigenen Trainingsdatensatzes ohne vorhandene Daten aus über 100 öffentlich verfügbaren CAD-Dateien im STEP-Format und Erweiterung der rund 1.000 Paare aus Zwangsbedingung und Gelenk durch Datenaugmentierung und synthetische Daten
- Extraktion technischer Parameter aus PDF-Dokumenten durch Named Entity Recognition mit BERT (Hugging Face Transformers) und einem in TensorFlow trainierten Klassifikator auf synthetischen Trainingsdaten aus ECLASS

##### Lehrstuhl für Technische Dynamik (Tutor) (09/2025 – 08/2026)
- Betreuung von Bachelorstudierenden in MATLAB-Übungen zu numerischen Methoden der Statik und Dynamik (FE-Analyse von Fachwerken, transiente Simulation von Kranschwingungen)

##### Lehrstuhl für Fertigungstechnologie (06/2024 – 12/2024)
Werkzeuge: Simufact Forming, FEM
- FEM-Simulation des Scherclinchens mehrlagiger Blechbauteile aus Aluminium und Stahl in Simufact Forming zur Analyse von Materialfluss, Verformung und Rissbildung

##### BRAINIACS-Gruppe, Lehrstuhl für Kontinuumsmechanik (11/2023 – 11/2024)
Werkzeuge: deal.II (C++), FEM, Python
- Identifikation der Materialparameter von Hydrogelen durch FE-Simulationen in deal.II (C++) mit nichtlinearen, viskoelastischen Materialmodellen und systematische Variation der Parameter bis zur Übereinstimmung mit dem gemessenen Relaxationsverhalten
- Durchführung von Druck- und Relaxationsversuchen an Hydrogelen sowie Auswertung der Messdaten in Python im Abgleich mit Daten von menschlichem Hirngewebe

#### ServiceNow-Entwicklung und Prozessautomatisierung · Tata Consultancy Services (08/2020 – 09/2022, Indien)
Werkzeuge: ServiceNow, JavaScript, REST API, Jira, SQL, Power BI
- Einführung einer ServiceNow-Plattform für einen international tätigen Kunden in acht Ländern mit Datenmigration aus Jira über REST-API-Integrationen, Abnahmetests (UAT) und Go-live
- Entwicklung kundenspezifischer Funktionen in JavaScript, sowohl serverseitige Logik als auch Anpassungen der Benutzeroberfläche
- Leitung der Entwicklung für einzelne Unternehmen des Kunden

### Ausbildung

#### Master Computational Engineering (Rechnergestütztes Ingenieurwesen) · Friedrich-Alexander-Universität Erlangen-Nürnberg (10/2022 – 08/2026, Erlangen)

#### Bachelor Maschinenbau · Amrita Vishwa Vidyapeetham (07/2016 – 06/2020, Indien)

### Projekte

#### PINN zur Parameteridentifikation in Verbundwerkstoffen (10/2025 – 02/2026, Masterarbeit)
Werkzeuge: PyTorch, Python, MATLAB, NumPy, SciPy, DeepONet, Surrogatmodelle
Code: https://github.com/Sumanthreddy-DE/PINN-for-composite-interface-identification
- Entwicklung eines physikinformierten neuronalen Netzes in PyTorch zur inversen Identifikation von Grenzflächenparametern in Verbundwerkstoffen aus effektiven Kompressions- und Schubmoduli
- Erprobung eines DeepONet als Vorwärts-Surrogat mit Optimierer für das inverse Problem, das bei extremen Steifigkeitsverhältnissen versagte, vor der Wahl des PINN
- Senkung des Vorhersagefehlers auf unter fünf Prozent durch Korrektur falsch annotierter Grenzfälle, adaptive Verlustgewichtung und Gradientenbegrenzung

#### SimReady: LLM-Agent für die FEA-Vorverarbeitung (03/2026 – heute, Projekt)
Werkzeuge: Python, PyTorch, PyTorch Geometric, pythonocc, CadQuery, Unsloth, Streamlit, Hugging Face, Linux
Code: https://github.com/Sumanthreddy-DE/simready
- Umsetzung eines dialogfähigen LLM-Agenten in Python und pythonOCC, der CAD-Dateien auf Simulationsfähigkeit prüft und einfache Bauteile erzeugt, sowie Vergleich offener Sprachmodelle bei der Erzeugung korrekter Bauteile
- Training eines Modells zur Erkennung von Geometriefehlern in CAD-Bauteilen und zur Vorhersage der Bereiche mit Bedarf an Netzverfeinerung und Erprobung der Fehlererkennung an realen Industriebauteilen
- Fine-Tuning eines Vision-Language-Modells (Qwen2.5-VL-3B) per QLoRA mit Unsloth und Hugging Face zur Erzeugung von CadQuery-Code aus Bauteilbildern und Bewertung nach Lauffähigkeit des Codes und Übereinstimmung mit dem Originalbauteil

#### Minimierung der Spitzenleistung unter harmonischen Lasten (09/2024, Projekt)
Werkzeuge: Python, FEM, PICOS, MOSEK
Code: https://github.com/Sumanthreddy-DE/Peak-Power-Minimization
- Neuimplementierung einer publizierten SDP-Methode zur Topologieoptimierung von Fachwerken in Python, Lösung mit dem MOSEK-Solver
- Bericht über die Fehler, die im veröffentlichten Originalcode zu falschen Ergebnissen führten

### Konferenzbeitrag

#### „A Study on the Effect of Cryotreatment on Copper based Brass Alloys“ · Vortrag als Erstautor, ICAMES 2020, PES College of Engineering (02/2020, Mandya, Indien)

### Kenntnisse
- Programmierung: Python, C++ (deal.II), MATLAB, SQL, FastAPI, REST API, Git, CMake, Docker, Linux, Bash, Claude Code, Playwright, GitHub Actions
- Machine Learning: PyTorch, PyTorch Geometric, TensorFlow, Hugging Face Transformers, scikit-learn, Pandas, NumPy, SciPy, Streamlit, Deep Learning, LLM-Agenten, Vision-Language-Modelle, PINN, DeepONet, Surrogatmodelle, Graph Neural Networks, LLM-Fine-Tuning, QLoRA, Unsloth, NER, RL-Umgebungen, LLM-Evaluation
- Simulation und FEM: Technische Mechanik, Festigkeitslehre, Werkstoffkunde, Finite-Elemente-Methode (FEM), CAE, Festigkeitsberechnung, Strukturanalyse, Kontinuumsmechanik, Strukturdynamik, Modalanalyse (freie Schwingung), Fügesimulation (Scherclinchen), Topologieoptimierung, Mehrkörpersimulation, ANSYS Workbench, Simufact Forming, MATLAB Simscape/Simulink, ParaView
- CAD und Automatisierung: Siemens NX, NXOpen API (Python), PTC Creo, SolidWorks, Autodesk Inventor, AutoCAD, STEP/pythonocc, CadQuery
- Werkstoffprüfung: Druck- und Relaxationsversuche, Tieftemperaturbehandlung, Auswertung von Versuchsdaten (Python)

### Sprachen
Deutsch – B2 (Zertifikat in Vorbereitung) · Englisch – C1 (fließend) · Hindi – fließend · Telugu – Muttersprache

### Engagement
- Mitgründer der Studierendenorganisation TEA an der FAU zur Begleitung internationaler Studierender beim Studienstart
- Leitung des Designteams bei der Go-Kart Design Competition 2019, Platz 11 von über 250 Teams

## Fallstudie PINN

Titel: Grenzflächenparameter in Verbundwerkstoffen per PINN bestimmen

Die wichtigste Entscheidung: die Homogenisierungsgleichungen direkt in die Verlustfunktion einzubauen, statt das Netz nur auf Daten zu trainieren. So prüft jeder Trainingsschritt, ob die vorhergesagten Parameter die Steifigkeiten wirklich ergeben.

In partikelverstärkten Verbundwerkstoffen entscheidet die dünne Übergangszone (Interphase) zwischen Partikel und Matrix über die Lastübertragung und die effektive Bauteilsteifigkeit. In Finite-Elemente-Rechnungen ist diese Schicht teuer, weil extrem kleine Schichtdicken sehr feine Netze und schlecht konditionierte Steifigkeitsmatrizen erzwingen. Ein Null-Dicken-Grenzflächenmodell (Extended General Interface Model, EGIM) ersetzt die Schicht durch vier effektive Parameter, die sich jedoch weder direkt messen noch analytisch invertieren lassen.

### Der Ansatz: Mikromechanik in der Verlustfunktion

Ich habe die analytischen Mori-Tanaka-Homogenisierungsgleichungen von MATLAB nach Python und PyTorch überführt (gegen die Referenzimplementierung bis auf Maschinengenauigkeit von 10⁻¹⁴ verifiziert) und direkt in die Verlustfunktion eines inversen PINN eingebettet. Eingang sind die effektiven Kompressions- und Schubmoduli eines dreischichtigen Interphasenmodells sowie die Phasenkennwerte; Ausgang sind die vier Grenzflächenparameter, die genau diese effektiven Moduli reproduzieren.

Physikalische Schranken sind direkt in der Ausgabeschicht verankert, damit das Netz ausschließlich zulässige Steifigkeiten und Grenzflächenpositionen vorhersagt. In jedem Trainingsschritt prüft das eingebettete Vorwärtsmodell, ob die vorhergesagten Parameter die Zielsteifigkeiten tatsächlich rekonstruieren.

### Was über die Genauigkeit im Training entschieden hat

Drei Eingriffe haben die Rekonstruktionsgenauigkeit maßgeblich verbessert: die Korrektur fehlerhaft annotierter Randfälle im Trainingsdatensatz, eine adaptive Verlustgewichtung nach dem ReLoBRaLo-Prinzip zwischen Daten- und Physikverlust sowie Gradientenbegrenzung gegen instabile Updates. Der erste Punkt war der größte Hebel, weil synthetische Platzhalterwerte an den Rändern des Parameterraums das Netz zuvor systematisch verzerrt hatten.

Abbildung: Konvergenz des inversen PINN über 500 Epochen. Physik- und Datenverlust laufen fast deckungsgleich, der Property-Verlust liegt vier Größenordnungen darunter; das beste Modell steht bei Epoche 323.

### Modellvergleich und Validierung im Parameterraum

Um die direkte Inversion sauber einzuordnen, habe ich zusätzlich ein Branch-Trunk-DeepONet als differenzierbares Vorwärts-Surrogat trainiert (0,21 % mittlerer Vorwärtsfehler für K_eff und 0,36 % für G_eff) und mit einem Multi-Start-L-BFGS-Inversionssolver sowie einer globalen Differential-Evolution-Optimierung verglichen. Während die iterative Inversion auf dem Surrogatmodell bei extremen Steifigkeitsverhältnissen in lokalen Minima hängenbleibt, liefert das direkte inverse PINN die Parameter in einem einzigen Vorwärtsschritt ohne Laufzeit-Optimierung.

Abbildung: Partikelverstärkter Fall, 500 zufällige Testkonfigurationen: K_eff wird genauer getroffen als G_eff (Medianfehler 1,4 % gegen 4,0 %). Die „33 von 36“ darunter stammen aus einer separaten, strukturierten Parameterstudie.

Rekonstruktionsfehler unter 5 % in 33 von 36 Konfigurationen der strukturierten Parameterstudie

Im strukturierten Sweep über Steifigkeitsverhältnis und Volumenanteil liegen 33 von 36 Konfigurationen unter der 5-%-Schwelle, außerhalb extrem weicher Partikel meist unter 2 %. Genau genug, um aufwendige FE-Detailmodelle der Interphase in Parameterstudien durch das schnelle Grenzflächenmodell zu ersetzen.

## Fallstudie SimReady

Titel: SimReady: KI-Copilot für FEA-Vorverarbeitung und CAD-Generierung

Die wichtigste Entscheidung: Das Sprachmodell schreibt keinen freien CAD-Code, sondern nur Befehle einer festen, typsicheren Sprache, die der eigene Geometrie-Checker sofort prüft.

Vor jeder Finite-Elemente-Rechnung steht die Vorverarbeitung: Geometrie prüfen, das CAD-Modell reparieren und entscheiden, wo das Netz feiner sein muss. Pro Bauteil kostet das erfahrene Berechnungsingenieure oft mehrere Stunden. Was dabei übersehen wird, führt später im Solver zu Abbrüchen oder ungenauen Spannungen.

### 1. Zwölf B-Rep-Geometrieprüfungen und automatische Heilung

SimReady liest eine STEP-Datei über pythonocc (OpenCascade) ein, repariert Topologiefehler über ShapeFix und führt zwölf Geometrieprüfungen aus. Geprüft werden unter anderem offene Schalen, Selbstüberschneidungen, Splitterflächen (Sliver Faces), sehr kurze Kanten, dünne Wände sowie kleine Bohrungen und Verrundungen. Das Ergebnis ist ein klarer Vernetzbarkeits-Score von 0 bis 100, eine geheilte STEP-Datei und eine farbliche Markierung direkt an den betroffenen Flächen des 3D-Modells.

Abbildung: Streamlit-Oberfläche von SimReady bei der Analyse eines Kastenprofils mit Bohrungen: Gesamtscore, B-Rep-Topologie, Befundliste und Flächenbewertung.

### 2. Graph Neural Network auf dem B-Rep-Flächengraphen (BRepSAGE)

Regeln allein betrachten jede Fläche isoliert. Ein Berechnungsingenieur bewertet eine Fläche aber immer zusammen mit ihren Nachbarflächen. Deshalb übersetzt SimReady die B-Rep-Topologie in einen Flächen-Nachbarschaftsgraphen mit zwölf geometrischen Merkmalen pro Fläche (Flächentyp, Größe, Normalenvektor, mittlere Krümmung und UV-Ausdehnung).

Darauf arbeitet BRepSAGE, ein zweischichtiges GraphSAGE-Netz mit drei Ausgabeköpfen: Es sagt für jede einzelne Fläche den Verfeinerungsbedarf und die lokale Komplexität voraus und klassifiziert gleichzeitig den Fehlertyp des gesamten Bauteils. Trainiert wurde das Modell auf 2.272 selbst generierten und gezielt degradierten CAD-Bauteilen, getrennt nach Ursprungsbauteil ohne Datenleckage zwischen Training und Validierung.

91 % F1-Score (92 % Precision, 90 % Recall) auf 3.612 Flächen · 88 von 100 valide CAD-Modelle aus Bildern

### 3. Multi-Turn-LLM-Agent, RAG und sichere Text-zu-CAD-Generierung

Über die Analyse-Pipeline legt SimReady einen Multi-Turn-LLM-Copiloten mit vier Werkzeugen: Geometrie analysieren, gezielte Reparaturen vorschlagen, FEA-Standards über eine Vektorsuche (RAG) nachschlagen und neue Bauteile generieren. Für die Generierung führt das System keinen freien LLM-Code aus, sondern nutzt eine typsichere Pydantic-DSL (Quader, Zylinder, Vereinigung, Abzug), die direkt in valide STEP-Dateien übersetzt und sofort durch den eigenen Geometrie-Checker geprüft wird (5 von 5 Prompts fehlerfrei auf gehosteten LLMs).

### 4. Vision-Language-Fine-Tuning (Bild zu CadQuery) und Qualitätsprüfung

Im zweiten Projektstrang bewertet SimReady KI-generierte CAD-Modelle. Dafür habe ich Qwen2.5-VL-3B per QLoRA auf dem GenCAD-Code-Datensatz feinabgestimmt, um aus einem 2D-Bauteilbild direkt ausführbaren CadQuery-Code zu erzeugen. Auf dem 100-Teile-Testset stieg die Rate lauffähiger CAD-Programme von 0 auf 88 von 100 (Volumen-IoU im Mittel 0,563, Median 0,580).

Entscheidend für die Praxis: Jedes generierte Bauteil läuft anschließend automatisch durch den SimReady-Checker. Dabei erkennt der Checker Selbstüberschneidungen, zu dünne Wände und ungültige Solids, die eine reine Voxel-IoU-Metrik komplett übersieht (zum Beispiel ein Bauteil mit sehr gutem IoU von 0,83, das sich selbst durchdringt). Aktuell baue ich diese Brücke zu einem 150-Prompt-Text-to-CAD-Benchmark für Konstruktionsregeln (ISO-Durchgangslöcher, NEMA-Flanschbilder, Mindestwandstärken) aus, um den Geometrie-Checker als direktes Reward-Signal im Reinforcement Learning (GRPO) zu nutzen.

## Fallstudie NX → Simscape

Titel: Von der NX-Baugruppe zum simulationsfähigen Simscape-Modell

Die wichtigste Entscheidung: die Zuordnung von Zwangsbedingungen zu Gelenken als Klassifikation zu lernen, statt sie von Hand mit Regeln abzubilden.

Am Lehrstuhl entstehen Mehrkörpersimulationen von Baugruppen. Die Geometrie kommt aus Siemens NX, gerechnet wird in MATLAB Simscape. Der Übergang zwischen beiden war Handarbeit: Bauteile, Zwangsbedingungen und Gelenke wurden manuell übertragen, langsam und fehleranfällig.

### Die Pipeline

Sie liest Geometrie und Zwangsbedingungen über die NXOpen API direkt aus der Baugruppe aus und erzeugt daraus simulationsfähiges XML für Simscape. Der Kern ist die Zuordnung: Jede NX-Zwangsbedingung braucht das passende Gelenk.

### Zuordnung als Klassifikationsproblem

Diese Zuordnung übernimmt ein Klassifikationsmodell auf 41 Constraint-Merkmalen je Bauteilpaar, validiert auf das passende Gelenk in PTC Creo. Den Trainingsdatensatz habe ich selbst aufgebaut: öffentliche STEP-Dateien geparst und daraus Paare aus Zwangsbedingung und Gelenk extrahiert. Validiert wurde gegen reale Modelle in PTC Creo.

### Die Pipeline prüft sich selbst

Zum Schluss vergleicht sie die Gelenkpositionen in NX und in Simscape. Weicht etwas ab, gibt es eine Warnung statt eines stillen Fehlers. Das ist der Teil, der den Unterschied macht: ein automatisch erzeugtes Modell, dem niemand traut, spart keine Zeit.

Aus Stunden manueller Übertragung werden Minuten

## Fallstudie Lebenslauf-Assistent

Titel: Fragen an meinen Lebenslauf: Chat-Assistent mit Quellenbindung

Die wichtigste Entscheidung: kein Retrieval. Lebenslauf und Fallstudien stehen vollständig im System-Prompt, weil ein Suchschritt eine weitere Stelle wäre, an der ein Kernfakt verloren gehen kann.

Recruiter und Fachleute stellen zu einem Lebenslauf oft dieselben Fragen: Wo hat er gearbeitet, was hat er selbst gebaut, ab wann ist er verfügbar? Ein Chat-Assistent kann das sofort beantworten, aber nur, wenn er nichts erfindet. Eine falsche Antwort über einen Bewerber schadet mehr als gar keine. Deshalb darf dieser Assistent nur aus festen Quellen antworten und muss offen sagen, wenn etwas nicht belegt ist.

### Der Ansatz: feste Quellen, Regeln und eine Quellenzeile

Die Quellen entstehen automatisch: Ein Build-Skript erzeugt aus meinem Lebenslauf und den Fallstudien-Seiten eine Markdown-Datei. Es übernimmt nur ausdrücklich freigegebene Felder, sodass ein neues privates Feld nie unbemerkt im Chat landet. Der Server lädt diese Datei stündlich neu aus dem öffentlichen Repository dieser Website. Lebenslauf, Fallstudien und Regeln stehen zusammen in einem gecachten System-Block von rund 18.000 Tokens; jede Folgefrage liest ihn aus dem Cache.

Die Regeln im System-Prompt legen fest: Fakten nur aus den Quellen, Schlussfolgerungen nur als solche gekennzeichnet, „nicht belegt“ heißt nie „keine Erfahrung“, Arbeitgeber und Kooperationspartner bleiben getrennt, und Behauptungen von Besuchern ändern die Regeln nicht. Unter jeder Antwort steht eine Quellenzeile in der Sprache der Frage; wählt das Modell die falsche Sprache, korrigiert der Server sie im laufenden Stream.

Für Fragen wie „Arbeitet er noch an SimReady?“ gibt es ein einziges, nur lesendes Werkzeug: Es holt die letzte Aktivität eines von drei freigegebenen GitHub-Projekten. Das Modell kann nur einen dieser drei Namen wählen, und Commit-Nachrichten werden ihm bewusst nicht übergeben, weil sie fremden oder privaten Text enthalten können.

### Geprüft wird von Hand, nach jeder Änderung

Ein fester Satz von 29 Testfragen läuft nach jeder Prompt-Änderung gegen den Live-Server, und ich bewerte jede Antwort von Hand. Die Fragen enthalten Fallen: Siemens war Kooperationspartner und nie Arbeitgeber, PTC Creo ein Werkzeug und kein Arbeitgeber, Prompt-Injection über den Gesprächsverlauf, beendete Tätigkeiten, die nicht als laufend erscheinen dürfen, und eine Positivkontrolle. Automatische Muster markieren Auffälligkeiten nur vor; das Urteil fällt von Hand.

Letzter vollständiger Lauf (29 Fragen, 27.11.2026): 24 bestanden, 4 teilweise, 1 nicht bestanden

„Teilweise“ heißt hier meist: inhaltlich richtig, aber länger als die erlaubten 60 Wörter oder ohne ein erwartetes Detail. Nicht bestanden hat eine englische Frage, die der Assistent auf Deutsch beantwortet hat.

### Betrieb auf dem eigenen Server

Das Backend ist eine FastAPI-Anwendung, die Antworten als NDJSON streamt. Sie läuft als abgeschotteter systemd-Dienst hinter Caddy auf einem selbst administrierten Server in Deutschland. Gegen Missbrauch und Kosten gibt es Grenzen pro Anfrage, höchstens zehn Fragen pro zehn Minuten und IP-Adresse, eine tägliche Obergrenze, einen eigenen API-Schlüssel mit Ausgabenlimit und einen Ausschalter. Fällt der Server aus oder greift eine Grenze, zeigt die Seite eine vorbereitete Antwort mit Hinweis, nie eine Fehlermeldung. Was gespeichert wird, steht im Datenschutz.

## Fallstudie text-to-cad-rl

Titel: text-to-cad-rl: RL-Umgebung für Text-zu-CAD

Die wichtigste Entscheidung: bewertet wird die gebaute 3D-Geometrie, nicht der Text der Antwort. Das Modell schreibt keinen ausführbaren Code, sondern ein JSON-CAD-Programm, und eine Prüfung in OpenCASCADE misst Maße und Features direkt am Volumenkörper.

Sprachmodelle sollen aus einer Beschreibung wie „Montageplatte für einen NEMA-17-Schrittmotor, 5 mm dick, mit Freiraum für den Zentrierbund und die vier M3-Schrauben“ ein korrektes CAD-Bauteil erzeugen. Um sie darin zu trainieren oder fair zu vergleichen, braucht es eine Belohnung, die nur ein wirklich richtiges Bauteil bekommt. Eine Umgebung, die sich mit einem fast richtigen Körper täuschen lässt, trainiert genau diese Täuschung.

### Der Aufbau: JSON-CAD-Programm, Prüfung im Subprozess

Die Umgebung baut auf verifiers v1 von Prime Intellect auf und ist auf dem Prime Intellect Environments Hub veröffentlicht. Das Modell antwortet in einem Schritt mit einem JSON-Programm in der CAD-Sprache aus meinem Projekt SimReady, die vier Operationen kennt: Quader, Zylinder, Vereinigen und Abziehen. Der B-Rep-Checker aus SimReady baut daraus den Körper in einem isolierten Subprozess, der sich bei Hängern beenden lässt, und prüft Maße und Features am 3D-Modell. Fehler im Checker selbst führen zu einem Ausführungsfehler statt zu einer falschen Null-Belohnung.

### Daten: getrennte Test- und Trainingsaufgaben

Der Testsatz besteht aus 111 festen Aufgaben: 37 mechanische Bauteile in drei Formulierungen, mit expliziten Maßen, im Stil eines Ingenieurs mit Normen und Passungen, und als Konstruktionsabsicht. Die Trainingsaufgaben (Platten mit Bohrungen, Buchsen, Flansche) erzeugt ein deterministischer Generator mit Durchgangsbohrungen nach ISO 273. Eine Prüfung über geometrische Signaturen stellt sicher, dass kein Trainingsbauteil einem Testbauteil gleicht: 6.000 von 6.000 erzeugten Aufgaben bestehen ihre eigenen Prüfungen, ohne eine einzige Überschneidung mit dem Testsatz. Als Kontrolle bestehen alle 111 Musterlösungen, und alle 111 unveränderten Leerantworten erhalten 0.

### Gegen Täuschung abgesichert

Ich habe versucht, die Bewertung selbst zu überlisten: Platte ohne Bohrungen, drei statt vier Bohrungen, Sacklöcher statt Durchgangsbohrungen, Bohrungen neben dem Bauteil, ein zweiter loser Körper, ein Vollstab statt einer Buchse und weitere. Alle 13 Täuschungsversuche fallen durch. Drei bekannte Lücken des Checkers sind dokumentiert und in Tests festgehalten, sodass jede Verbesserung in SimReady hier sofort sichtbar wird.

### Ergebnis: Normangaben sind die eigentliche Hürde

Vier offene Sprachmodelle liefen mit je fünf Durchläufen pro Aufgabe über den ganzen Testsatz, zusammen 2.220 Episoden. Die Erfolgsquote pro Versuch (pass@1) liegt zwischen 43,6 % und 91,5 %; zwei Frontier-Modelle erreichten auf denselben Aufgaben mit demselben Checker in SimReady 95,5 % und 96,2 %, wenn auch über einen Tool-Aufruf statt einer Textantwort. Die meisten Fehler sind Geometriefehler, also falsche Maße oder fehlende Features, keine Formatfehler. Eine Episode deckte zudem einen Fehler im SimReady-Checker auf, den ich gemeldet habe.

14 bis 49 Prozentpunkte weniger Erfolg bei Normangaben als bei expliziten Maßen, bei allen vier Modellen statistisch belegt

Bei expliziten Aufgaben steht jedes Maß im Text, für die Motorplatte also 42 × 42 × 5 mm, eine 22,5-mm-Mittelbohrung und vier 3,4-mm-Bohrungen im 31-mm-Quadrat. Bei Ingenieursaufgaben muss das Modell diese Zahlen selbst aus Normen und Passungen ableiten, aus „NEMA 17“ und „M3“. Bei allen vier Modellen schließt das gepaarte 95-%-Bootstrap-Intervall der Lücke die Null aus; bei den Frontier-Modellen ist die Lücke klein und nicht gesichert. Genau diesen Übersetzungsschritt belohnt die Umgebung. Ein Modell wurde mit ihr noch nicht trainiert: Gebaut, validiert und evaluiert ist die Umgebung, ein RL-Lauf steht noch aus.

## Fallstudie Telefonassistent

Titel: KI-Telefonassistent für lokale Betriebe: Latenz zuerst messen

Die wichtigste Entscheidung: erst messen, dann bauen. Bevor es ein Produkt gibt, laufen alle Kandidaten für Spracherkennung, Sprachmodell und Sprachausgabe gegen Grenzwerte, die vorher feststehen. So zeigt die Messung, an welcher Stufe es hängt, bevor ein Anbieter fest eingebaut ist.

Der Assistent soll Anrufe für lokale Betriebe auf Deutsch und Englisch annehmen, zuerst Tischreservierungen im Restaurant. Am Telefon zählt jede Pause: Bis die erste Silbe der Antwort zu hören ist, laufen Spracherkennung, die Antwort des Sprachmodells bis zum ersten Satz und der Start der Sprachausgabe nacheinander ab. Lange Pausen wirken am Telefon wie eine abgebrochene Verbindung. Das Projekt ist noch in Entwicklung, es gibt noch keinen Kunden.

### Runde 1: jede Stufe einzeln gegen feste Grenzwerte

Gemessen habe ich mit eigenen Testsätzen aus dem Restaurantalltag: 30 Sätze für die Spracherkennung, darunter Gerichte wie „Chicken Tikka Masala“ und Uhrzeiten wie „halb 8“, zehn Gesprächsschritte für das Sprachmodell, das über ein Werkzeug freie Tische sucht, und 15 Sätze für die Sprachausgabe, deren Stimmen ich blind bewertet habe. Die Grenzwerte standen vorher fest: Median bis zur ersten Audioausgabe höchstens 2,3 Sekunden bei einfachen Antworten und 3,5 Sekunden mit Werkzeugaufruf, keine kritischen Erkennungsfehler, mindestens 9 von 10 richtigen Gesprächsschritten, Stimmqualität im Mittel mindestens 4 von 5 und höchstens 15 Cent pro Gesprächsminute.

Schnellste Kombination: 1,28 Sekunden bis zur ersten Audioausgabe (Summe der Mediane je Stufe) bei rund 4 bis 5 US-Cent pro Minute

Trotzdem besteht keine Kombination jeden Grenzwert, und das Ergebnis sagt auch, woran es liegt. Die Spracherkennung macht in fünf von sechs Läufen trotz Keyword-Boosting aus „Butter Chicken“ ein „Buttered Chicken“, und im Streaming-Modus schneidet sie einen Satz einmal zu früh ab. Die Sprachmodelle verfehlen vor allem Datumsangaben, etwa einen Sonntag statt des nächsten Montags, oder überspringen die Tischsuche. Zwei Prüfungen waren selbst fehlerhaft („halb 8“ ist eine richtige Uhrzeit); ich habe sie korrigiert und dokumentiert, nicht passend gemacht.

### Was feststeht und was offen ist

Gewählt sind Deepgram im Streaming-Modus, mit der Erkennung ganzer Sätze als Rückfallebene, und eine Stimme von ElevenLabs; deren Bewertung von 3,93 stammt bisher von nur einer Person und bleibt vorläufig. Beim Sprachmodell liegen Claude Haiku 4.5 und das offene Modell gpt-oss-120b auf Groq innerhalb des Rauschens von zehn Gesprächsschritten: gpt-oss ist bei einfachen Antworten rund 750 Millisekunden schneller, macht aber mehr Datumsfehler. Beide laufen deshalb weiter, mit einem verbesserten Prompt.

### Runde 2: die ganze Pipeline mit Pipecat

Die zweite Runde setzt die Stufen mit dem Open-Source-Framework Pipecat zu einer Pipeline zusammen. Unterbricht der Anrufer die Antwort, stoppt die Ausgabe mit den Standardeinstellungen nach rund 390 bis 500 Millisekunden, mit einer schneller reagierenden Sprachaktivitätserkennung nach 257 bis 303 Millisekunden; im Gesprächsverlauf bleiben nur die Sätze, die der Anrufer vollständig gehört hat. Eine erste Sperrliste vor dem Sprachmodell zeigt, wo die Sicherheitsprüfung sitzt: Gesperrte Anfragen erreichen das Modell gar nicht erst. Geprüft habe ich auch Lizenz und Pflege des Frameworks und ob es eine Telefonanbindung für sipgate gibt: Die gibt es nicht direkt, mögliche Wege sind notiert. Offen sind die Ende-zu-Ende-Messung mit der echten Stimme und der Wechsel des Anbieters per Konfiguration.
