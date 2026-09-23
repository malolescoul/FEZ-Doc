# Validation — jour 1 et complément pré-AMR

## Révisions et couverture

Deux HEADs demeurent suivis : master `ccf20caa0745` et branche personnelle `35d43b8e3bc4`. La référence historique `cc8dace141900` est leur contexte pré-AMR spécialisé, pas une troisième branche Git.

L'atlas contient **10 graphes, 159 entrées de nœuds et 198 relations**. Ils composent trois canevas hiérarchiques selon la révision choisie. Les alias et pivots peuvent se répéter dans les données ; ces nombres ne représentent pas des classes distinctes. Le complément apporte deux parcours de **35 et 30 nœuds** dans la référence pré-AMR.

**87 couples fichier/révision** font l'objet de lectures ciblées dans les fiches et graphes. Le snapshot Doxygen comprend aussi des déclarations nécessaires à l'API. Télécharger un fichier complet ne signifie pas auditer toutes ses lignes.

Le registre couvre **61 commits propres, 13 imports de master et cinq merges**. L'ensemble des 61 SHA correspond exactement à la comparaison GitHub indépendante master…cc8dace. Les parents proviennent des métadonnées de commit et l'ordre respecte toutes les dépendances internes. Les patches pertinents de chaque entrée ont été lus ; les contenus MMG et maillage omis par GitHub, ainsi que certaines incohérences de statistiques, restent explicitement signalés.

## Contrôles exécutés

- `tools/validate-atlas.py` : sept contrôles réussis sur endpoints, types, paragraphes des fiches, SHA/plages source, liens de navigation/documents, quiz et références Doxygen séparées.
- `tools/validate-history.py` : cinq contrôles réussis sur lien direct pré-AMR→AMR, couverture sans doublon, topologie/preuves, cohérence du registre embarqué et rendu mathématique.
- 126 expressions des Markdown compilées par KaTeX, sans erreur après correction de deux underscores dans des identifiants textuels. La notation mathématique reste dans les Markdown ; le HTML/MathML est généré localement.
- Relecture indépendante du workflow, des modèles et de l'histoire : correction d'une équation ψ initialement reprise d'un commentaire au signe différent du résidu. Les limites de preuve et les réversions de mobilité ont été confrontées au code.

Les premiers essais ont révélé un format de détails de nœud incorrect (chaîne au lieu de liste de paragraphes), corrigé puis couvert par le validateur. Ils ont également identifié le conflit entre les délimiteurs LaTeX des guides et les commandes Doxygen, corrigé par le prétraitement documentaire et le rendu mathématique local.

## Navigateur

- Sélection des trois révisions avec provenance correspondante.
- Référence pré-AMR : classes → CHNSSolver → workflow/modèles → fonctions, dans le même canevas. Le workflow déplié conserve 45 nœuds, dont ses parents.
- Recherche de « mobilité » puis sélection de la variante 2 finale : chemin récursif ouvert, fiche en paragraphes et source exacte `include/cahn_hilliard.h#L729-L759` à cc8dace.
- Historique : 61 entrées propres, filtre Fusion = 5, imports master = 13, recherche de SHA et résultat vide explicite ; détails, parents et liens de code présents.
- Le bouton d'exploration dans le Journal revient au workflow en refermant le lecteur.
- Fiche physique : formules HTML/MathML présentes et texte disponible jusqu'à sa dernière section. Sources immuables et téléchargements Markdown conservés.
- Vue bureau 1280 px ; contrôles historiques et page vérifiés à 390 px sans débordement horizontal global. Surcharge de viewport retirée après contrôle.
- Aucun message d'erreur JavaScript relevé pendant ces parcours.

Les interactions précédemment vérifiées (pan/zoom, repli, FSI, quatre quiz) restent décrites dans l'historique de la première édition. Les nouveaux contrôles ciblent les changements du complément. L'essai passe par un serveur HTTP local ; le navigateur de contrôle interdit `file://`. L'ouverture directe du fichier n'est donc pas déclarée testée ; scripts, données, CSS, polices et formules sont embarqués pour une lecture locale.

## Doxygen

Trois générations avec Doxygen 1.18.0, code de retour 0. Le manifeste vérifie les liens et ancres, les sources figées, les guides synchronisés et les formules rendues. Les avertissements conservés proviennent des commentaires source du snapshot ; aucun code FEZ n'est corrigé pour les masquer.

| Référence | Fichiers conservés | Pages HTML | Avertissements | Liens/ancres manquants |
|---|---:|---:|---:|---:|
| master | 25 | 200 | 24 | 0 |
| prod | 28 | 200 | 42 | 0 |
| pre_amr | 46 | 395 | 46 | 0 |

La référence reste partielle ; des dépendances extérieures aux snapshots ne sont pas indexées. Les avertissements et contrôles détaillés sont conservés dans `doxygen/logs` et `doxygen/manifest.json`.

## Ce qui n'a pas été exécuté

Aucun build FEZ, test numérique, essai MPI ou calcul de production. Les tests lus et les résultats mentionnés dans les messages de commit ne constituent pas une reproduction indépendante. Aucun nouveau bug numérique n'est déclaré confirmé. Les différences documentaires et les chemins à investiguer sont signalés comme tels.
