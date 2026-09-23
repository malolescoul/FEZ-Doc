# Complément du jour 1 — référence avant le nouveau couplage AMR

Référence : `cc8dace141900b82e5790fa878e39d9c54898784`, parent direct de `35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858`. La référence contient déjà des infrastructures AMR importées de master. L'étude porte sur le workflow CHNS–ALE antérieur au nouveau couplage.

1. Lire les différences et les parents des 61 commits propres à la branche avant ce couplage ; reconstruire la bifurcation mobilité et les imports de master.
2. Reconstituer le parcours exécutable → presolver → géométrie/ψ → initialisation → calcul → diagnostics/reprise à cette révision.
3. Lire les formulations, les mobilités et leurs corrections en distinguant l'introduction historique du comportement final.
4. Conserver les preuves dans des fiches Markdown, un registre de commits et deux graphes de fonctions accessibles dans la hiérarchie existante.
5. Générer une référence Doxygen distincte pour cette révision ; vérifier liens, lignes, couverture du registre et navigation dans la page.
6. Livrer le dossier actualisé et son archive, puis synchroniser les fichiers avec le dépôt documentaire demandé.

Aucun build FEZ ni test numérique n'est disponible. Les résultats de tests mentionnés par un auteur restent des déclarations historiques ; les fichiers de test constituent des cas à reproduire. Le workflow décrit les chemins supportés par le code, sans supposer les paramètres du cas de production personnel.
