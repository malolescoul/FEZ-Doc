# Références Doxygen locales — FEZ

Trois références isolent les états du code étudiés. La référence pré-AMR est le parent immédiat du commit AMR, sur la branche `chns-ding-horriche-master-form`.

| Référence | Commit immuable | Snapshot conservé | Fichiers dans l’API | Pages HTML | Avertissements |
|---|---|---:|---:|---:|---:|
| [master](master/html/index.html) | `ccf20caa0745cc2fe640f879d34acf2bf3855e6c` | 25 | 25 | 200 | 24 |
| [Branche personnelle pré-AMR](pre_amr/html/index.html) | `cc8dace141900b82e5790fa878e39d9c54898784` | 46 | 34 | 395 | 46 |
| [Branche personnelle avec AMR](prod/html/index.html) | `35d43b8e3bc4cae33a6ed7b6b57a6f3d77e93858` | 28 | 26 | 200 | 42 |

Les trois références HTML et XML ont été générées avec **Doxygen 1.18.0**, avec un code de retour **0** pour chaque référence, puis vérifiées le **20 septembre 2026 UTC**. L’archive portable officielle a été vérifiée avec le SHA-256 publié avant exécution. Aucun logiciel n’a été installé au niveau du système.

Le [manifeste](manifest.json) conserve les commits, les empreintes des sources et des guides, les journaux de génération et les résultats des contrôles. Le nombre de fichiers conservés mesure le contenu des snapshots ; il ne constitue pas un inventaire de lectures approfondies. Les snapshots sont **partiels**, et cette édition ne prétend pas fournir l’API exhaustive de FEZ. Les 12 fichiers de tests pré-AMR et les 2 tests de la référence AMR sont conservés hors index API ; leur présence ne signifie pas qu’ils ont été exécutés.

## Guides et mathématiques hors ligne

Les neuf guides sont synchronisés depuis les Markdown canoniques de `../knowledge`. Les quatre guides pré-AMR donnent accès au [workflow](pre_amr/html/fez_pre_amr_workflow.html), aux [modèles CHNS](pre_amr/html/fez_pre_amr_models.html), au [presolver et au cache](pre_amr/html/fez_pre_amr_presolver.html) et aux [mobilités, corrections et pas de temps](pre_amr/html/fez_pre_amr_mobility.html).

Les copies destinées à Doxygen reçoivent des identifiants de page stables, des délimiteurs mathématiques protégés, des liens explicites entre références et un marqueur de fin de guide. Cette protection évite que Doxygen interprète une commande mathématique telle que `\dot` comme l’ouverture d’un bloc Graphviz. Les fichiers Markdown canoniques et les sources C++ ne sont pas modifiés par cette préparation.

`render-math.mjs` transforme ensuite les formules en **HTML et MathML statiques avec KaTeX 0.18.7** : **60 expressions** dans le guide des modèles et **63** dans celui des mobilités, soit **123**, sans échec de conversion. La feuille de style et les polices proviennent du dossier local `../assets/vendor/katex/dist`. Les scripts MathJax générés par Doxygen sont retirés ; les équations se lisent sans connexion et sans exécution JavaScript dans le navigateur.

La vérification a confirmé la présence de toutes les sections et du marqueur final de chacun des neuf guides, ainsi que le nombre exact de formules attendu depuis les sources Markdown. Aucun lien local ou fragment manquant, aucun script distant et aucun avertissement issu des guides n’a été relevé.

## Avertissements et limites

Les **24 / 46 / 42 avertissements** indiqués dans le tableau restent enregistrés dans les journaux [master](logs/master-warnings.log), [pré-AMR](logs/pre_amr-warnings.log) et [AMR](logs/prod-warnings.log). Ils concernent des commandes mathématiques présentes dans les commentaires C++ hérités, sans délimiteurs reconnus par Doxygen. Ces commentaires sont conservés tels quels : certaines formules de l’API restent donc en notation textuelle imparfaite, contrairement aux équations des guides rendues avec KaTeX. Ces avertissements documentaires ne démontrent pas une erreur numérique de FEZ.

Le header `include/post_processing_handler.h` a été ajouté au snapshot pré-AMR depuis son commit exact pour compléter les déclarations nécessaires à la documentation. Certaines dépendances restent absentes de ces snapshots partiels ; tous les symboles mentionnés ne disposent donc pas nécessairement d’une fiche API. Une signature extraite ou un commentaire affiché ne prouve pas que son comportement a été entièrement vérifié.

`fix-index-anchors.ps1` rétablit, uniquement dans le HTML généré, les ancres des index alphabétiques et des destructeurs émises incomplètement par Doxygen 1.18.0. La génération ne compile pas FEZ, ne lance aucun test numérique et n’utilise pas Graphviz. Les diagrammes interactifs de l’atlas restent le support de navigation entre les fonctionnalités.

## Régénérer

Depuis ce dossier, avec Doxygen 1.18.0, Node.js et Python disponibles :

```powershell
.\generate-docs.ps1 -DoxygenPath 'doxygen' -NodePath 'node'
python .\verify-docs.py
```

Les paramètres acceptent aussi des chemins absolus vers des exécutables portables. Le module KaTeX utilisé par Node est déjà conservé dans l’atlas : aucune installation npm ni ressource CDN n’est requise.

Le premier script synchronise les neuf guides, valide les chemins avant de nettoyer uniquement les trois dossiers de sortie générés, appelle les trois Doxyfile, rend les mathématiques et normalise les ancres. Les snapshots sont conservés. Les sorties sont `master/html/index.html`, `pre_amr/html/index.html` et `prod/html/index.html` ; les enregistrements `logs/*-generation.json` et `logs/*-math.json` décrivent chaque génération réussie.

`verify-docs.py` contrôle les copies préparées contre les Markdown canoniques, la fin et les sections des guides, les formules, les liens locaux, les fragments et l’absence de scripts distants. Il renouvelle les inventaires et le manifeste, et retourne un code non nul si un de ces contrôles échoue. Les commits et les informations de provenance de Doxygen sont fixés pour cette édition dans le script ; les actualiser explicitement lors d’un changement de snapshot ou de générateur.

Pour enrichir la référence, compléter chaque snapshot depuis son propre commit immuable, puis régénérer et vérifier. Les points d’entrée `main` sont exclus de l’index des symboles pour éviter de fusionner les exécutables ; leurs fichiers source restent consultables. Cette génération n’a modifié aucun dépôt FEZ et n’a créé aucun commit ou PR.

## Sources de la méthode

- [Doxygen : démarrage](https://www.doxygen.nl/manual/starting.html).
- [Doxygen : configuration](https://www.doxygen.nl/manual/config.html).
- [Distribution officielle et SHA-256](https://www.doxygen.nl/download.html).
- [KaTeX : options de rendu](https://katex.org/docs/options.html).
