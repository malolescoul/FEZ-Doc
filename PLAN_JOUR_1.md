# FEZ Atlas — plan de la première session

**Objectif :** livrer un atlas interactif local fondé sur une première lecture vérifiable de FEZ, des fiches Markdown durables, une documentation Doxygen locale et une leçon C++.

**Cadrage :** ../FEZ_ATLAS_CADRAGE.md. Le design et le démarrage ont été validés par l’utilisateur ; cette session utilise uniquement les sources GitHub. Aucune automatisation, aucun push et aucune compilation de FEZ.

**Architecture :** connaissances et provenance structurées, graphe indépendant de sa présentation, interface statique utilisable localement. Sources de référence figées par SHA. Génération de la documentation à partir des commentaires et des pages pédagogiques préparées localement.

## Étapes

- [x] Figer les deux branches et inventorier sources, tests, PR et reviews récentes.
- [x] Lire le cycle du solveur, l’assemblage et le rôle du système linéaire sur master.
- [x] Lire le parcours CHNS/ALE et le changement AMR de la branche personnelle ; isoler ses différences.
- [x] Produire des fiches de référence, deux mécanismes récurrents et un état de reprise.
- [x] Alimenter le canevas interactif avec des nœuds et relations sourcés ; ajouter choix de branche, zoom, détail et accès aux preuves.
- [x] Préparer la documentation Doxygen locale et la générer si l’outil est disponible, sans build FEZ.
- [x] Rédiger une leçon et des exercices C++ liés aux extraits effectivement étudiés.
- [x] Vérifier les liens internes, les références de lignes, les données du graphe et ses principales interactions ; livrer un dossier portable et une archive.

## Vérification et limites

- Chaque relation doit posséder sa provenance et son type ; ne pas transformer un graphe d’appels en ordre d’exécution démontré.
- Les deux branches gardent leurs SHA, leurs fiches et leurs différences. Une observation sur l’une n’est pas propagée à l’autre sans vérification.
- Des tests présents dans le dépôt ou une CI historique ne constituent pas une exécution locale dans cette session.
- Les zones non étudiées restent identifiées. Les pistes de recherche ne deviennent pas des bugs confirmés.
- Les fichiers de reprise permettent de continuer depuis un autre PC avec le dépôt et ses builds.
