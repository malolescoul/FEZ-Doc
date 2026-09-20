# Branches suivies — état du jour 1

Capture GitHub : 20 septembre 2026 à 03:16 UTC (19 septembre, soirée à New York). Dépôt : [arthurbawin/fez](https://github.com/arthurbawin/fez). Analyse statique, sans build FEZ.

## Références immuables

| Branche | Commit étudié | Dernier commit observé |
| --- | --- | --- |
| master | [ccf20caa0745cc2fe640f879d34acf2bf3855e6c](https://github.com/arthurbawin/fez/commit/ccf20caa0745cc2fe640f879d34acf2bf3855e6c) | 15 septembre : intégrales de champs, PR #91 |
| chns-ding-horriche-master-form | [35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858](https://github.com/arthurbawin/fez/commit/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858) | 18 septembre : couplage CHNS ALE et AMR arborescent |

La [comparaison des deux SHA](https://github.com/arthurbawin/fez/compare/ccf20caa0745cc2fe640f879d34acf2bf3855e6c...35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858) indique **62 commits d’avance, 0 de retard**, avec **182 fichiers** dans la liste de différences. La base commune est le SHA de master ci-dessus. La branche personnelle contient donc le master observé. Ces chiffres décrivent l’historique Git ; ils ne représentent pas 62 changements déjà étudiés en profondeur.

## Ce qui est connu sur chaque branche

### Master

- L’AMR Navier–Stokes/CHNS initial a été fusionné avec [#81](https://github.com/arthurbawin/fez/pull/81), commit aba07862f2252ac2808e9333ec805cd59123cfd6.
- Le posttraitement d’intégrales de champs a été fusionné avec [#91](https://github.com/arthurbawin/fez/pull/91), qui est le HEAD observé.
- Les correctifs FSI parallèle [#93](https://github.com/arthurbawin/fez/pull/93) et les forces multi-frontières [#92](https://github.com/arthurbawin/fez/pull/92) sont encore **ouverts**. Il ne faut pas attribuer automatiquement leur comportement à master.

### Branche personnelle

Le message du HEAD annonce : pré-solveur pseudo-solide avant l’AMR initial ; préservation de la géométrie ALE pendant le raffinement et le déraffinement ; sélection Kelly multi-champ ; bande physique d’interface ; transfert des historiques BDF et de la solution supplémentaire du pas adaptatif. Cette annonce est une entrée de lecture, pas une validation numérique. Les fiches techniques du jour confrontent ces mécanismes aux sources sélectionnées.

Les tests ajoutés visibles dans la comparaison comprennent amr_ale_transfer, amr_ale_indicator, amr_interface_band, amr_multifield, chns_presolver_amr et des cas CHNS ALE/enlarged. Leur présence ne prouve pas leur exécution ni leur réussite sur cette machine.

### Zone FSI commune vérifiée

Le contenu complet de src/monolithic_fsi_solver.cpp est identique aux deux SHA prioritaires. Les deux versions conservent la condition has_local_lambda_accumulator pour enregistrer les ghosts des accumulateurs ([master, ligne 1070](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/monolithic_fsi_solver.cpp#L1070), [prod, même ligne](https://github.com/arthurbawin/fez/blob/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858/src/monolithic_fsi_solver.cpp#L1070)). La PR #93 propose de la remplacer par has_local_position_master.

Le bloc du motif creux des DoF de vitesse du solide vérifie seulement !zero_mass_model à la [ligne 1933 de master](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/monolithic_fsi_solver.cpp#L1933) ; #93 ajoute has_cylinder_velocity_dofs. Il s’agit d’un signal déjà décrit par l’auteur de la PR, corroboré par lecture, et non d’un défaut reproduit ici.

## Reprendre à la prochaine session

1. Relire les HEADs distants et comparer avec les deux SHA ci-dessus.
2. Examiner le nouvel état de #92 et #93, y compris les nouvelles reviews.
3. Relire les fiches touchées par les fichiers modifiés avant de conserver leurs conclusions.
4. Sur le PC équipé : reproduire les scénarios MPI ciblés et mesurer l’intégrale du traceur immédiatement avant/après AMR.

Aucune automatisation, publication GitHub, modification de branche ou exécution FEZ n’a été effectuée.

