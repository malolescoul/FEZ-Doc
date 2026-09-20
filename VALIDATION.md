# Validation du rendu — session 01

## Sources et connaissance

Deux SHA sont figés dans state.json : master ccf20caa0745 et branche personnelle 35d43b8e3bc4. Le catalogue contient 6 graphes de données composés en un canevas hiérarchique par branche : 2 racines de classes, 3 parcours de fonctionnalités et 1 intérieur de fonction. Les 83 entrées de nœuds et 99 relations incluent des alias fusionnés à l’affichage ; ce ne sont pas 83 classes distinctes de FEZ.

44 couples fichier/révision ont fait l’objet d’une lecture ciblée pour les fiches et les graphes. Des sources supplémentaires sont présentes dans Doxygen pour résoudre les déclarations. La présence d’un fichier complet dans un snapshot ne signifie pas qu’il a été audité intégralement.

La revue croisée a corrigé la direction d’un héritage FSI, distingué les séquences d’opérations des appels et précisé les hypothèses de propriété MPI concernées par la PR #93.

## Vérifications exécutées

Le validateur tools/validate-atlas.py contrôle les identifiants et extrémités des graphes, les types de relations, les SHA et bornes de lignes, les cibles des détails, les liens de documents locaux, les réponses des quiz et l’existence des deux références Doxygen générées. Ses six familles de contrôles passent.

Contrôles dans le navigateur :

- Dépliage CHNS conservant les classes parentes ; dépliage supplémentaire de assemble_matrix ; dépliage FSI ; repli vers les classes.
- Changement de branche et de provenance ; recherche de Rotation BDF avec le lien exact de la branche personnelle.
- Zoom par groupe, zoom à la molette, déplacement du canevas, filtres de séquence.
- Extrait et lien source d’un nœud ; lecteur Markdown et accès Doxygen.
- Réponse fausse puis correction ; score final 4/4 sur les quatre exercices.
- Vue de bureau 1280 pixels et vue compacte 390 pixels sans débordement horizontal de la page.
- Aucun message d’erreur JavaScript observé pendant cette vérification.

Une revue statique de l’interface a aussi corrigé la capture du pointeur pendant le déplacement d’un nœud, le téléchargement Markdown et la distinction du filtre « séquence ». Le clic simple différé évite que la fiche masque le second clic d’un double-clic.

Les interactions ont été vérifiées via un serveur local. Le navigateur de contrôle interdit les URL file:// ; l’ouverture directe du fichier HTML n’a donc pas été exécutée dans ce navigateur. L’atlas embarque ses scripts et ses données et ne dépend d’aucun service distant pour les lire.

## Doxygen

Deux générations réelles avec Doxygen 1.18.0, codes de retour 0. Le manifeste et l’audit des liens internes sont dans doxygen/. Les 24 avertissements master et 42 avertissements prod concernent les formules LaTeX non balisées de commentaires existants. Ils restent documentés, sans retouche du code FEZ.

## Limite décisive

Aucun build FEZ, aucune exécution numérique, aucun essai MPI n’a été réalisé. Les tests repérés dans GitHub attendent une reproduction sur le PC disposant des builds. Aucun nouveau bug n’est déclaré confirmé.
