# Parcours du solveur CHNS — master, jour 1

Révision : `ccf20caa0745cc2fe640f879d34acf2bf3855e6c`. Méthode : lecture statique de GitHub. Aucun build ni calcul FEZ exécuté. Les liens désignent cette révision, pas une branche mobile.

## Ce que cette fiche permet de retrouver

Le symbole C++ réel est **CHNSSolver**, défini dans `include/incompressible_chns_solver.h`. Il hérite de **NavierStokesSolver**, qui hérite de **`GenericSolver<LA::ParVectorType>`**. Le premier choisit les champs et les formes CHNS ; le deuxième organise une simulation Navier–Stokes et ses variantes ; le troisième fournit l'interface utilisée par Newton et les boucles de convergence/adaptation. [Héritage CHNS](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/incompressible_chns_solver.h#L16-L22), [héritage NS](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/navier_stokes_solver.h#L32-L73).

## Entrée → simulation → Newton

1. `solvers/incompressible_chns.cpp::main` initialise MPI avec un thread, lit le fichier de paramètres et choisit une instanciation 2D ou 3D. Il construit `CHNSSolver<dim>`, donc la variante au paramètre `with_moving_mesh=false` par défaut. Il choisit ensuite étude MMS, boucle de point fixe métrique, ou `run()`. [Entrée](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/solvers/incompressible_chns.cpp#L6-L65).
2. `NavierStokesSolver::run` appelle `reset`, `initialize`, puis `run_time_subinterval` pour chaque intervalle, et `finalize`. Le travail métrique final est conditionnel. `initialize` appelle la méthode virtuelle `setup_assemblers`, ici celle de CHNS. [Cycle](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/navier_stokes_solver.cpp#L409-L434), [initialisation](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/navier_stokes_solver.cpp#L135-L157).
3. Un sous-intervalle lit ou restaure le maillage, distribue les DoFs, crée mappings, scratch, contraintes et structure creuse. À chaque pas : avancer le temps, appliquer les conditions aux limites, résoudre ou utiliser la solution exacte, puis accepter/recommencer le pas. Les solutions BDF sont tournées après post-traitement et adaptation éventuelle. [Sous-intervalle](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/navier_stokes_solver.cpp#L260-L386).
4. `GenericSolver::solve_nonlinear_problem` délègue à l'objet Newton créé dans son constructeur. [Création](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/generic_solver.cpp#L29-L35), [délégation](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/generic_solver.cpp#L245-L257).
5. Newton évalue le second membre, en calcule la norme **L2**, vérifie la tolérance, décide de réassembler la matrice, puis résout le système linéaire. Il applique ensuite l'incrément, éventuellement avec recherche linéaire, et redistribue les contraintes non homogènes. [Itération](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/newton_solver.h#L57-L129), [mise à jour](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/newton_solver.h#L186-L212).

**Précision importante :** `assemble_rhs` représente le **négatif du résidu non linéaire**. Le contrat de `GenericSolver` l'explicite. On lit donc conceptuellement J(U) δU = −R(U), puis U ← U + α δU. [Contrat](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/generic_solver.h#L94-L118). La matrice n'est pas nécessairement recalculée à chaque itération : une heuristique dépend du régime stationnaire et de la réduction du résidu. [Heuristique](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/newton_solver.h#L215-L235).

## Les vecteurs : la distinction à retenir

`setup_dofs` initialise `present_solution`, `evaluation_point` et les solutions précédentes avec les ensembles owned **et relevant**. `local_evaluation_point`, `newton_update` et `system_rhs` sont initialisés avec owned seulement. Cette différence est visible dans les appels ; elle doit rester explicite dans toute analyse MPI. [Initialisation](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/navier_stokes_solver.cpp#L438-L475).

L'assemblage lit `evaluation_point`. La mise à jour s'effectue dans `local_evaluation_point`, puis ce dernier est affecté à `evaluation_point`. Il faut donc tracer **qui écrit, qui lit, et quand les données sont échangées**, sans déduire une communication précise seulement du nom d'un vecteur. Le détail des communications internes au wrapper deal.II/PETSc n'a pas été audité aujourd'hui.

## Résolution linéaire

`NavierStokesSolver::solve_linear_system` sélectionne MUMPS direct (avec ou sans objet réutilisable) ou GMRES. [Sélection](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/navier_stokes_solver.cpp#L857-L894).

Les fonctions de `src/linear_solver.cpp` résolvent dans `completely_distributed_solution`, construit sur les DoFs owned. Elles affectent ensuite `newton_update` et appliquent les **contraintes homogènes** à l'incrément. Le chemin GMRES sélectionne ILU sous PETSc et AMG dans l'autre branche de compilation. [Direct](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/linear_solver.cpp#L10-L50), [GMRES](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/linear_solver.cpp#L95-L150).

Les alias `LA::ParVectorType` et `LA::ParMatrixType` sont définis par `FEZ_WITH_PETSC` ou `FEZ_WITH_TRILINOS`. Cette lecture ne prouve pas que toutes les configurations de compilation fonctionnent. [Types](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/types.h#L8-L27).

## Impacts à suivre lors d'une modification

| Modification | Relire ensemble | Pourquoi |
|---|---|---|
| Ajout d'un champ | FESystem, ordering, extracteurs, masques, scratch, sparsité | Tous désignent la même organisation des composantes. |
| Changement du résidu | assemble_rhs, assemble_matrix, vérification différences finies | Préserver le signe et la cohérence du Jacobien. |
| Conditions aux limites | zero/nonzero constraints, incrément, mise à jour de U | L'incrément et la solution n'obéissent pas aux mêmes données imposées. |
| Redistribution du maillage ou des DoFs | setup_dofs, mappings, scratch, transfert des solutions | Les indices, espaces de lecture et historiques doivent rester compatibles. |
| Recherche linéaire/Newton | evaluation_point, present_solution, résidu, statut du pas | L'état utilisé pour accepter le pas doit correspondre à l'état évalué. |

## Limites et prochaine lecture

Le chemin CHNS fixe est établi. Les mécanismes internes de `TimeHandler`, transferts entre maillages, réutilisation MUMPS et conditions FSI restent à analyser. Les variantes ALE sont repérées mais non validées numériquement. Aucun défaut d'exécution n'est conclu à partir de cette seule lecture.

