# Motif — presolver, cache et géométrie d'évaluation {#fez_pre_amr_presolver}

> Code lu à `cc8dace141900b82e5790fa878e39d9c54898784`, avant le nouveau couplage AMR. Constat statique ; aucun calcul ni test exécuté.

## Trois représentations, trois contrats

| Représentation | Identité des valeurs | Finalité |
|---|---|---|
| Solution du presolver | Champs FE `x`, éventuellement `psi`, sur son DoFHandler | Équilibre initial du pseudo-solide |
| Cache presolver | Coordonnées de support sur la référence + numéro de composante → valeur | Réutilisation du presolve avec une autre partition MPI compatible |
| État CHNS–ALE | Vecteur de champs où `x` pilote le mapping lié à `evaluation_point` | Évolution couplée sur la géométrie courante |

Le cache n'est pas une sérialisation de numéros DoF à réutiliser tels quels. Son entrée contient un tableau de coordonnées, une composante et une valeur. La clé textuelle utilise la composante et les coordonnées en précision 17 ; après lecture le solveur recherche les points possédés par **la partition actuelle**. C'est le mécanisme concret derrière « indépendant de la partition ». Il n'établit pas une compatibilité avec un autre maillage ou des points de support différents. [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/elasticity_solver.cpp#L66-L92), [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/elasticity_solver.cpp#L1033-L1071)

## Écrire avant de déplacer

Chaque rang parcourt ses DoFs possédés, associe la valeur aux points de support du mapping de référence et envoie ses entrées au rang 0. Celui-ci écrit l'empreinte et les entrées dans un fichier temporaire ; la barrière MPI et le remplacement des fichiers temporaires terminent l'écriture. Les rangs ne dépendent donc pas de la numérotation globale conservée entre deux lancements. [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/elasticity_solver.cpp#L926-L973)

Cet appel précède `postprocess_solution()`, qui peut déplacer les sommets de la triangulation pour visualiser le presolve. Enregistrer après ce déplacement changerait le repère des clés du cache. Même ordre pour l'export Gmsh : évaluer le champ déformé aux nœuds de référence, écrire, puis déplacer les sommets pour la visualisation. Le rôle de la référence est ici une donnée du format, pas seulement un choix graphique. [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/elasticity_solver.cpp#L320-L327), [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/elasticity_solver.cpp#L809-L855), [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/elasticity_solver.cpp#L1105-L1114)

## Valider avant de réutiliser

`try_load_presolved_mesh_cache()` remet le presolver à zéro, lit le maillage et recrée les DoFs. Chaque rang lit le cache et compare l'empreinte. Fichier absent, archive illisible, empreinte différente ou point de support possédé introuvable provoquent un retour `false`, pas une utilisation partielle du cache. Un `MPI::min` impose l'accord global ; la fabrique relance alors le presolve. [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/elasticity_solver.cpp#L977-L1031), [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/elasticity_solver.cpp#L1043-L1075), [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/presolver_tools.h#L26-L37)

L'empreinte comprend nom et hash FNV-1a du contenu du fichier maillage, degré de position, type quads, nombre de DoFs, modèle constitutif, expressions de Lamé, paramètre Ogden, sélection du forçage, épaisseur d'interface, compression physique, régularisation, présence/largeur/compression/exposant de `psi`, paramètres de continuation et expression analytique de `phi`. Le facteur de transport ne figure pas dans cette liste : le presolver n'assemble pas le transport. Le [patch du 30 juin](https://github.com/arthurbawin/fez/commit/a10d2366d98dd74562767ca92b14e617caf98795) ajoute explicitement les paramètres enlarged manquants et retire ce facteur de transport. [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/elasticity_solver.cpp#L46-L63), [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/elasticity_solver.cpp#L890-L922), [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/assembly/elasticity_assemblers.cpp#L326-L332)

**Limite de contrat, à vérifier selon le changement envisagé :** cette empreinte est une liste explicite, pas un hash du fichier de paramètres complet. Les expressions de BC et les sources utilisateur ne sont pas sérialisées dans cette fonction ; les expressions des fonctions sont enregistrées, sans inventaire explicite de toutes leurs constantes. On ne peut donc pas affirmer que tout changement qui influe sur le presolve invalide automatiquement le cache. C'est une inférence de la liste lue, pas un cas de réutilisation erronée exécuté. Pour étudier une modification hors de cette liste, `force_recompute` permet un résultat frais ; le graphe doit ensuite conduire vers l'empreinte pour décider s'il faut l'étendre. [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/elasticity_solver.cpp#L890-L922), [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/parameters.cpp#L1993-L2005)

Après une lecture réussie, le code compresse les insertions puis remplit `present_solution`, ses fantômes et `evaluation_point`. La fabrique rend le presolver sans appeler `run()`, donc sans refaire ses sorties finales. Une réutilisation du cache ne garantit pas la régénération d'un fichier msh de presolver demandé ailleurs : cette branche retourne directement l'objet chargé. [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/elasticity_solver.cpp#L1068-L1075), [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/presolver_tools.h#L32-L39)

## Injecter un état cohérent

Le transfert presolver → CHNS utilise une autre identité : composantes et points de support dans la cellule de référence. Il associe `x`, et `psi` s'il existe, puis parcourt les cellules actives source/destination dans le même ordre. Cette correspondance requiert des layouts et partitions compatibles. Le socle pré-AMR possède deux triangulations construites séparément ; le nouveau chemin AMR les partagera explicitement. [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/mesh_and_dof_tools.h#L52-L122), [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/navier_stokes_solver.cpp#L809-L842), [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/elasticity_solver.cpp#L96-L112)

Le lien causal est : `x` injecté → `evaluation_point` actualisé → `moving_mapping` modifié → interpolation de `u` et `phi` → contraintes physiques recalculées. En enlarged, le `psi` du presolver est aussi la valeur initiale de l'inconnue qui produit le forçage élargi. Repartir d'un `psi` nul modifierait ce forçage malgré la géométrie comprimée conservée ; le code et le [patch d'injection du 2 juillet](https://github.com/arthurbawin/fez/commit/7ae5094cf2a23005f89af4788bdf4d330ddeeab9) donnent cette motivation. [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/navier_stokes_solver.cpp#L758-L805), [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/navier_stokes_solver.cpp#L820-L842)

## Échos utiles pour la suite

- Une nouvelle composante peut nécessiter une modification du DoFHandler du presolver, de son masque, de la table de copie et de l'empreinte. Ce sont quatre lieux distincts à relire.
- Une nouvelle géométrie d'évaluation doit être restaurée avant ses consommateurs, comme lors de la [restauration après AMR](../../prod/html/fez_prod_distributed_state_transfer.html).
- Le cache géométrique n'est pas le restart : ce dernier charge triangulation, vecteurs courants/historiques et temps depuis des fichiers de rang, puis restaure séparément l'historique PVD.
- Les valeurs prises aux sondes de ligne utilisent les coordonnées physiques du mapping courant ; des clés de cache utilisent les points de référence. Réutiliser une de ces conventions dans l'autre mécanisme exige un choix explicite.

Ces rapprochements sont des inférences de conception fondées sur les chemins de données cités, sans revendiquer une équivalence des algorithmes. [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/elasticity_solver.cpp#L932-L948), [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/navier_stokes_solver.cpp#L1463-L1495), [Source pré-AMR](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/incompressible_chns_solver.cpp#L1575-L1594)



<span id="fez-guide-end-fez_pre_amr_presolver"></span>
