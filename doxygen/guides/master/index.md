# FEZ — référence master

**Jour 1 · source immuable : [ccf20caa0745cc2fe640f879d34acf2bf3855e6c](https://github.com/arthurbawin/fez/tree/ccf20caa0745cc2fe640f879d34acf2bf3855e6c).**

Cette référence est générée sur un **snapshot partiel** : le noyau du solveur, le parcours CHNS, l’assemblage et la FSI monolithique. Elle associe les commentaires du code à des guides de lecture rédigés après étude statique. Aucun build FEZ ni test numérique n’a été lancé.

## Commencer par un parcours

1. [Du programme CHNS à Newton](features/core-solver.md) : héritage, temps, résidu, incrément et contraintes.
2. [Assemblage CHNS](features/chns-assembly.md) : préparation des données, contributions locales, copie globale et Jacobien.
3. [FSI monolithique](features/fsi-monolithic.md) : inconnues de position, multiplicateurs, forces, couples et hypothèses MPI.

## Entrées dans l’API

- CHNSSolver : choix des champs et des assembleurs CHNS.
- NavierStokesSolver : cycle de simulation et structures partagées.
- GenericSolver : interface du solveur non linéaire.
- NewtonSolver : résolution non linéaire et recherche linéaire.
- FSISolver : uniquement l’implémentation monolithic_fsi_solver de ce snapshot.
- ScratchDataCHNS et CopyDataBase : lecture sur l’élément et résultat local.

Les noms présents deviennent des liens lorsque Doxygen les résout. Certaines classes externes et dépendances internes absentes du snapshot restent sans référence. L’index « Fichiers » donne accès au code source inclus.

## Lire les liens avec leur preuve

Un lien source vers GitHub pointe sur le commit analysé, donc conserve le contexte exact des observations. Les pages API extraites reflètent également des commentaires historiques du dépôt : elles ne garantissent pas qu’une précondition implicite ait été auditée. Les explications validées et les limites sont distinguées dans les guides.

Le contrat de l’assemblage reste essentiel : le second membre contient le négatif du résidu ; les contraintes homogènes s’appliquent à l’incrément. Le fait de rencontrer le même motif WorkStream dans CHNS et FSI n’autorise pas à transposer les formes physiques entre eux.

## Limites de cette édition

La formulation mathématique complète, les spécialisations des templates, la communication PETSc/deal.II et les scénarios MPI n’ont pas tous été audités. Doxygen ne compile ni ne teste ces sources. Les graphes d’appel automatiques ne sont pas générés ; ils seraient incomplets sans toutes les dépendances et ne remplaceraient pas l’analyse de flux de données.

La branche personnelle possède sa propre référence et son propre snapshot ; aucune signature provenant de cette branche n’a été mélangée à celle-ci.
