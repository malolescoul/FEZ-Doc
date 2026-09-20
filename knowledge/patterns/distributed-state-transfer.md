# Motif — transporter un état distribué qui contient sa géométrie

> Branche personnelle ; commit `35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858`. Constat statique confirmé sur les fonctions citées. Les effets numériques et le comportement MPI doivent encore être exécutés sur un build local.

## Résumé pour reprendre rapidement

L'AMR ne transporte pas simplement « le vecteur solution ». Il transporte une **famille d'états à des dates différentes** vers un nouveau maillage distribué. En ALE, chaque état contient aussi une position de maillage. La topologie change, les DoFs changent, et les contraintes doivent retrouver une géométrie cohérente avant d'être évaluées.

La couche `LA::ParVectorType` est un alias compilé vers les vecteurs MPI PETSc ou Trilinos, selon les macros. Il faut donc distinguer le contrat FEZ de l'implémentation du backend. [types.h](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/include/types.h#L8-L25)

## Les objets et leurs contrats

| Objet | Rôle dans le transport |
|---|---|
| `present_solution` | État courant, position ALE comprise |
| `previous_solutions` | États aux dates BDF antérieures, donc positions antérieures comprises |
| `additional_solution` | État historique supplémentaire, exposé par le contrôleur temporel si disponible |
| `evaluation_point` | Vecteur auquel `MappingFEField` est lié ; les positions qu'il contient déterminent la géométrie courante |
| `SolutionTransfer` | Prépare l'interpolation avant le changement de topologie, puis l'effectue après recréation des DoFs |
| `locally_owned_dofs` / `locally_relevant_dofs` | Partition détenue par le rang et DoFs requis localement, y compris les fantômes |

La liaison géométrique est explicite : `MappingFEField(*dof_handler, evaluation_point, position_mask)`. Il ne suffit donc pas qu'un autre vecteur contienne les bonnes positions. [setup_mappings](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L521-L550)

## Séquence observée

