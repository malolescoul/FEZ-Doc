# Versionnement des rendus

Destination : `C:/Users/Malol/OneDrive/Bureau/FEZ Doc`.
Dépôt privé : [malolescoul/FEZ-Doc](https://github.com/malolescoul/FEZ-Doc).

Au début de ce complément, le premier rendu était commité en **332d857** (`Document FEZ day one with hierarchical atlas and Doxygen`). Le suivi local indiquait `main...origin/main` et un arbre de travail propre. L'ancien obstacle de propriété Git a donc été résolu côté utilisateur.

Cette édition ajoute la référence historique cc8dace, les analyses du workflow et des formulations, le registre de 61 commits et 13 apports de master, les parcours interactifs, les exercices et la troisième référence Doxygen. Aucun calcul FEZ n'est modifié.

Le complément est livré sous forme de fichiers à versionner. Un commit ou un push ne doit être annoncé qu'après vérification effective. Les verrous `.git` ayant été refusés au compte sandbox lors de la session précédente, les commandes suivantes permettent de finaliser depuis le PowerShell habituel si cette limite persiste :

```powershell
Set-Location 'C:/Users/Malol/OneDrive/Bureau/FEZ Doc'
git status --short
git add .
git commit -m "Document pre-AMR workflow and CHNS branch history"
git push
```

Le remote existe déjà : ne pas refaire `remote add`. En cas d'erreur de propriété sous un autre compte, une exception `safe.directory` doit viser uniquement ce dépôt. Aucune exception globale `*` n'est nécessaire.

## Sources des rendus

Les Markdown de `knowledge/` et `pedagogie/` sont les textes canoniques. `data/atlas.json` décrit les graphes ; `data/history-ledger.json` conserve le registre historique. `tools/refresh-atlas.mjs` recharge ce registre, rend les textes et les équations, vérifie les extraits et produit `assets/data.js` pour la lecture hors ligne.

Installer la dépendance `marked` dans `tools/` avant de relancer ce script avec Node.js. KaTeX est conservé localement avec sa licence et sa provenance dans `assets/vendor/katex/`. [Documentation du rendu mathématique](https://katex.org/docs/node.html).

Exécuter ensuite `python tools/validate-atlas.py` et `python tools/validate-history.py`. La régénération de Doxygen est décrite dans [son guide](doxygen/README.md). Toute mise à jour des sources doit conserver le SHA correspondant ; une ancienne référence historique ne suit jamais silencieusement le HEAD.

Pour reprendre le travail, lire [START_HERE](knowledge/START_HERE.md) puis le [protocole de session](knowledge/SESSION_PROTOCOL.md).
