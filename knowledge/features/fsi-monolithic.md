# FSI monolithique : une interface couplée

Lecture ciblée de `master@ccf20caa0745cc2fe640f879d34acf2bf3855e6c`. Date de session : 19 septembre 2026 (New York).

## Où entrer

L’[exécutable monolithic_fsi.cpp](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/solvers/monolithic_fsi.cpp#L30-L44) construit **FSISolver**, puis appelle `run()` ou la boucle MMS. Attention au nom : cette fiche concerne `monolithic_fsi_solver.h/.cpp`. L’autre implémentation `fsi_solver.h/.cpp` devra être étudiée séparément.

FSISolver hérite de `NavierStokesSolver<dim, true>`. Son [système d’éléments finis](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/monolithic_fsi_solver.cpp#L31-L74) associe **vitesse u, pression p, position x et multiplicateur λ**. La position du maillage est donc une inconnue du système.

Le parcours hérité est visible dans la carte : [run() initialise puis conduit les sous-intervalles](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/navier_stokes_solver.cpp#L409-L415), [initialize() configure les assembleurs par appel virtuel](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/navier_stokes_solver.cpp#L135-L157), et [le sous-intervalle déclenche la résolution non linéaire](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/navier_stokes_solver.cpp#L344-L365). [GenericSolver délègue à Newton](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/generic_solver.cpp#L245-L250), qui [appelle assemble_matrix() sur le solveur FSI quand un réassemblage est requis](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/newton_solver.h#L107-L111).

## Ce qui compose le système

[`setup_assemblers()`](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/monolithic_fsi_solver.cpp#L207-L225) configure trois familles : Navier–Stokes avec `divergence_form | pseudo_solid`, multiplicateur de Lagrange sur maillage mobile, élasticité du pseudo-solide. Le constructeur vérifie une seule frontière de non-glissement faible et la compatibilité de son identifiant avec la frontière couplée. Il refuse la pression de moyenne nulle sur maillage mobile dans cette version.

## Le motif commun à CHNS

[`assemble_matrix()`](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/monolithic_fsi_solver.cpp#L2030-L2099) utilise le motif **WorkStream → ScratchData → assembleurs → CopyData → contraintes homogènes → matrice globale → compress(add)**. Ce motif est aussi présent dans CHNS. La ressemblance porte sur l’organisation du calcul ; elle ne prouve pas que les formulations physiques sont interchangeables.

Spécificité FSI : une étape de **couplage algébrique position–force** est appelée après la compression si `enable_coupling`. Son [entrée](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/monolithic_fsi_solver.cpp#L2179-L2226) récupère les lignes avant de modifier la matrice. Réordonner ces opérations pourrait modifier l’état d’assemblage requis par les itérateurs : c’est un contrat explicite dans le commentaire du code, pas un bug constaté.

## Force, couple et distribution

Le [header](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/monolithic_fsi_solver.h#L234-L254) définit les coefficients de force à partir de l’intégrale de −λ et les coefficients de couple intrinsèque par rapport au centre du corps. Le [contrôle de somme des poids de couple](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/monolithic_fsi_solver.cpp#L1309-L1335) effectue une réduction MPI puis vérifie une somme proche de zéro.

Les indicateurs `has_local_position_master`, `has_local_lambda_accumulator`, `has_cylinder_velocity_dofs` et `has_rotation_angle` expriment une intention de stockage local ; ils ne remplacent pas un test de propriété dans `locally_owned_dofs`. Dans cette révision, les deux derniers sont activés par la présence d’une face de frontière sur une cellule owned, puis servent à demander des DoFs inutilisés pour la vitesse ou l’angle ([calcul des indicateurs](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/monolithic_fsi_solver.cpp#L828-L897)). La [PR #93](https://github.com/arthurbawin/fez/pull/93) propose précisément de fonder ces deux décisions sur les DoFs de position possédés. Il faut distinguer intention de stockage, propriété effective et disponibilité comme fantôme avant de raisonner sur une lecture ou une écriture MPI. Aucun défaut n’a été reproduit ici.

## Risques de propagation à vérifier

- Modifier les composantes : vérifier extracteurs, masques et indices des termes couplés.
- Modifier ScratchData/CopyData : relire CHNS **et** FSI, les deux consomment ce motif.
- Modifier la distribution MPI : vérifier qui possède les DDL spéciaux, qui a leurs valeurs fantômes et qui écrit les lignes.
- Modifier forces/couples : relire l’origine physique de la pression et la convention de signe, ainsi que la stratégie de couplage.

Ces pistes sont des obligations de revue, pas des défauts démontrés. Aucun calcul FSI n’a été exécuté aujourd’hui. Lecture fine restante : variantes de couplage, rotation, différence entre les deux implémentations FSI, formulations des assembleurs de frontière et cas tests multi-rangs.