1. `NavierStokesSolver::adapt_mesh()` obtient `time_handler.get_additional_solution()`. Le résultat peut être nul si aucun estimateur n'existe ou si son vecteur n'est pas encore initialisé. [Appel](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L1433-L1443), [getter](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/time_handler.cpp#L279-L284)
2. `TransientFixedPointData::adapt_mesh_with_dealii_routines()` construit la liste `all_in` : courant, historiques, puis supplémentaire. Il vérifie la taille et la présence de fantômes. Les champs physiques et positions voyagent dans les mêmes vecteurs. [Préparation](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/mesh_adaptation/transient_fixed_point.cpp#L900-L918)
3. Le code appelle successivement `prepare_coarsening_and_refinement()`, `solution_transfer->prepare_for_coarsening_and_refinement(all_in)`, puis `execute_coarsening_and_refinement()`. Ce chemin est conditionné par `DEAL_II_WITH_P4EST`. [Modification topologique](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/mesh_adaptation/transient_fixed_point.cpp#L920-L934)
4. Le solveur réexécute `setup_dofs()` et `setup_mappings()`. Le transport interpole vers des vecteurs ne contenant que les DoFs possédés. [Recréation](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L1448-L1451), [sorties possédées](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/mesh_adaptation/transient_fixed_point.cpp#L565-L581)
5. Le transfert distribue les contraintes reçues sur le courant, mais seulement les contraintes de nœuds pendants sur les historiques et le supplémentaire. Le supplémentaire est réinitialisé avec les nouveaux ensembles possédés/pertinents avant copie. [Restauration](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/mesh_adaptation/transient_fixed_point.cpp#L583-L613)
6. En ALE, l'appelant transmet d'abord uniquement des contraintes de nœuds pendants. Il réimpose ensuite les positions courantes de bord, recopie vers `evaluation_point`, reconstruit les contraintes physiques et les structures algébriques, puis contraint le courant. [Ordre ALE complet](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L1453-L1516)

Il n'y a pas d'appel explicite à `repartition()` dans ces passages : la mutation distribuée est confiée à `execute_coarsening_and_refinement()`. Le message du commit mentionne p4est et le repartitionnement ; une preuve dynamique d'un changement effectif de propriétaire des cellules reste à produire.

## Trois invariants à conserver

### 1. Même index, même sens, même instant

Les états de `all_in` et `all_out` doivent conserver le même ordre. Une nouvelle catégorie d'état nécessite de modifier préparation et restauration ensemble. Les positions historiques ne doivent pas recevoir les valeurs de bord imposées au temps courant. Le commentaire du transport rappelle explicitement cette différence. [Ordre des états](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/mesh_adaptation/transient_fixed_point.cpp#L906-L912), [temps des contraintes](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/mesh_adaptation/transient_fixed_point.cpp#L587-L604)

### 2. Géométrie reconstruite avant ses consommateurs

Les conditions physiques, points de quadrature et poids de pression dépendent de la géométrie. Restaurer seulement `present_solution` sans mettre à jour `evaluation_point` ne respecte pas la liaison observée de `MappingFEField`. Le test de bord évalue la vitesse imposée contre les points de quadrature du mapping mobile. [Test de géométrie de bord](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/tests/unit_tests/amr_ale_transfer.cc#L40-L76)

### 3. État temporel au-delà du BDF nominal

`TimeHandler::rotate_solutions()` copie d'abord le dernier historique vers l'estimateur de pas de temps, puis décale l'historique BDF. Ce vecteur supplémentaire fait donc partie de la mémoire du calcul et doit suivre l'AMR. [Rotation](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/time_handler.cpp#L262-L275), [stockage supplémentaire](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/timestep_adaptation.cpp#L49-L59)

## Échos déjà identifiés

- **Injection presolver → CHNS** : autre changement de représentation d'état. `extract_subsolution` remappe les composants de position et éventuellement `psi`, puis compresse les insertions et met à jour `evaluation_point`. Même exigence de cohérence géométrique, mais ce n'est pas le même algorithme que le transport AMR. [Injection](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L865-L905)
- **Initialisation des champs physiques** : la position est évaluée en premier ; vitesse et `phi` sont ensuite interpolés sur le mapping mobile. Même dépendance géométrie → évaluation physique. [Initialisation](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L792-L856)
- **Préraffinement du calcul comprimé** : les champs initiaux peuvent être reconstruits tout en préservant la position déjà transportée. Même vecteur, mais certaines composantes sont conservées tandis que d'autres sont réinterpolées. [Branche preserve_mesh_position](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L803-L846), [appel](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/navier_stokes_solver.cpp#L328-L342)

Ces rapprochements sont confirmés par les appels et copies lus. Ils ne signifient pas que les opérations soient interchangeables.

## Ce qui pourrait casser si le motif évolue

| Changement | Conséquence à examiner, encore hypothétique |
|---|---|
| Ajout d'un champ stocké en dehors du vecteur principal | Il peut rester sur l'ancien maillage si aucun transfert dédié ne l'inclut |
| Réduction de l'historique transporté | Incohérence du schéma ou de l'estimateur temporel après adaptation |
| Application des BC courantes à tous les historiques | Altération de la dépendance temporelle des positions et des champs |
| Mise à jour tardive de `evaluation_point` | Conditions physiques calculées sur la mauvaise géométrie |
| Changement de backend PETSc/Trilinos | Revalider copie, fantômes, compression et réinitialisation sous ce backend |
| Remplacement de l'interpolation par une projection conservative | Revoir exactitude polynomiale, contraintes et comportement de masse au déraffinement |

Aucune de ces lignes n'est un bug diagnostiqué. Elles donnent les chemins à suivre lors d'une future modification.

## Preuves testables déjà dans le dépôt

Le test [amr_ale_transfer](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/tests/unit_tests/amr_ale_transfer.cc#L80-L148) vérifie deux raffinements puis un déraffinement d'états représentables, les historiques aux dates distinctes, les positions mappées et `evaluation_point`. Son `main` couvre les variantes standard/enlarged, avec et sans pression moyenne. [Configurations](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/tests/unit_tests/amr_ale_transfer.cc#L218-L244)

Le test [chns_presolver_amr](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/tests/unit_tests/chns_presolver_amr.cc#L118-L154) vérifie l'état initial comprimé après adaptation et contrôle explicitement `additional_solution`. Il exige la conservation de la masse représentée au raffinement de sa fixture, mais seulement une masse finie et bornée au déraffinement : aucune garantie générale de conservation exacte de masse ne découle de ce test.

À exécuter ensuite : ces fixtures sur 1 et 4 rangs, instrumentation du propriétaire des cellules avant/après et contrôle du transfert avec pas de temps adaptatif effectivement utilisé. Aujourd'hui : sources lues, exécution non effectuée.

## Exercice C++ de lecture

Dans la signature suivante, pourquoi le dernier paramètre est-il un pointeur initialisable à `nullptr`, alors que les contraintes sont passées par référence constante ?

```cpp
void transfer_solution_between_refinements(
  const IndexSet &locally_relevant_dofs,
  const AffineConstraints<double> &nonzero_constraints,
  LA::ParVectorType *additional_solution);
```

**Réponse :** l'état supplémentaire est optionnel et mutable : le code teste sa présence puis le réinitialise et le remplit. Les deux références désignent des objets obligatoires, consultés sans modifier leur interface. Un pointeur ne signifie pas ici un transfert de propriété : le propriétaire de l'état reste l'estimateur temporel. [Implémentation](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/mesh_adaptation/transient_fixed_point.cpp#L558-L613), [accès à l'état](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/time_handler.cpp#L279-L284)

