# Protocole de reprise manuelle de FEZ

> À appliquer lorsqu'une nouvelle session est lancée par l'utilisateur depuis son PC. Aucun déclenchement quotidien, tâche planifiée ni automatisme n'est nécessaire.

## 1. Reprendre la mémoire, puis vérifier son actualité

Lire d'abord [la carte](MAP.md), [l'état des branches](branches.md), le [dernier journal](journal/jour-1.md) et [state.json](../state.json). Le fichier d'état donne les commits capturés, les sources suivies et les travaux restants ; il ne remplace pas les fiches de compréhension.

Pour chaque branche prioritaire, distinguer :

- le dernier commit distant **observé** ;
- le dernier commit dont les changements ont été **analysés** ;
- le commit et la configuration réellement **testés**.

Ces valeurs peuvent différer. La découverte d'un nouveau HEAD ne met pas automatiquement à jour la compréhension du code.

Commencer par `master` et `chns-ding-horriche-master-form`. Examiner les autres branches seulement si un changement, une PR ou une dépendance l'exige.

## 2. Identifier le clone et les builds disponibles

Sur le PC équipé, repérer le dépôt FEZ et ses instructions locales avant de lancer des commandes de développement. Relever le remote, la branche active, le SHA exact et l'état des modifications locales. Préserver les travaux de l'utilisateur.

Repérer les répertoires de build existants et leur configuration : type Debug/Release, compilateur, versions deal.II/PETSc ou Trilinos, MPI, p4est, générateur CMake et options FEZ. Déterminer quels exécutables correspondent à quel commit. Un build présent sur disque ne prouve pas qu'il corresponde aux sources actuelles.

Les lectures et tests ciblés peuvent se poursuivre dans les installations existantes. Si une modification de code exige une autre branche, employer un checkout isolé plutôt que changer le contexte de travail actif de l'utilisateur.

## 3. Comparer les têtes avec l'état mémorisé

Lire les HEADs GitHub puis les comparer aux SHA conservés dans state.json. Si le clone local est utilisé, actualiser les références distantes sans modifier sa branche de travail.

- **HEAD inchangé :** exploiter la session pour approfondir une zone non lue ou produire une validation numérique.
- **Avance normale :** examiner les commits, fichiers et fonctions modifiés depuis la dernière révision analysée.
- **Historique réécrit ou divergence :** conserver les anciens SHA et reconstruire une comparaison explicite ; ne pas supposer un simple intervalle linéaire.
- **Code local non poussé :** le traiter comme une variante locale distincte, avec patch identifié ; ne pas attribuer ses résultats au HEAD GitHub.

Comparer aussi l'état des PR déjà suivies, leurs reviews et discussions finales. Au jour 1, #92 et #93 étaient ouvertes ; leur statut doit être relu, pas recopié. Une PR ouverte, fusionnée ou fermée sans fusion a des conséquences différentes pour les fiches.

Conserver une capture compacte des événements nouveaux : commit, push reflété par le changement de tête, PR, review, décision finale et liens. Une revue quotidienne manuelle n'observe pas nécessairement chaque événement intermédiaire d'un historique réécrit : signaler cette limite si elle compte.

## 4. Choisir les fiches à revalider

Pour chaque fichier modifié, utiliser [MAP.md](MAP.md) et les sources du graphe pour identifier les fonctions lues et leurs consommateurs. Les trois premières traversées transversales sont :

1. Forme locale → scratch → CopyData → contraintes → algèbre globale, en CHNS et FSI.
2. Maillage/DoFs → vecteurs et historiques → mappings → contraintes → posttraitement.
3. Transfert AMR → intégrale du traceur → interprétation de la conservation.

Marquer les conclusions dépendantes comme **à revalider** avant de les conserver. Distinguer changement mécanique, changement de contrat et changement de formulation. Pour chaque rapprochement nouveau, enregistrer les deux symboles, la révision, le contrat commun, les différences et les tests permettant de départager les interprétations.

Ne pas étendre une restriction d'une branche à l'autre par similitude de nom. Dans les graphes, distinguer appel, flux de données, héritage et utilisation. Une table de parcimonie représente des couplages autorisés, pas un graphe d'appels.

## 5. Vérifier avec le build disponible

Choisir des contrôles proportionnés au changement et enregistrer pour chacun : commande exacte, SHA/source locale, build, rangs MPI, paramètres, résultat, journaux et durée. Découvrir les commandes du projet et les noms CTest réels au lieu d'inventer une syntaxe de lancement.

En cas de simple progression de compréhension, cibler les invariants les plus utiles. En cas d'échec, isoler la cause avant de modifier le code. Une exécution terminée n'implique pas à elle seule une formulation correcte.

