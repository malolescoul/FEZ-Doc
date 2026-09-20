# Versionnement des rendus

Destination demandée : C:\Users\Malol\OneDrive\Bureau\FEZ Doc.

Dépôt distant : https://github.com/malolescoul/FEZ-Doc.git (privé, créé pendant la session).

Le dépôt documentaire est distinct du dépôt FEZ. Le premier rendu comprend la page, les données, les fiches, les exercices, les sources sélectionnées et Doxygen. Il ne modifie aucun calcul FEZ.

Les fichiers sont copiés dans le dossier demandé et Git y est initialisé sur main. **Aucun commit ni push n’a pu être créé** : le sandbox refuse les verrous .git/config.lock et .git/index.lock, même après autorisation du dossier et de .git. Le connecteur GitHub renvoie aussi 404 pour ce dépôt privé et le client Git ne dispose pas d’une authentification utilisable. Aucune protection système n’a été modifiée.

## Finaliser depuis ton terminal habituel

Ces commandes agissent uniquement dans le dépôt documentaire demandé. Si le dépôt distant contient déjà un commit initial, le push peut être refusé : il faudra alors récupérer et intégrer cet historique, sans forcer.

```powershell
Set-Location 'C:\Users\Malol\OneDrive\Bureau\FEZ Doc'
git remote add origin https://github.com/malolescoul/FEZ-Doc.git
git add .
git commit -m "Document FEZ day one with hierarchical atlas and Doxygen"
git push -u origin main
```

Le remote n’a pas été ajouté pendant la session à cause du verrou refusé. Si tu l’as ajouté entre-temps, vérifie git remote -v et saute la seconde commande au lieu de remplacer une configuration existante. Authentifie Git avec le compte ayant accès au dépôt privé lorsque nécessaire.

Le contenu canonique du graphe est data/atlas.json. assets/data.js en est la copie embarquée pour la lecture hors ligne. Après modification de la connaissance, exécuter tools/refresh-atlas.mjs (Node.js et la dépendance marked de tools/package.json), puis tools/validate-atlas.py. Si les sources ou les SHA changent, régénérer aussi les snapshots et Doxygen et mettre à jour state.json.

Pour une session suivante, lire knowledge/START_HERE.md et knowledge/SESSION_PROTOCOL.md avant d’interpréter la carte comme actuelle.
