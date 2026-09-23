/*
 @licstart  The following is the entire license notice for the JavaScript code in this file.

 The MIT License (MIT)

 Copyright (C) 1997-2020 by Dimitri van Heesch

 Permission is hereby granted, free of charge, to any person obtaining a copy of this software
 and associated documentation files (the "Software"), to deal in the Software without restriction,
 including without limitation the rights to use, copy, modify, merge, publish, distribute,
 sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all copies or
 substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
 BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

 @licend  The above is the entire license notice for the JavaScript code in this file
*/
var NAVTREE =
[
  [ "FEZ — workflow avant AMR", "index.html", [
    [ "FEZ — workflow de référence avant le couplage CHNS–ALE AMR", "index.html", "index" ],
    [ "Physique CHNS avant la nouvelle adaptation h", "fez_pre_amr_models.html", [
      [ "Trois axes de configuration indépendants", "fez_pre_amr_models.html#autotoc_md0", null ],
      [ "Les équations : partir du résidu assemblé", "fez_pre_amr_models.html#autotoc_md1", [
        [ "Pourquoi NLM garde φ et μ comme inconnues", "fez_pre_amr_models.html#autotoc_md2", null ]
      ] ],
      [ "ψ : un problème de Helmholtz couplé à la géométrie", "fez_pre_amr_models.html#autotoc_md3", null ],
      [ "Stabilisation : résidu fort, tests modifiés, géométrie ALE", "fez_pre_amr_models.html#autotoc_md4", null ],
      [ "Pression et diagnostics : comparer les bonnes quantités", "fez_pre_amr_models.html#autotoc_md5", null ],
      [ "Douze jalons à relire dans les patches", "fez_pre_amr_models.html#autotoc_md6", null ],
      [ "Lire les tests avec leur portée", "fez_pre_amr_models.html#autotoc_md7", null ]
    ] ],
    [ "Le workflow CHNS–ALE avant le nouvel AMR", "fez_pre_amr_workflow.html", [
      [ "Le socle à retenir", "fez_pre_amr_workflow.html#autotoc_md8", null ],
      [ "1. Choisir l'exécutable et construire les objets", "fez_pre_amr_workflow.html#autotoc_md9", null ],
      [ "2. Préparer une géométrie comprimée", "fez_pre_amr_workflow.html#autotoc_md10", null ],
      [ "3. Passer du presolver à CHNS", "fez_pre_amr_workflow.html#autotoc_md11", null ],
      [ "4. Imposer les bords sur la bonne géométrie", "fez_pre_amr_workflow.html#autotoc_md12", null ],
      [ "5. Boucle temporelle et reprise", "fez_pre_amr_workflow.html#autotoc_md13", null ],
      [ "6. Observer ce que le calcul produit", "fez_pre_amr_workflow.html#autotoc_md14", null ],
      [ "Cas concrets lus, sans extrapoler aux réglages personnels", "fez_pre_amr_workflow.html#autotoc_md15", null ],
      [ "Ce que le nouveau couplage AMR change précisément", "fez_pre_amr_workflow.html#autotoc_md16", null ],
      [ "Invariants à garder pour les ajouts suivants", "fez_pre_amr_workflow.html#autotoc_md17", null ]
    ] ],
    [ "Du modèle de mobilité au flux corrigé et au pas de temps", "fez_pre_amr_mobility.html", [
      [ "Un contrat de données commun", "fez_pre_amr_mobility.html#autotoc_md21", null ],
      [ "Les cinq lois finales, sans confondre les versions historiques", "fez_pre_amr_mobility.html#autotoc_md22", [
        [ "La généalogie du modèle 2 explique pourquoi le titre d'un commit ne suffit pas", "fez_pre_amr_mobility.html#autotoc_md23", null ]
      ] ],
      [ "Parcours en assemblage : M atteint plusieurs équations", "fez_pre_amr_mobility.html#autotoc_md24", null ],
      [ "Correction de profil et projection du flux", "fez_pre_amr_mobility.html#autotoc_md25", [
        [ "Les révisions changent le comportement, pas seulement les noms", "fez_pre_amr_mobility.html#autotoc_md26", null ]
      ] ],
      [ "Le critère temporel fondé sur la mobilité", "fez_pre_amr_mobility.html#autotoc_md27", null ],
      [ "Tests lus et expériences utiles avant une extension", "fez_pre_amr_mobility.html#autotoc_md28", null ]
    ] ],
    [ "Motif — presolver, cache et géométrie d'évaluation", "fez_pre_amr_presolver.html", [
      [ "Trois représentations, trois contrats", "fez_pre_amr_presolver.html#autotoc_md29", null ],
      [ "Écrire avant de déplacer", "fez_pre_amr_presolver.html#autotoc_md30", null ],
      [ "Valider avant de réutiliser", "fez_pre_amr_presolver.html#autotoc_md31", null ],
      [ "Injecter un état cohérent", "fez_pre_amr_presolver.html#autotoc_md32", null ],
      [ "Échos utiles pour la suite", "fez_pre_amr_presolver.html#autotoc_md33", null ]
    ] ],
    [ "Espaces de nommage", "namespaces.html", [
      [ "Liste des espaces de nommage", "namespaces.html", "namespaces_dup" ],
      [ "Membres de l'espace de nommage", "namespacemembers.html", [
        [ "Tout", "namespacemembers.html", null ],
        [ "Fonctions", "namespacemembers_func.html", null ],
        [ "Variables", "namespacemembers_vars.html", null ],
        [ "Définitions de type", "namespacemembers_type.html", null ],
        [ "Énumérations", "namespacemembers_enum.html", null ],
        [ "Valeurs énumérées", "namespacemembers_eval.html", null ]
      ] ]
    ] ],
    [ "Classes", "annotated.html", [
      [ "Liste des classes", "annotated.html", "annotated_dup" ],
      [ "Index des classes", "classes.html", null ],
      [ "Hiérarchie des classes", "hierarchy.html", "hierarchy" ],
      [ "Membres de classe", "functions.html", [
        [ "Tout", "functions.html", "functions_dup" ],
        [ "Fonctions", "functions_func.html", "functions_func" ],
        [ "Variables", "functions_vars.html", "functions_vars" ],
        [ "Définitions de type", "functions_type.html", null ],
        [ "Énumérations", "functions_enum.html", null ],
        [ "Symboles associés", "functions_rela.html", null ]
      ] ]
    ] ],
    [ "Fichiers", "files.html", [
      [ "Liste des fichiers", "files.html", "files_dup" ],
      [ "Membres de fichier", "globals.html", [
        [ "Tout", "globals.html", null ],
        [ "Fonctions", "globals_func.html", null ],
        [ "Variables", "globals_vars.html", null ],
        [ "Macros", "globals_defs.html", null ]
      ] ]
    ] ]
  ] ]
];