Les états de validation doivent rester distincts :

| Étiquette | Preuve minimale |
|---|---|
| Repéré | Chemin ou symbole trouvé |
| Lu | Source et rôle examinés sur un SHA |
| Confirmé statiquement | Appel, copie, contrat ou relation vérifiée dans les lignes citées |
| Hypothèse | Explication plausible, encore à confronter au code ou à une expérience |
| Exécuté | Commande et configuration conservées, résultat observé |
| Régression confirmée | Cas qui passe sur une référence appropriée et échoue sur la révision étudiée |
| Limitation explicite | Garde, assertion ou contrat du code indiquant le cas non pris en charge |

Les sorties `.output` versionnées sont des références de tests, pas un résultat de la session.

## 6. Conditions pour appeler quelque chose un bug

Un rapprochement suspect devient d'abord une question d'investigation. Avant de conclure, il faut au minimum :

- un **comportement attendu justifié** par le contrat, la formulation, un invariant ou un test existant ;
- un **comportement observé contradictoire**, avec source exacte et scénario atteignable ;
- une **configuration explicite** : branche/SHA, paramètres, géométrie, schéma temporel et contexte MPI pertinent ;
- une distinction entre erreur introduite, limitation annoncée, défaut déjà décrit en PR et choix d'approximation assumé ;
- idéalement un **reproducteur réduit**, ou, pour un défaut statique démontrable, une preuve du chemin et de la violation sans dépendre d'une supposition numérique.

Pour une régression, comparer avec une référence valide. Pour une divergence scientifique, documenter normes, conservation, ordre de convergence ou résidu attendu. Pour un problème MPI, identifier propriétaire, fantômes, écrivain et moment de synchronisation. Vérifier les PR existantes avant d'annoncer une découverte.

Ne pas qualifier de bug une perte de masse simplement parce qu'un transfert interpolatif n'est pas conservatif, une option explicitement refusée, ou une approximation géométrique documentée. Cela peut justifier une amélioration ou un contrat plus clair ; le diagnostic doit nommer le problème réel.

## Priorités de la prochaine session équipée

| Priorité | Travail borné | Résultat attendu |
|---|---|---|
| 1 | Capturer les nouveaux HEADs, l'état de #92/#93 et le clone/build local | État exact et fiches devenues obsolètes identifiées |
| 2 | Exécuter les tests disponibles `amr_ale_transfer`, `chns_presolver_amr`, `presolver_amr` sur 1 puis 4 rangs, selon la configuration du projet | Évidence sur géométrie, champs, BDF et état supplémentaire |
| 3 | Mesurer l'intégrale du traceur immédiatement avant/après raffinement et déraffinement, en séparant le pas physique | Bilan du transfert avec contexte et tolérances justifiées |
| 4 | Examiner/reproduire le scénario MPI FSI décrit par #93 sur un partitionnement pertinent | Signal connu confirmé, infirmé ou mieux délimité, sans attribution erronée à une nouvelle découverte |
| 5 | Approfondir une verticale Ding–Horriche : sélection → scratch → résidu → Jacobien → test | Une fiche de formulation et un graphe fin, sans prétendre auditer tous les modèles |
| 6 | Ajouter un exercice C++ tiré de cette verticale | Question courte, indice, correction et source exacte |

Les points 2 à 4 dépendent des exécutables et fixtures réellement disponibles. Si un test n'est pas accessible, documenter l'obstacle et poursuivre une lecture ou une expérience indépendante utile. La vérification d'une nouvelle modification urgente prime sur cette liste.

## Clore une session avec des livrables cohérents

Mettre à jour ensemble :

1. Les fiches Markdown, leurs sources, hypothèses et éléments à revalider.
2. Le graphe interactif : nœuds, relations, preuves et branche affichée.
3. Le journal : changements significatifs, découverte approfondie, résultats exécutés et questions ouvertes.
4. La documentation Doxygen locale, sans mélanger des symboles homonymes issus de snapshots de branches différents.
5. Les exercices pédagogiques liés au code réellement lu.
6. state.json : HEADs observés, révisions analysées/testées, couverture réelle et prochaine action.

Vérifier les liens relatifs et permalinks, la cohérence des extrémités du graphe, le rendu des pages modifiées et la génération documentaire. Ne jamais faire passer « fichier téléchargé » pour « fichier lu intégralement », ni « relation statique comprise » pour « calcul validé ».

La publication GitHub reste une étape distincte. Le résultat normal de cette session est un atlas consultable, une mémoire locale propre et une documentation prête à progresser ; aucune planification automatique n'est créée.

