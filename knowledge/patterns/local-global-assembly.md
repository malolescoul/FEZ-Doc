# Motif : assemblage local → système global

Périmètre confirmé : CHNS sur `master@ccf20caa0745cc2fe640f879d34acf2bf3855e6c`. Ce motif est un **point de comparaison à réutiliser**, pas une affirmation que tous les solveurs FEZ ont été audités.

## Contrat des trois objets

| Objet | Ce qu'il contient | Qui l'utilise |
|---|---|---|
| ScratchData | Valeurs/gradients aux points de quadrature, fonctions de forme, paramètres physiques, historique temporel | L'opération locale le réinitialise ; les assembleurs le lisent. |
| CopyDataBase | Matrice locale, second membre local, indices globaux de l'élément, état de propriété de cellule | Les assembleurs y accumulent ; le copieur global le lit. |
| AffineConstraints | Relations entre DoFs et valeurs imposées | Transforme la contribution lors de la copie globale ; distribue ensuite les valeurs contraintes. |

L'interface `AssemblerBase` reçoit un `const ScratchData &` et un `CopyData &` : ses arguments rendent lisible la direction des données. [Interface](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/assembly/assembler.h#L20-L38), [CopyData](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/copy_data.h#L37-L101).

## Séquence observée

1. Remettre la matrice globale à zéro.
2. Pour chaque cellule, mémoriser si elle est owned puis ignorer les autres.
3. Réinitialiser le scratch depuis la solution d'évaluation.
4. Remettre la contribution locale à zéro.
5. Accumuler tous les assembleurs actifs.
6. Récupérer les indices globaux de DoFs.
7. Copier au système global avec les contraintes homogènes.
8. Terminer les additions distribuées par `compress(add)`.

[Étapes de matrice](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L420-L501). Le second membre utilise la même organisation. [Étapes RHS](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L516-L575).

## Invariants à confronter aux futures fonctionnalités

- **Ownership :** le worker et le copieur filtrent tous deux les cellules non owned. Si l'on change l'un, relire l'autre ; sinon une contribution conservée dans un CopyData réutilisé pourrait être copiée à tort.
- **Remise à zéro :** un élément commence avec une contribution nulle, puis les assembleurs additionnent leurs termes. Remplacer une addition par une affectation peut effacer une autre physique.
- **Ordre des données :** les assembleurs lisent un scratch correspondant à la cellule et au même point d'évaluation que le résidu/Jacobien attendus.
- **Numérotation :** les indices copiés doivent être ceux du DoFHandler et du FESystem utilisés pour calculer la contribution.
- **Contraintes :** l'incrément Newton reçoit les contraintes homogènes ; la solution reçoit les contraintes non homogènes.
- **Parallélisme :** le chemin matrice contient une assertion demandant un seul thread sous PETSc ; `main` initialise MPI avec une limite d'un thread. Cela ne signifie pas un seul rang MPI. [Assertion](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L429-L435), [entrée MPI](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/solvers/incompressible_chns.cpp#L10-L14).

Ces invariants donnent des **questions d'impact**, pas des bugs déclarés.

## Premier rapprochement CHNS / FSI

Le même fichier de scratch définit `ScratchDataFSI`, `ScratchDataFSI_hp` et `ScratchDataCHNS` en combinant des drapeaux. Le drapeau pseudo-solide est partagé entre les variantes FSI et CHNS mobile. Cela confirme un socle de préparation commun et justifie une prochaine analyse transversale des mappings et de la vitesse de maillage. Cela ne démontre pas encore l'identité des formes FSI et CHNS. [Alias](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/scratch_data.h#L130-L150).

Pour enregistrer un futur rapprochement, conserver : les deux symboles, leur révision, le contrat commun, les différences de paramètres/drapeaux, une preuve dans le code et les tests à exécuter. Un nom ressemblant ne suffit pas.

