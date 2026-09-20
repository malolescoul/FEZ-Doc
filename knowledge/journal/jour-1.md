# Jour 1 — première base vérifiable

Session du 19 septembre 2026, capture terminée le 20 septembre à 03:16 UTC. [État des branches](../branches.md).

## Périmètre réel

Lecture de sources sélectionnées aux deux SHA prioritaires, comparaison de branches et étude des descriptions, fichiers modifiés, discussions et reviews de **cinq PR** : #81, #86, #91, #92, #93. Une liste de quinze PR récentes a servi au repérage ; les dix autres ne sont pas présentées comme analysées.

Aucun calcul FEZ n’a été exécuté. La présence de fichiers de tests et de sorties de référence est documentée ; leur passage n’est pas affirmé. Cette journée constitue une base d’observations, pas un audit exhaustif ni une certification scientifique.

## Les rapprochements utiles

### 1. AMR → transfert → conservation du traceur → intégrale de champ

Dans [la review de #81](https://github.com/arthurbawin/fez/pull/81#discussion_r3935556906), la question porte sur la conservation de l’intégrale de phase_tracer lors du déraffinement. La [réponse de l’auteur](https://github.com/arthurbawin/fez/pull/81#discussion_r3936199510) reconnaît que le transfert ne garantit pas cette conservation sans traitement spécifique. Le besoin de mesure conduit explicitement à une PR séparée, [annoncée ici](https://github.com/arthurbawin/fez/pull/81#discussion_r3936282798), puis réalisée par [#91](https://github.com/arthurbawin/fez/pull/91).

**Ce que cela apprend sur FEZ :** la fonctionnalité de posttraitement n’est pas isolée. Elle fournit un observateur pour étudier les conséquences du transfert de solution après AMR. Mesurer une intégrale ne rend toutefois pas le transfert conservatif.

**Contrat à retenir :** les reviews de #91 demandent un calcul à chaque pas, puis une écriture selon output_frequency. [Décision](https://github.com/arthurbawin/fez/pull/91#discussion_r3940041730) et [réponse d’implémentation](https://github.com/arthurbawin/fez/pull/91#discussion_r3941130525). Une modification de la fréquence d’écriture ne devrait donc pas supprimer des valeurs de la table.

**À faire avec un build :** comparer l’intégrale juste avant et juste après le transfert, avec déraffinement non nul, afin de séparer l’erreur du solveur physique de celle de l’adaptation.

### 2. AMR → objets à DoF → durée de validité des mappings

La review de #81 rappelle que les postprocesseurs à DoF conservent un espace EF, un DoFHandler, des matrices et vecteurs associés au maillage. [Question de validité après adaptation](https://github.com/arthurbawin/fez/pull/81#discussion_r3919371805) ; [réponse prévoyant leur réinitialisation](https://github.com/arthurbawin/fez/pull/81#discussion_r3922552605).

**Ce que cela apprend :** changer le maillage dépasse les cellules. Il faut examiner la durée de validité de tous les objets qui dépendent de sa numérotation ou de sa géométrie. Ce motif rejoint l’ordre d’initialisation ALE et les transferts de la branche personnelle.

La discussion [sur l’ALE initial](https://github.com/arthurbawin/fez/pull/81#discussion_r3935504788) cite d’ailleurs directement chns-ding-horriche-master-form. L’auteur [réserve cette prise en charge à une étape ultérieure](https://github.com/arthurbawin/fez/pull/81#discussion_r3936254897). Une limite d’une ancienne PR ne doit pas devenir une limite supposée de tous les HEADs ultérieurs.

### 3. FSI MPI : posséder une position n’est pas posséder une face

La [PR #93](https://github.com/arthurbawin/fez/pull/93) explique qu’un rang peut posséder un DoF de position sur le solide sans posséder une face du solide. Les accumulateurs de force étant liés aux intégrales de faces, le même critère de propriété ne peut pas sélectionner les deux ensembles.

Le patch change notamment :
- le critère d’attribution des DoF de vitesse du solide et de l’angle ;
- l’ajout des accumulateurs aux ghosts des rangs ayant un maître de position ;
- la garde du motif creux quand aucun DoF de vitesse du solide n’existe sur le rang ;
- l’usage de coupling_table dans NSSolver::create_sparsity_pattern.

Les deux sources prioritaires de monolithic_fsi_solver.cpp sont identiques et conservent les conditions ciblées par #93. **Signal connu à reproduire**, sans annoncer un bug nouvellement découvert ni une correction acquise. La PR reste ouverte et l’API n’a retourné aucune review au moment de la capture.

**À faire avec un build :** conserver un partitionnement qui dissocie propriété des faces et des nœuds, puis comparer plusieurs nombres de rangs et les modes debug/release.

### 4. Forces : une ressemblance de calcul masque une différence de pression

La [PR #92](https://github.com/arthurbawin/fez/pull/92) ajoute la gestion par frontière et propose une conversion de pression par la densité. La [review physique](https://github.com/arthurbawin/fez/pull/92#discussion_r4027016768) signale que CHNS ne divise pas son équation de quantité de mouvement par la densité comme le solveur NS mentionné et utilise une pression modifiée dépendant de la formulation.

**Ce que cela apprend :** partager une fonction de calcul de contraintes n’autorise pas à partager une interprétation de la variable pression. Une future fiche de fonction doit expliquer les unités et la signification de ses arguments.

La review formelle de #92 est **CHANGES_REQUESTED** au 16 septembre. [Synthèse du reviewer](https://github.com/arthurbawin/fez/pull/92#pullrequestreview-5222878123) : généraliser les frontières au niveau du type de paramètres commun, privilégier les sorties individuelles, nettoyer le code. Ce sont des demandes de review ; elles ne sont pas assimilées à des changements déjà fusionnés.

### 5. FSI : la conversation corrige la description initiale d’une PR

[#86](https://github.com/arthurbawin/fez/pull/86) introduit masse non nulle et rotation du solide rigide. La review demande si la force résultante suffit pour exprimer le moment. L’auteur [reconnaît le terme manquant](https://github.com/arthurbawin/fez/pull/86#discussion_r3813515326), puis [annonce l’ajout du couple autour du centre du solide](https://github.com/arthurbawin/fez/pull/86#issuecomment-5356273799).

Le code courant contient lambda_torque_coeffs. Le chemin de rotation avec accumulateurs porte toujours une [limitation explicite dans le second membre](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/monolithic_fsi_solver.cpp#L2742). La discussion finale et le code sont donc plus précis que la description initiale sur les couplages pris en charge.

**Règle de mémoire :** conserver la décision finale et son contexte, tout en reliant l’ancienne hypothèse à la correction. Ne pas recopier aveuglément le corps d’une PR dans Doxygen.

## Tableau de l’activité étudiée

| PR | État capturé | Fichiers modifiés | Dernier état de review significatif |
| --- | --- | ---: | --- |
| [#81](https://github.com/arthurbawin/fez/pull/81) — AMR initial NS | Fusionnée le 4 septembre | 22 | APPROVED |
| [#86](https://github.com/arthurbawin/fez/pull/86) — masse et rotation FSI | Fusionnée le 22 août | 22 | APPROVED |
| [#91](https://github.com/arthurbawin/fez/pull/91) — intégrales de champs | Fusionnée le 15 septembre | 15 | APPROVED |
| [#92](https://github.com/arthurbawin/fez/pull/92) — forces multi-frontières | Ouverte | 9 | CHANGES_REQUESTED |
| [#93](https://github.com/arthurbawin/fez/pull/93) — LLVM et correctifs FSI | Ouverte | 25 | Aucune review retournée |

## Priorités de la prochaine session

1. Mesure avant/après AMR sur un cas CHNS contrôlé, en suivant solution courante et historiques BDF.
2. Scénario FSI MPI de #93 ; séparer propriété des nœuds, faces, accumulateurs et ghosts.
3. Pression physique/modifiée pour chaque formulation CHNS avant toute généralisation du calcul des forces.
4. Réexaminer le statut GitHub de #92 et #93 ; actualiser uniquement les fiches dont les preuves ont changé.

Les données de capture gardent les SHA, liens de discussions, états de review et listes de fichiers. Les rapprochements ci-dessus sont distingués des validations qui nécessitent encore une exécution.

