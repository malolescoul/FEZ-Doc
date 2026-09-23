# FEZ — workflow de référence avant le couplage CHNS–ALE AMR

Révision figée : [cc8dace141900b82e5790fa878e39d9c54898784](https://github.com/arthurbawin/fez/tree/cc8dace141900b82e5790fa878e39d9c54898784), 16 septembre 2026. Elle précède le nouveau couplage AMR de la branche personnelle, mais contient déjà des infrastructures AMR importées de master.

Cette référence partielle isole le socle de travail antérieur : presolver élastique, géométrie ALE, système enlarged avec ψ, formulations et mobilités, reprises et diagnostics. Les fichiers sont issus de cette révision précise ; aucune compilation FEZ n'a été effectuée.

## Parcours conseillé

1. [Du lancement au redémarrage](features/workflow-pre-amr.md).
2. [Modèles CHNS et variantes enlarged](features/chns-models-pre-amr.md).
3. [Presolver, cache et géométrie](patterns/presolver-cache-geometry.md).
4. [Mobilité, corrections et contrôle du pas](patterns/mobility-corrections-timestep.md).

## Repères dans l'API

CHNSSolver hérite de NavierStokesSolver et sélectionne les assembleurs. ElasticitySolver prépare un état géométrique avant le calcul. ScratchDataCHNS contient les champs nécessaires aux contributions locales. TimeHandler reçoit les informations utilisées par le contrôle de pas.

Les commentaires sources sont conservés tels quels. La fiche workflow signale notamment un commentaire périmé sur l'injection de ψ ; la fiche physique distingue le résidu réellement assemblé de certains commentaires de signes. Ces divergences documentaires ne constituent pas des bugs numériques reproduits.

Les tests présents dans le snapshot sont des cas à relancer sur le PC FEZ. Le registre des 61 commits et les 13 imports de master sont accessibles dans le Journal de l'atlas, séparément de cette référence d'API.
