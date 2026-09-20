# CHNS–ALE et adaptation du maillage : première carte vérifiée {#fez_prod_chns_ale_amr}

> État : lecture statique ciblée, premier jour. Branche `chns-ding-horriche-master-form`, commit `35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858`. Comparaison ponctuelle avec `master` à `ccf20caa0745cc2fe640f879d34acf2bf3855e6c`. Aucun build ni test exécuté.

## Ce qu'il faut retenir

Le solveur CHNS mobile stocke la **position du maillage parmi les inconnues**. La géométrie utilisée pour intégrer les champs dépend donc du vecteur de solution. Une adaptation correcte doit transporter ensemble les champs physiques, les positions actuelles, les positions historiques BDF et, si nécessaire, la solution supplémentaire du contrôleur de pas de temps. L'ordre de restauration est déterminant : géométrie d'abord, conditions physiques ensuite.

Le commit de tête, daté du 18 septembre 2026, s'intitule **Couple CHNS ALE with tree-based AMR**. Son message annonce le couplage presolver/AMR, Kelly multichamp, la bande d'interface et le transport de l'historique. Les paragraphes ci-dessous distinguent les éléments effectivement retrouvés dans le code des vérifications restant à mener. [Commit](https://github.com/arthurbawin/fez/commit/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858)

## Points d'entrée et responsabilités

