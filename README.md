# FEZ — Atlas des couplages · Jour 1 + référence pré-AMR

Ouvrir **index.html** dans un navigateur récent. L’atlas, les textes, les extraits de code et les quiz fonctionnent hors ligne ; les liens GitHub nécessitent Internet. Conserver tout le dossier ensemble.

## Explorer

- Choisir master, la branche personnelle ou la référence historique avant AMR dans la barre supérieure. La vue commence par les classes communes, puis les solveurs physiques.
- Molette : zoom au pointeur ; glisser le fond : déplacement ; glisser un nœud : réorganisation temporaire.
- Cliquer le titre d’un groupe : cadrer cette région.
- Cliquer un nœud : rôle, extrait, révision et dépendances sourcées. Cliquer une connexion : sa preuve.
- Double-cliquer un solveur ou son bouton « + » : déplier ses fonctionnalités plus bas dans le même canevas. Les classes parentes restent présentes. Sur la référence avant AMR, CHNSSolver ouvre deux domaines (workflow et modèles), puis leurs fonctions au niveau suivant. assemble_matrix() possède un niveau supplémentaire d’opérations documentées.
- « Déplier + » ouvre le prochain niveau disponible ; « Replier − » revient aux classes. Les boutons Socle / Solveurs / Features / Fonctions cadrent ces niveaux sans changer de page. Une fonction sans détail interne cartographié met en évidence son voisinage sourcé.
- Recherche : symboles des trois révisions. Journal : bilan, PR et histoire de la branche (61 commits propres, 13 imports de master, filtres et preuves). Lire : mémoire Markdown et accès Doxygen. Apprendre : quatre quiz interactifs et les nouvelles lectures C++ corrigées.
- Clavier : + / − pour zoomer, 0 pour recadrer, flèches pour naviguer, Échap pour fermer une fiche.

Les ports visualisent des **relations de code**, pas une signature exhaustive des arguments. Les lignes distinguent appels, données, héritage, utilisations et séquences. La disposition ne prétend pas reconstruire automatiquement tous les chemins d’exécution.

## Documents

- [Commencer la lecture](knowledge/START_HERE.md)
- [Workflow avant le nouveau couplage AMR](knowledge/features/workflow-pre-amr.md)
- [Chronologie des ajouts et correctifs](knowledge/history/chronologie-branche.md)
- [Modèles, mobilité et corrections](knowledge/features/chns-models-pre-amr.md)
- [Bilan du complément historique](knowledge/journal/complement-pre-amr.md)
- [Carte du dépôt](knowledge/MAP.md)
- [Journal de la session](knowledge/journal/jour-1.md)
- [État des révisions](state.json)
- [Protocole de reprise](knowledge/SESSION_PROTOCOL.md)
- [Exercices C++](pedagogie/lecture-cpp-jour1.md)
- [Doxygen master](doxygen/master/html/index.html) et [Doxygen branche personnelle](doxygen/prod/html/index.html)
- [Doxygen avant AMR · cc8dace](doxygen/pre_amr/html/index.html)
- [Périmètre et reproduction Doxygen](doxygen/README.md)

## Organisation du livrable

`knowledge/` conserve les faits, motifs, preuves et questions ouvertes. `data/atlas.json` contient les graphes et la provenance. `assets/` porte le rendu local et sa copie embarquée des données. `pedagogie/` contient les lectures. `doxygen/` contient les trois références générées, leurs configurations et les snapshots sélectionnés. `state.json` permet de comparer la prochaine capture à celle-ci.

L’apparence reprend le format de canevas approuvé, inspiré de blueprintUE : commentaires de groupes, petits nœuds, broches et câbles. Les accents de couleur et les courbes de phase du filigrane donnent une identité liée aux champs couplés de FEZ. Aucun asset graphique d’Unreal Engine n’est embarqué.

## Portée du premier jour

Sources GitHub figées, lecture ciblée, aucune compilation de FEZ. Les tests du site et la génération de Doxygen ne sont pas des tests numériques du solveur. La référence API est partielle. Le premier rendu est déjà versionné en 332d857 dans FEZ-Doc ; ce complément constitue une nouvelle édition à versionner. Aucune automatisation n’a été créée. Voir [versionnement](VERSIONING.md).

Les équations du lecteur sont rendues localement avec KaTeX ; CSS, polices, licence et provenance sont embarqués. Aucun service externe n’est requis pour lire ces formules.
