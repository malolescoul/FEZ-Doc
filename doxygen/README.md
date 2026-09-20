# Référence Doxygen locale — FEZ, jour 1

Deux références sont préparées séparément pour éviter de confondre les variantes des classes selon la branche.

- **master** : ccf20caa0745cc2fe640f879d34acf2bf3855e6c.
- **chns-ding-horriche-master-form** : 35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858.

## Édition générée

Les deux références HTML et XML ont été **effectivement générées avec Doxygen 1.18.0**, avec un code de retour 0 pour chaque branche. L’archive portable officielle a été vérifiée avec le SHA-256 publié avant exécution. Aucun logiciel n’a été installé au niveau du système.

- [Ouvrir la référence master](master/html/index.html) : 25 fichiers source inclus.
- [Ouvrir la référence CHNS ALE](prod/html/index.html) : 28 fichiers source conservés, dont 26 dans l’index API et 2 tests conservés pour la reprise.
- [Manifeste des sources et contrôles](manifest.json) : SHA des commits, empreintes SHA-256 des fichiers et résultats de vérification.

Les avertissements restants concernent des commandes LaTeX présentes dans les commentaires du dépôt sans délimiteurs Doxygen : **24 pour master, 42 pour la branche personnelle**. Ils sont conservés dans logs/master-warnings.log et logs/prod-warnings.log. Les sources n’ont pas été retouchées pour les faire disparaître ; certaines formules des commentaires restent donc en notation textuelle imparfaite. Les guides de lecture rédigés pour cette édition restent séparés de ces commentaires hérités.

Une étape limitée au HTML généré rétablit les ancres des index alphabétiques et des destructeurs émises incomplètement par Doxygen 1.18.0. Le script fix-index-anchors.ps1 rend cette correction reproductible ; il ne modifie ni le texte de l’API ni le code FEZ.

Les snapshots contiennent uniquement les sources sélectionnées pour la lecture du jour 1. Cette documentation ne constitue donc pas encore la référence exhaustive de FEZ. Les symboles absents des snapshots, notamment certaines dépendances, ne disposent pas tous d’une fiche ou d’un lien résolu. Les commentaires existants et les signatures sont extraits ; leur présence dans une page ne signifie pas que tout leur comportement a été vérifié.

La génération utilise les sources C++ et les guides Markdown, sans compiler FEZ et sans Graphviz. Les diagrammes interactifs de l’atlas restent le support de navigation ; Doxygen fournit ici la référence d’API et la lecture du code source.

## Régénérer sur le PC FEZ

Depuis ce dossier, avec Doxygen 1.18.0 disponible :

```powershell
.\generate-docs.ps1 -DoxygenPath 'doxygen'
```

Le script appelle les deux Doxyfile puis normalise les ancres des index. Un chemin absolu vers un exécutable portable est également accepté. Le manifeste décrit la génération du jour 1 ; après enrichissement des sources, il faut renouveler l’inventaire et la vérification avant de le présenter comme actuel.

Les chemins d’entrée, de sortie et de suppression de préfixe sont relatifs à ce dossier. Le script synchronise les cinq guides depuis `../knowledge`, ajoute uniquement des identifiants de page stables, et nettoie les deux dossiers de sortie générés après validation de leurs chemins. Les fichiers HTML des guides se nomment ainsi `fez_master_core_solver.html`, `fez_master_chns_assembly.html`, `fez_master_fsi_monolithic.html`, `fez_prod_chns_ale_amr.html` et `fez_prod_distributed_state_transfer.html`, indépendamment du nom d’utilisateur ou du chemin de la machine.

Avec Python disponible, `python verify-docs.py` inventorie les fichiers, vérifie les liens locaux et les fragments, puis réécrit le manifeste. Les SHA et la version du générateur sont fixés dans ce script pour cette édition : les actualiser explicitement lors d’un changement de snapshot ou de Doxygen.

Les sorties attendues sont master/html/index.html et prod/html/index.html. Les logs et le manifeste de génération indiquent l’état réellement atteint, les avertissements et le nombre de fichiers inclus.

Les snapshots sont séparés par branche. Pour enrichir la référence, compléter chaque snapshot depuis son commit immuable, puis régénérer. Ne pas copier des headers de master dans le snapshot prod en supposant qu’ils sont identiques. Les fichiers de tests conservés dans un snapshot ne sont pas des tests exécutés lors de cette génération. Les points d’entrée main sont exclus de l’index des symboles pour éviter de fusionner les différents exécutables ; les fichiers source restent consultables.

## Sources de la méthode

- [Doxygen : démarrage](https://www.doxygen.nl/manual/starting.html).
- [Doxygen : configuration](https://www.doxygen.nl/manual/config.html).
- [Distribution officielle et SHA-256](https://www.doxygen.nl/download.html).

Cette génération n’a pas modifié le dépôt FEZ et n’y a créé aucun commit ou PR. Les livrables documentaires peuvent être versionnés séparément dans le dépôt privé FEZ-Doc.
