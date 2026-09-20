# FEZ — CHNS ALE et AMR

**Jour 1 · branche chns-ding-horriche-master-form · [35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858](https://github.com/arthurbawin/fez/tree/35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858).**

Cette référence porte sur un **snapshot partiel et distinct de master**. La lecture du jour privilégie le couplage entre géométrie ALE, pré-solveur, AMR et état temporel. Aucun build FEZ ni test numérique n’a été lancé.

## Parcours de lecture

1. [CHNS ALE, pré-solveur et AMR](features/chns-ale-amr.md) : ordre de construction de la géométrie, indicateurs et adaptation.
2. [Transfert d’un état distribué](patterns/distributed-state-transfer.md) : solution courante, historiques BDF, état supplémentaire et contraintes.

## Entrées dans l’API

- CHNSSolver : variantes avec maillage mobile et système enlarged.
- NavierStokesSolver : initialisation, adaptation, mappings et orchestrations communes.
- ElasticitySolver : pré-solveur de pseudo-solide.
- TimeHandler et BDFErrorEstimator : état temporel et estimation d’erreur pour l’adaptation du pas.
- ScratchDataCHNS : données préparées pour l’assemblage.
- Les fonctions d’adaptation sont accessibles dans mesh_adaptation_tools.h et son implémentation.

Les headers de base sont inclus au même SHA afin de rendre les signatures et l’héritage lisibles. Leur inclusion ne signifie pas que l’intégralité de leur implémentation a été auditée. Les dépendances absentes du snapshot restent susceptibles de produire des références non résolues.

## Le contrat qui relie ces parties

Une adaptation change à la fois le maillage, la numérotation et les objets qui en dépendent. Le chemin ALE relu restaure la position transportée avant de reconstruire les conditions physiques sur la géométrie actualisée. Les historiques ne doivent pas recevoir à tort les valeurs de bord du temps courant.

Les deux tests amr_ale_transfer.cc et chns_presolver_amr.cc sont conservés dans le snapshot pour la reprise sur le PC de calcul. Ils sont des sources lues, pas des tests exécutés aujourd’hui. Ils sont exclus de l’index API pour que les fixtures et fonctions main ne dominent pas les symboles du solveur.

## Ce qui reste à vérifier

Le déraffinement par interpolation ne garantit pas la conservation de masse. Les caractéristiques de l’indicateur d’interface, les approximations géométriques et la gestion des historiques sont documentées dans les guides, avec leurs limites explicites. La cohérence mathématique de tous les termes et Jacobiennes reste à étudier.

Cette édition n’inclut pas de graphes d’appels produits par Graphviz. Les liens Doxygen et le code source facilitent la lecture ; l’atlas interactif expose les parcours analysés séparément.