| Entrée | Responsabilité observée |
|---|---|
| [`solvers/incompressible_chns_ale.cpp`](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/solvers/incompressible_chns_ale.cpp#L32-L50) | Lit les paramètres et instancie `CHNSSolver<2,true>`. Le presolver externe n'est créé que hors AMR arborescent. |
| [`CHNSSolver::initialize_solution`](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/incompressible_chns_solver.cpp#L91-L125) | En ALE+AMR+presolver, crée le presolver sur la triangulation CHNS partagée, injecte les champs et reconstruit les contraintes. |
| [`NavierStokesSolver::run_time_subinterval`](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L265-L428) | Orchestre initialisation, préraffinement, pas de temps, adaptation et rotation de l'historique. |
| [`NavierStokesSolver::adapt_mesh`](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L1433-L1517) | Rétablit la géométrie, les contraintes et les structures algébriques après modification du maillage. |
| [`TransientFixedPointData`](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/mesh_adaptation/transient_fixed_point.cpp#L780-L924) | Marque le maillage, prépare le transport de tous les états, puis exécute raffinement/déraffinement. |

La variante enlarged est instanciée comme `CHNSSolver<2,true,true>` dans son exécutable. Le champ supplémentaire `psi` intervient dans le forçage du maillage et possède une équation de reconstruction ; ne pas l'assimiler à la phase physique `phi`. [Entrée enlarged](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/solvers/incompressible_chns_ale_enlarged.cpp#L32-L50), [couplages](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/incompressible_chns_solver.cpp#L819-L848)

## Parcours 1 — préparer un état CHNS sur la géométrie comprimée

1. Le solveur crée ses DoFs, mappings et contraintes.
2. En simulation transitoire, premier intervalle, sans restart, avec ALE+AMR+presolver, les stratégies **FixedNumber et InterfaceBand** déclenchent `initialize_solution()` **avant** les préraffinements. Cette condition est explicite : ne pas la généraliser à FixedFraction. [Condition](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L302-L316)
3. `create_elasticity_presolver(param, with_enlarged, triangulation)` crée un `ElasticitySolver` empruntant la triangulation de référence. Le mode cache doit être `off` et l'export final msh désactivé pour cette combinaison. [Fabrique](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/include/presolver_tools.h#L15-L42), [gardes CHNS](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/incompressible_chns_solver.cpp#L133-L143)
4. Le presolver applique une continuation du multiplicateur de compression lorsque le forçage utilise `chns_form`, puis résout le problème non linéaire. Il ne relit pas un nouveau maillage lorsqu'une triangulation est empruntée. [ElasticitySolver::run](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/elasticity_solver.cpp#L258-L308)
5. La position est injectée **avant** l'interpolation de vitesse et de traceur sur `moving_mapping`. Dans la variante enlarged, `psi` est aussi copié si les deux solveurs le possèdent. Le code exige la même triangulation pour le passage AMR. [Injection](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L787-L905), [traceur](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/incompressible_chns_solver.cpp#L758-L770)
6. Les contraintes de pression sont recréées sur la géométrie comprimée. Les historiques BDF sont initialisés avec cet état ; pendant le préraffinement, les champs initiaux sont réinterpolés en conservant la position transportée. [Initialisation CHNS](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/incompressible_chns_solver.cpp#L103-L121), [préraffinement](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L321-L342)

**Pourquoi cela compte :** réévaluer une condition initiale physique sur le maillage de référence à la place de la géométrie comprimée change le champ réellement imposé. Réinitialiser seulement les positions présentes, mais pas leur passé BDF, peut introduire une vitesse de maillage artificielle. Ces conséquences sont des inférences directes du rôle de l'état et des assertions des tests, pas des bugs constatés.

## Parcours 2 — décider où raffiner

### Kelly multichamp

`compute_error_estimate()` calcule un indicateur séparé pour chaque variable choisie. En ALE, il multiplie l'indicateur par `sqrt(h_def/h_ref)`, avec `h_def` obtenu entre sommets mappés ; le commentaire précise que cela n'est pas le diamètre exact d'une cellule courbe de haut ordre. [Indicateurs](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L1374-L1428), [diamètre](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/include/mesh_adaptation_tools.h#L18-L30)

`mark_multifield_adaptation()` sélectionne indépendamment chaque champ non nul, combine le raffinement par union et le déraffinement par intersection. Lorsqu'un budget limite l'union, les cellules demandées par davantage de champs passent en premier ; `CellId` tranche les égalités, sans comparer les unités physiques des indicateurs. Le commentaire indique que l'équilibrage peut ajouter des cellules au-delà de ce budget de demandes. [Sélection](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/mesh_adaptation_tools.cpp#L28-L121)

### Bande autour de l'interface

La stratégie utilise le zéro du traceur, une demi-largeur et un diamètre cible exprimés en multiples de `epsilon_interface`. Elle est explicitement limitée à **2D et aux quadrilatères**. Le contour est échantillonné puis approché par segments, rassemblés avec MPI ; les cellules sont comparées à ce contour dans la géométrie mappée. [Appel et limitation 2D](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L1344-L1367), [construction du contour](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/mesh_adaptation_tools.cpp#L189-L269)

Les critères valent +1 pour raffiner, 0 pour conserver et −1 pour demander un déraffinement. Les marges 1,1 sur la bande et 0,9 sur le diamètre limitent les oscillations ; le diamètre d'un parent ALE inactif est estimé à deux fois celui de l'enfant. Cela reste une approximation géométrique, explicitement codée. [Décision](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/mesh_adaptation_tools.cpp#L271-L325)

## Parcours 3 — transporter, puis reconstruire

`adapt_mesh()` récupère l'éventuel état supplémentaire du contrôleur temporel. La couche d'adaptation prépare `present_solution + previous_solutions + additional_solution` avec des vecteurs fantômes avant `execute_coarsening_and_refinement()`. Après redistribution des DoFs, elle interpole vers des vecteurs ne contenant que les DoFs possédés, applique les contraintes, puis recopie vers les états du solveur. Voir la fiche [transfert d'état distribué](../patterns/distributed-state-transfer.md).

Le point sensible est l'ordre ALE :

- transporter d'abord tous les états avec seulement les contraintes de nœuds pendants ;
- réimposer les positions de bord **courantes** ;
- rendre le `moving_mapping` cohérent via `evaluation_point` ;
- reconstruire pression, conditions physiques, parcimonie et solveur direct ;
- appliquer les contraintes physiques courantes à la solution courante.

Les historiques reçoivent seulement les contraintes de nœuds pendants, afin de ne pas remplacer leurs valeurs de bord passées par celles du temps présent. [Orchestration](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L1453-L1516), [interpolation des états](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/mesh_adaptation/transient_fixed_point.cpp#L558-L613)

## Assemblage : les premiers liens vérifiés

`CHNSSolver::setup_assemblers()` installe les assembleurs CHNS et ajoute les assembleurs d'élasticité lorsque le maillage est mobile. La fabrique CHNS sélectionne les drapeaux de spécialisation à la compilation pour ALE, enlarged, stabilisation et Ding–Horriche. Elle impose notamment que la variante enlarged soit ALE. [Composition](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/incompressible_chns_solver.cpp#L626-L641), [fabrique](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/include/assembly/incompressible_chns_assemblers.h#L369-L456)

La table de parcimonie indique des dépendances autorisées, **pas un graphe d'appels ni une preuve qu'un coefficient est toujours non nul** : positions couplées à `x,phi,u`, également à `psi` en enlarged ; ligne de `psi` couplée à `psi,phi,mu,x`. Modifier une formulation doit faire relire à la fois assembleur, scratch et table de couplage. [Table](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/incompressible_chns_solver.cpp#L795-L859)

La lecture complète des termes faibles, de leur Jacobienne et de leur cohérence mathématique est réservée à une prochaine session. Les passages de la grosse implémentation d'assemblage ont été repérés, pas audités intégralement.

## Différence avec master effectivement lue

| Sujet | master ccf20caa | Branche personnelle 35d43b8e |
|---|---|---|
| Variables Kelly | Assertion limitant à une seule variable | Indicateur indépendant par variable, combinaison des sélections |
| Après adaptation | Structures et contraintes reconstruites avant le transfert | Chemin ALE restaurant d'abord la géométrie puis les conditions physiques |
| État temporel supplémentaire | Transfert courant + historiques seulement | Ajout d'un pointeur optionnel vers l'état supplémentaire |

Sources master : [indicateur et adaptation](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/navier_stokes_solver.cpp#L1183-L1242), [transfert](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/mesh_adaptation/transient_fixed_point.cpp#L558-L603). Cette comparaison porte sur ces fonctions ; elle n'affirme pas que les deux branches ne diffèrent que sur ces trois points.

## Tests disponibles et statut

- [`amr_ale_transfer.cc`](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/tests/unit_tests/amr_ale_transfer.cc#L80-L148) : deux raffinements puis un déraffinement ; contrôle solution présente, `evaluation_point`, historiques et géométrie avec un état exactement représentable. La même fixture couvre standard/enlarged et la pression moyenne ; un cas séparé contrôle l'évaluation des valeurs de bord sur la nouvelle géométrie.
- [`chns_presolver_amr.cc`](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/tests/unit_tests/chns_presolver_amr.cc#L95-L154) : interpolation initiale sur géométrie mobile, historiques cohérents, raffinement/déraffinement et conservation de l'état supplémentaire. Le test précise que le déraffinement par interpolation n'a pas à conserver exactement la masse.
- L'arbre GitHub contient des références `.mpirun=1.output` et `.mpirun=4.output` pour ces deux tests, ainsi que `presolver_amr`, `amr_ale_indicator`, `amr_interface_band`, `amr_multifield` et des cas d'intégration standard/enlarged. Leur présence n'est **pas** une preuve d'exécution réussie au commit courant.
- AMR+restart est explicitement refusé à l'exécution dans ce parcours. [Garde](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L281-L286)

## Impacts à surveiller et suite de lecture

| Modification future | Relations à revalider |
|---|---|
| Ordre de `setup_mappings` / contraintes / transfert | Géométrie ALE, BC physiques, poids de pression moyenne |
| Nouveau champ ou changement de composants | `ComponentOrdering`, masques, injection presolver, assembleurs, transport de l'état complet |
| Nouveau contrôleur de pas de temps | Existence, taille et renouvellement de `additional_solution` |
| Autre stratégie de préraffinement | Condition `presolve_before_prerefinement` et conservation de la géométrie comprimée |
| Maillage très courbe ou interface complexe | Approximation entre sommets, échantillonnage du zéro, coût du rassemblement global des segments |

**Prochaine validation sur le PC de calcul :** exécuter les fixtures ciblées sur 1 et 4 rangs, relever les versions deal.II/PETSc/p4est et mesurer une situation où des cellules changent effectivement de propriétaire MPI. Aucun bug nouveau n'est affirmé à ce stade.

