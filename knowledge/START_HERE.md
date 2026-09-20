# FEZ — reprendre la compréhension

Point d’entrée de la mémoire de travail. Session 01 : **19 septembre 2026, heure de New York** ; capture technique le 20 septembre UTC. Sources GitHub uniquement. Les fiches décrivent des lectures ciblées, jamais une couverture complète du dépôt.

## Lire dans cet ordre

1. [État machine des révisions](../state.json) : SHA observés, périmètre étudié, validations et suites.
2. [Carte du dépôt et des dépendances](MAP.md) : où trouver une feature et quoi relire avant de la modifier.
3. [Différence entre les deux branches](branches.md) puis [journal du jour](journal/jour-1.md).
4. La fiche de feature concernée et son motif transversal. Les liens de code incluent toujours un SHA et une plage de lignes.
5. [Protocole de la prochaine session](SESSION_PROTOCOL.md).

## Carte mentale de départ

**FEZ est un ensemble de solveurs éléments finis pour écoulements et interactions fluide–structure.** Notre premier périmètre est centré sur CHNS multiphasique, son extension ALE et l’adaptation de maillage, avec une entrée ciblée dans la FSI monolithique.

- [Socle solveur](features/core-solver.md) : GenericSolver et NavierStokesSolver organisent le calcul ; Newton rappelle les méthodes virtuelles du solveur spécialisé.
- [CHNS](features/chns-assembly.md) : champs de vitesse, pression, traceur de phase et potentiel chimique ; contributions locales de la formulation et de son Jacobien.
- [CHNS–ALE–AMR](features/chns-ale-amr.md) : le maillage déformé et les états temporels doivent survivre ensemble à l’adaptation et au changement de distribution.
- [FSI monolithique](features/fsi-monolithic.md) : vitesse, pression, position et multiplicateur de Lagrange ; couplage algébrique ajouté après assemblage.

## Les deux motifs à garder disponibles

[Assemblage local vers global](patterns/local-global-assembly.md) : ScratchData prépare les valeurs aux points de quadrature ; les assembleurs écrivent dans CopyData ; les contraintes distribuent vers le système global ; la compression finalise les contributions distribuées. Le motif se retrouve en CHNS et en FSI, avec des contenus physiques différents.

[Transport de l’état distribué](patterns/distributed-state-transfer.md) : une solution pertinente pour l’évaluation, un vecteur possédé localement pour l’écriture, l’historique BDF, les données du contrôle de pas et la géométrie n’ont pas tous le même rôle. Il faut suivre leur cycle de vie et les contraintes appliquées à chacun.

## Ce qui est établi aujourd’hui

- Le symbole réel est **CHNSSolver**, dans les fichiers incompressible_chns_solver.
- Le résidu non linéaire et la correction de Newton suivent des conventions précises ; ne pas déduire un signe ou une contrainte à partir du nom d’une variable.
- Dans la branche personnelle, l’AMR ALE transporte plusieurs états et reconstruit le mapping avant certaines contraintes physiques. L’ordre des opérations a une signification.
- Les PR #81 et #91 font le lien entre adaptation et suivi de conservation ; les reviews #92 rappellent que la signification de la pression dépend de la formulation. Voir leurs limites dans le journal.
- Les corrections proposées par #93 restent des changements ouverts à la capture. Elles ne doivent pas être décrites comme déjà présentes dans les branches étudiées.

Les références détaillées sont dans les fiches. Les assertions de ce résumé héritent de leur périmètre et de leurs SHA.

## Ce qui n’est pas encore établi

Aucun build FEZ, test MPI, test de convergence ou cas physique n’a été lancé. Les sorties de tests versionnées sont des données du dépôt, pas une reproduction indépendante. Aucun nouveau bug n’est confirmé.

Restent notamment à approfondir : dérivation complète des formulations CHNS et variantes enlarged, symétrie/signes du Jacobien, toutes les stratégies FSI et l’autre implémentation fsi_solver, adaptation métrique/MMG, redémarrage, garanties de conservation au transfert, performance et robustesse selon les rangs MPI.

## Conventions de confiance

**Lu / confirmé** : relation établie dans une source précise. **Inférence** : interprétation ou conséquence à vérifier. **Test présent** : cas repéré sans exécution. **Reproduit** : seulement après commande, configuration et résultat archivés. Une liaison absente de l’atlas ne démontre jamais l’absence de dépendance.

La page interactive et Doxygen sont des vues de cette connaissance. Les Markdown, les graphes JSON et l’état des révisions permettent de la reprendre et de la corriger sans dépendre de l’historique du chat.
