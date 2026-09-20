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
  [ "FEZ — CHNS ALE · branche personnelle", "index.html", [
    [ "FEZ — CHNS ALE et AMR", "index.html", "index" ],
    [ "CHNS–ALE et adaptation du maillage : première carte vérifiée", "fez_prod_chns_ale_amr.html", [
      [ "Ce qu'il faut retenir", "fez_prod_chns_ale_amr.html#autotoc_md0", null ],
      [ "Points d'entrée et responsabilités", "fez_prod_chns_ale_amr.html#autotoc_md1", null ],
      [ "Parcours 1 — préparer un état CHNS sur la géométrie comprimée", "fez_prod_chns_ale_amr.html#autotoc_md2", null ],
      [ "Parcours 2 — décider où raffiner", "fez_prod_chns_ale_amr.html#autotoc_md3", [
        [ "Kelly multichamp", "fez_prod_chns_ale_amr.html#autotoc_md4", null ],
        [ "Bande autour de l'interface", "fez_prod_chns_ale_amr.html#autotoc_md5", null ]
      ] ],
      [ "Parcours 3 — transporter, puis reconstruire", "fez_prod_chns_ale_amr.html#autotoc_md6", null ],
      [ "Assemblage : les premiers liens vérifiés", "fez_prod_chns_ale_amr.html#autotoc_md7", null ],
      [ "Différence avec master effectivement lue", "fez_prod_chns_ale_amr.html#autotoc_md8", null ],
      [ "Tests disponibles et statut", "fez_prod_chns_ale_amr.html#autotoc_md9", null ],
      [ "Impacts à surveiller et suite de lecture", "fez_prod_chns_ale_amr.html#autotoc_md10", null ]
    ] ],
    [ "Motif — transporter un état distribué qui contient sa géométrie", "fez_prod_distributed_state_transfer.html", [
      [ "Résumé pour reprendre rapidement", "fez_prod_distributed_state_transfer.html#autotoc_md16", null ],
      [ "Les objets et leurs contrats", "fez_prod_distributed_state_transfer.html#autotoc_md17", null ],
      [ "Séquence observée", "fez_prod_distributed_state_transfer.html#autotoc_md18", null ],
      [ "Trois invariants à conserver", "fez_prod_distributed_state_transfer.html#autotoc_md19", [
        [ "1. Même index, même sens, même instant", "fez_prod_distributed_state_transfer.html#autotoc_md20", null ],
        [ "2. Géométrie reconstruite avant ses consommateurs", "fez_prod_distributed_state_transfer.html#autotoc_md21", null ],
        [ "3. État temporel au-delà du BDF nominal", "fez_prod_distributed_state_transfer.html#autotoc_md22", null ]
      ] ],
      [ "Échos déjà identifiés", "fez_prod_distributed_state_transfer.html#autotoc_md23", null ],
      [ "Ce qui pourrait casser si le motif évolue", "fez_prod_distributed_state_transfer.html#autotoc_md24", null ],
      [ "Preuves testables déjà dans le dépôt", "fez_prod_distributed_state_transfer.html#autotoc_md25", null ],
      [ "Exercice C++ de lecture", "fez_prod_distributed_state_transfer.html#autotoc_md26", null ]
    ] ],
    [ "Espaces de nommage", "namespaces.html", [
      [ "Liste des espaces de nommage", "namespaces.html", "namespaces_dup" ],
      [ "Membres de l'espace de nommage", "namespacemembers.html", [
        [ "Tout", "namespacemembers.html", null ],
        [ "Fonctions", "namespacemembers_func.html", null ],
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
        [ "Symboles associés", "functions_rela.html", null ]
      ] ]
    ] ],
    [ "Fichiers", "files.html", [
      [ "Liste des fichiers", "files.html", "files_dup" ],
      [ "Membres de fichier", "globals.html", [
        [ "Tout", "globals.html", null ],
        [ "Fonctions", "globals_func.html", null ],
        [ "Variables", "globals_vars.html", null ]
      ] ]
    ] ]
  ] ]
];

var NAVTREEINDEX =
[
"annotated.html",
"class_generic_solver.html#a2ef873f5575b35c23fa5fd742b8725aa",
"class_navier_stokes_scratch_1_1_scratch_data.html#a5acec509178f227d79a2b167299a8a3d",
"class_navier_stokes_scratch_1_1_scratch_data.html#af3eae3291fa131c7990efa975d04541d",
"class_transient_fixed_point_data.html#a626ab1c7afbd39e6925e5596e3fcb650",
"timestep__adaptation_8cpp_source.html"
];

const SYNCONMSG = 'cliquez pour désactiver la synchronisation du panel';
const SYNCOFFMSG = 'cliquez pour activer la synchronisation du panel';
const LISTOFALLMEMBERS = 'Liste de tous les membres';