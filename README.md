# FEZ — Atlas des couplages · Jour 1

Ouvrir **index.html** dans un navigateur récent. L’atlas, les textes, les extraits de code et les quiz fonctionnent hors ligne ; les liens GitHub nécessitent Internet. Conserver tout le dossier ensemble.

## Explorer

- Choisir master ou la branche personnelle dans la barre supérieure. La vue commence par les classes communes, puis les solveurs physiques.
- Molette : zoom au pointeur ; glisser le fond : déplacement ; glisser un nœud : réorganisation temporaire.
- Cliquer le titre d’un groupe : cadrer cette région.
- Cliquer un nœud : rôle, extrait, révision et dépendances sourcées. Cliquer une connexion : sa preuve.
- Double-cliquer un solveur ou son bouton « + » : déplier ses fonctionnalités plus bas dans le même canevas. Les classes parentes restent présentes. assemble_matrix() possède un niveau supplémentaire d’opérations documentées.
- « Déplier + » ouvre le prochain niveau disponible ; « Replier − » revient aux classes. Les boutons Socle / Solveurs / Features / Fonctions cadrent ces niveaux sans changer de page. Une fonction sans détail interne cartographié met en évidence son voisinage sourcé.
- Recherche : symboles des deux branches. Journal : bilan et PR. Lire : mémoire Markdown et accès Doxygen. Apprendre : quatre quiz corrigés et un exercice C++.
- Clavier : + / − pour zoomer, 0 pour recadrer, flèches pour naviguer, Échap pour fermer une fiche.

Les ports visualisent des **relations de code**, pas une signature exhaustive des arguments. Les lignes distinguent appels, données, héritage, utilisations et séquences. La disposition ne prétend pas reconstruire automatiquement tous les chemins d’exécution.

## Documents

- [Commencer la lecture](knowledge/START_HERE.md)
- [Carte du dépôt](knowledge/MAP.md)
- [Journal de la session](knowledge/journal/jour-1.md)
- [État des révisions](state.json)
- [Protocole de reprise](knowledge/SESSION_PROTOCOL.md)
- [Exercices C++](pedagogie/lecture-cpp-jour1.md)
- [Doxygen master](doxygen/master/html/index.html) et [Doxygen branche personnelle](doxygen/prod/html/index.html)
- [Périmètre et reproduction Doxygen](doxygen/README.md)

## Organisation du livrable

`knowledge/` conserve les faits, motifs, preuves et questions ouvertes. `data/atlas.json` contient les graphes et la provenance. `assets/` porte le rendu local et sa copie embarquée des données. `pedagogie/` contient les lectures. `doxygen/` contient les deux références générées, leurs configurations et les snapshots sélectionnés. `state.json` permet de comparer la prochaine capture à celle-ci.

L’apparence reprend le format de canevas approuvé, inspiré de blueprintUE : commentaires de groupes, petits nœuds, broches et câbles. Les accents de couleur et les courbes de phase du filigrane donnent une identité liée aux champs couplés de FEZ. Aucun asset graphique d’Unreal Engine n’est embarqué.

## Portée du premier jour

Sources GitHub figées, lecture ciblée, aucune compilation de FEZ. Les tests du site et la génération de Doxygen ne sont pas des tests numériques du solveur. La référence API est partielle. Aucun fichier n’a été publié ou envoyé sur GitHub ; aucune automatisation n’a été créée.