var NAVTREEINDEX =
[
"annotated.html",
"class_c_h_n_s_solver.html#a1e5188a61fc785855103ae478c6ca152",
"class_generic_solver.html#a231b6929535d7e1834e9072f920d618b",
"class_navier_stokes_scratch_1_1_scratch_data.html#a5aa4c26c5510e901756ac9357dedccb7",
"class_navier_stokes_scratch_1_1_scratch_data.html#af19971aee6b96279bc0151b04264bf24",
"class_parameters_1_1_cahn_hilliard.html#af6d1d0761c12923e197a8dd3fc881402a588396a4841ade426b36d7039704518b",
"class_vector_function_from_components.html#abb63dcbb6a3c15e6af086045240303c0",
"namespace_cahn_hilliard.html#a26d9455e41da6c54c7f2ff8eca43f4cd",
"struct_parameters_1_1_elasticity.html#a524dbc8ffa87a8a99506354d65fa55e2",
"struct_parameters_1_1_mesh.html#a6eb432a39c41bb4020b6c983d5bc2441",
"struct_parameters_1_1_post_processing_1_1_post_processing_base.html#a921eee483d06be1b60f73ad5194704cf"
];

const SYNCONMSG = 'cliquez pour désactiver la synchronisation du panel';
const SYNCOFFMSG = 'cliquez pour activer la synchronisation du panel';
const LISTOFALLMEMBERS = 'Liste de tous les membres';