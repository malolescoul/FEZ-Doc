# Carte de FEZ — fonctions, features et dépendances

> Index transversal du jour 1. Lecture statique ciblée ; aucune exécution FEZ. Les liens de code sont figés au commit de leur branche. **Master** : `ccf20caa0745cc2fe640f879d34acf2bf3855e6c`. **Perso** : `35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858`. [État et comparaison des branches](branches.md).

## Entrées rapides

| Je veux comprendre… | Fiche | Point d'entrée précis |
|---|---|---|
| Le parcours de l'exécutable au calcul | [Cœur du solveur](features/core-solver.md) | master · [`main` CHNS](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/solvers/incompressible_chns.cpp#L6-L65) |
| La boucle temporelle et Newton | [Cœur du solveur](features/core-solver.md) | master · [`run_time_subinterval`](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/navier_stokes_solver.cpp#L260-L386) et [Newton](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/newton_solver.h#L57-L129) |
| Les champs u, p, φ, μ et le résidu | [Assemblage CHNS](features/chns-assembly.md) | master · [champs](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L24-L91) et [formes locales](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/assembly/incompressible_chns_assemblers.cpp#L54-L184) |
| La copie d'une contribution vers la matrice | [Motif local → global](patterns/local-global-assembly.md) | master · [`assemble_matrix` et copie](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L420-L501) |
| La FSI monolithique, les forces et le couple | [FSI monolithique](features/fsi-monolithic.md) | master · [`setup_assemblers`](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/monolithic_fsi_solver.cpp#L207-L225) et [couplage algébrique](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/monolithic_fsi_solver.cpp#L2179-L2226) |
| Le presolver avant CHNS–ALE | [CHNS–ALE et AMR](features/chns-ale-amr.md) | perso · [`CHNSSolver::initialize_solution`](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/incompressible_chns_solver.cpp#L91-L125) |
| Pourquoi la géométrie dépend d'un vecteur | [Transfert d'état distribué](patterns/distributed-state-transfer.md) | perso · [`setup_mappings`](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L521-L550) |
| Où raffiner autour d'une interface | [CHNS–ALE et AMR](features/chns-ale-amr.md) | perso · [indicateurs](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L1344-L1429) et [bande d'interface](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/mesh_adaptation_tools.cpp#L189-L325) |
| Comment combiner plusieurs critères | [CHNS–ALE et AMR](features/chns-ale-amr.md) | perso · [`mark_multifield_adaptation`](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/mesh_adaptation_tools.cpp#L28-L121) |
| Ce qui arrive aux champs et à leur passé après AMR | [Transfert distribué](patterns/distributed-state-transfer.md) | perso · [`adapt_mesh`](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L1433-L1517) et [interpolation](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/mesh_adaptation/transient_fixed_point.cpp#L558-L613) |
| Le contexte des PR et décisions de review | [Journal du jour 1](journal/jour-1.md) | [#81 AMR](https://github.com/arthurbawin/fez/pull/81), [#91 intégrales](https://github.com/arthurbawin/fez/pull/91), [#92 forces](https://github.com/arthurbawin/fez/pull/92), [#93 MPI FSI](https://github.com/arthurbawin/fez/pull/93) |

La FSI étudiée correspond à `monolithic_fsi_solver.h/.cpp`. L'autre implémentation `fsi_solver.h/.cpp` attend sa lecture fine. Une restriction lue sur master ne doit pas être appliquée automatiquement à la branche personnelle.

## Couches de responsabilités

| Couche | Objets repérés | Responsabilité |
|---|---|---|
| Configuration | exécutables, ParameterReader, ComponentOrdering | Choisir le solveur, les champs et les options |
| Orchestration | GenericSolver, NavierStokesSolver, CHNSSolver, FSISolver | Cycle temporel, Newton, points d'extension physiques |
| Géométrie et état | DoFHandler, mappings, vecteurs et historiques | Numérotation et état servant à évaluer les équations |
| Calcul local | ScratchData, assembleurs, CopyData | Valeurs aux points de quadrature et contributions locales |
| Algèbre distribuée | contraintes, objets LA, solveurs linéaires | Assemblage global et calcul de l'incrément |
| Adaptation | critères, TransientFixedPointData, SolutionTransfer | Modifier le maillage et transporter l'état |
| Observation | posttraitement, intégrales, tests | Confronter les calculs aux contrats attendus |

Cet index n'impose pas un sens unique de dépendance : l'ALE fait dépendre la géométrie de l'état que le solveur cherche.

## Écho 1 — CHNS et FSI partagent une organisation d'assemblage

**Preuve.** Les deux parcours utilisent WorkStream, ScratchData, CopyData, une copie contrainte vers le système global et `compress(add)`. [CHNS master](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L420-L501), [FSI master](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/monolithic_fsi_solver.cpp#L2030-L2099). Les alias de scratch combinent un socle commun de drapeaux, dont le pseudo-solide pour les variantes mobiles. [Alias](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/scratch_data.h#L130-L150)

**Différence.** La FSI ajoute un couplage algébrique après compression. La signification physique des variables reste propre à la formulation : une ressemblance de worker ou de tenseur ne suffit pas à partager une convention de pression. La review de [#92](https://github.com/arthurbawin/fez/pull/92#discussion_r4027016768) souligne précisément cette différence pour CHNS.

**En cas de changement, relire ensemble :**

- [Motif local → global](patterns/local-global-assembly.md), [assemblage CHNS](features/chns-assembly.md) et [FSI monolithique](features/fsi-monolithic.md).
- Filtres de propriété, remise à zéro du CopyData, indices DoF, masques et structure creuse.
- Contraintes homogènes de l'incrément, contraintes non homogènes de la solution et ordre de compression.
- Résidu et Jacobien pour tout changement de terme, puis contrôle par différences finies adapté aux choix de linéarisation.

Le lien organisationnel est établi pour les parcours lus ; les formulations physiques ne sont pas déclarées équivalentes.

## Écho 2 — le maillage relie état, contraintes et géométrie

**Preuve.** En ALE, MappingFEField utilise les positions de `evaluation_point`. Après AMR, le solveur restaure la géométrie avant les contraintes physiques. Les historiques reçoivent les contraintes de nœuds pendants, sans les valeurs de bord du temps courant. [Mapping](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L521-L550), [ordre ALE](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L1453-L1516), [historiques](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/mesh_adaptation/transient_fixed_point.cpp#L587-L613)

Le passage presolver → CHNS respecte le même ordre : position et éventuellement ψ d'abord, interpolation des champs ensuite. Ce passage remappe des composantes ; l'AMR interpole des états complets. Les opérations partagent un contrat géométrique sans être interchangeables. [Injection](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L787-L905)

La review de #81 identifie une autre conséquence : les postprocesseurs à DoF possèdent des objets liés au maillage et doivent être reconstruits. [Discussion](https://github.com/arthurbawin/fez/pull/81#discussion_r3919371805). Le chemin personnel réattache le maillage et recrée ces postprocesseurs pendant l'adaptation. [Code](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L1492-L1507)

**En cas de changement, relire ensemble :**

- [CHNS–ALE et AMR](features/chns-ale-amr.md), [transfert distribué](patterns/distributed-state-transfer.md) et initialisation des vecteurs dans le [cœur du solveur](features/core-solver.md).
- DoFs possédés/pertinents, courant, evaluation_point, historiques BDF et état supplémentaire du contrôleur.
- Mappings fixe/mobile, positions de bord, poids de pression, scratch et objets de posttraitement.
- Fixtures `amr_ale_transfer` et `chns_presolver_amr`, sur plusieurs rangs avec géométrie déformée.

La discussion MPI FSI [#93](https://github.com/arthurbawin/fez/pull/93) complète ce motif : posséder un DoF de position n'équivaut pas à posséder une face. Propriété, fantômes et responsabilité d'écriture doivent être tracés séparément.

## Écho 3 — le transfert AMR appelle un observateur de conservation

**Preuve historique.** Une question sur la conservation du traceur au déraffinement de #81 a motivé l'outil d'intégrales devenu #91. [Question](https://github.com/arthurbawin/fez/pull/81#discussion_r3935556906), [réponse](https://github.com/arthurbawin/fez/pull/81#discussion_r3936199510), [suite proposée](https://github.com/arthurbawin/fez/pull/81#discussion_r3936282798), [PR #91](https://github.com/arthurbawin/fez/pull/91).

**Preuve dans la branche personnelle.** La fixture du presolver vérifie la masse représentée au raffinement puis précise que le déraffinement interpolatif n'a pas à conserver exactement la masse. [Test](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/tests/unit_tests/chns_presolver_amr.cc#L118-L154). L'orchestrateur effectue le posttraitement avant l'AMR du pas : une table temporelle ordinaire ne remplace donc pas automatiquement une mesure juste avant/après transfert. [Ordre](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L415-L428)

**En cas de changement, relire ensemble :**

- Le [journal](journal/jour-1.md), le motif de [transfert](patterns/distributed-state-transfer.md) et la décision finale de #91.
- Le moment de calcul de l'intégrale, la géométrie et le champ intégrés, puis le moment d'écriture.
- Le contrat de review : calculer chaque pas et écrire selon `output_frequency`. [Décision](https://github.com/arthurbawin/fez/pull/91#discussion_r3940041730).
- Une mesure isolant transfert seul, pas de temps seul et calcul complet.

Calculer une intégrale observe la conservation ; cela ne rend pas le transfert conservatif. Un commentaire, une sortie de référence et une demande de review ne remplacent pas une mesure sur le build retenu.

## Hors carte fine aujourd'hui

- Audit mathématique complet Ding–Horriche/Abels, mobilité, Jacobiennes ALE/enlarged.
- Implémentation FSI distincte, détails des modes de couplage et de rotation.
- Communications internes des wrappers et effet mesuré du repartitionnement p4est.
- Coût du rassemblement MPI des segments d'interface.
- Couverture complète des options de compilation et des tests.

Le [protocole de session](SESSION_PROTOCOL.md) indique comment continuer. Les trois échos servent à choisir les lectures d'impact ; ils ne constituent pas des diagnostics de bugs.

