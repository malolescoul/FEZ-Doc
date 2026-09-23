# Complément du jour 1 — comprendre le socle avant l'AMR récent

Étude du 20 septembre 2026. Référence : **cc8dace141900b82e5790fa878e39d9c54898784**, parent direct de **35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858**. Sources GitHub, sans build FEZ.

## Ce qui change dans notre compréhension

La première lecture partait du HEAD et mettait l'adaptation au centre. Cette lecture rétablit le workflow qui existait avant le nouveau couplage CHNS–ALE AMR. Le presolver, ψ, les modèles de mobilité et les outils d'observation ont leur propre histoire ; ils ne sont pas des sous-produits de l'AMR.

Le périmètre comprend **61 commits propres à la branche**, dont cinq merges, et **13 commits de master entre le point de départ historique et le master intégré au baseline**. Ce sont deux ensembles distincts. Les 61 commits incluent des correctifs et des tests ; ils ne représentent pas 61 nouvelles fonctionnalités. Le [registre historique](../history/chronologie-branche.md) précise pour chacun son rôle, ses parents et les limites des différences consultées.

## Parcours de référence

1. L'exécutable choisit la dimension et la variante standard/enlarged puis lit les paramètres.
2. Si demandé, le presolver prépare la géométrie et, en enlarged, ψ ; le cache peut restituer cet état.
3. CHNS reçoit cet état et initialise les champs physiques sur la géométrie pertinente.
4. Les assembleurs choisis par les paramètres, le scratch et les mappings déterminent le calcul local. Newton et la boucle temporelle orchestrent les résolutions.
5. Sorties, diagnostics, sondes et reprise permettent de suivre le calcul et de reprendre son historique.

Les preuves et conditions d'activation sont dans le [workflow détaillé](../features/workflow-pre-amr.md), le [motif cache/géométrie](../patterns/presolver-cache-geometry.md) et la [fiche des modèles](../features/chns-models-pre-amr.md). Ce parcours est supporté par le dépôt ; les paramètres exacts du cas de production de l'utilisateur restent à relever sur son PC.

## Trois enseignements de l'histoire

**La mobilité a sa propre bifurcation.** Elle est développée sur une lignée distincte, puis rejoint les travaux de BC du traceur et de presolver. Une simple liste de commits triée par date masquerait cette articulation. Le registre conserve les parents et un ordre compatible avec ces dépendances.

**Une introduction peut être modifiée presque aussitôt.** Le modèle de mobilité 2 passe par une extension des queues puis une restriction au cœur de l'interface. La correction de profil passe par une indépendance vis-à-vis de M avant de revenir à la mobilité locale. La fiche [mobilité, corrections et pas de temps](../patterns/mobility-corrections-timestep.md) décrit le comportement présent à cc8dace, sans figer la première intention comme contrat final.

**« Avant AMR » doit rester qualifié.** Le merge cc8dace a déjà intégré l'AMR Navier–Stokes de master. L'ajout récent 35d43b8 porte sur le couplage spécifique CHNS–ALE, le presolver et le transfert de leurs états. La [fiche AMR au HEAD](../features/chns-ale-amr.md) reste une vue distincte.

## Liens à surveiller lors des prochaines modifications

| Si cette partie change… | Relire aussi… | Pourquoi |
|---|---|---|
| Ordre des composantes, ajout de ψ | Presolver, cache, masques, BC, extracteurs de posttraitement | Un champ ajouté doit garder sa signification dans chaque consommateur |
| Fonction ou champ de forçage du maillage | Reconstruction ψ, normalisation, empreinte du cache, géométrie initiale | Réutiliser une géométrie ancienne peut contredire les nouveaux paramètres |
| Loi de mobilité | Dérivées du scratch, résidu/Jacobien, correction de profil, contrôle du pas | Une seule option agit à plusieurs étages du calcul |
| Mapping ou vitesse ALE | Interpolation initiale, BC, convection/SUPG, taille de cellule et CFL | Les évaluations doivent employer le repère prévu |
| Nouvelle adaptation | Tous les invariants précédents et historiques temporels | L'AMR ajoute un changement de maillage et de distribution au workflow existant |
| Modèle physique | Pression exportée, diagnostics et intégrales interprétées | Un nom de champ identique ne garantit pas une convention physique identique |

Ces lignes sont des chemins de relecture et de validation, pas des défaillances observées.

## Niveau de preuve et suite utile

Les appels, copies et gardes décrits dans les fiches sont lus dans les sources citées. Les grandes intégrations où GitHub omet une partie du patch sont signalées dans le registre. Des commentaires périmés ou ambigus sont relevés sans être transformés en bugs de calcul.

Sur le PC FEZ, commencer par identifier un cas personnel représentatif et son jeu de paramètres. Reproduire le workflow pré-AMR et ses invariants géométriques, puis comparer le même cas avec l'AMR désactivé au HEAD, avant d'activer l'adaptation. Les tests existants de presolver, Jacobien et contrôle de pas fournissent des points d'appui ; leur présence ne remplace pas leur exécution.

La référence ancienne demeure figée. Une prochaine session actualisera le HEAD et les conclusions concernées sans réécrire rétroactivement ce que cc8dace faisait.
