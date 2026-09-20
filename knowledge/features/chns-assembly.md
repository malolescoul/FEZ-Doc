# Assemblage CHNS — master, jour 1

Révision : `ccf20caa0745cc2fe640f879d34acf2bf3855e6c`. Statut : parcours et dépendances statiques confirmés ; formulation et résultats numériques non validés par exécution.

## Champs et composition

`CHNSSolver` construit un système d'éléments finis contenant vitesse u, pression p, traceur φ et potentiel μ ; la variante mobile ajoute la position x. Les degrés sont indépendamment paramétrables. Les masques et extracteurs sont construits à partir de `ordering`. [Construction](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L24-L91).

La classe choisit `ScratchDataCHNS<dim, with_moving_mesh>`, `CopyDataBase<1>` et une interface commune `AssemblerBase`. [Alias](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/incompressible_chns_solver.h#L16-L22). Il ne faut donc pas confondre **CHNS** (physique/choix de champs), **ScratchData** (valeurs préparées sur l'élément) et **Assembler** (contribution à la forme discrète).

## Une cellule, deux sorties

`assemble_matrix` et `assemble_rhs` organisent des parcours `WorkStream::run`. Chaque parcours possède une opération locale et une opération de copie vers le système global. Le système est mis à zéro avant le parcours, puis `compress(VectorOperation::add)` est appelé après. [Matrice](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L420-L450), [second membre](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L516-L575).

L'opération locale vérifie que la cellule appartient au rang courant, réinitialise le scratch avec le point d'évaluation et l'historique, remet la contribution locale à zéro et invoque chaque assembleur. Les indices globaux des DoFs de la cellule sont ensuite récupérés. [Opération locale](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L463-L489).

La copie utilise `zero_constraints.distribute_local_to_global`. Ce sont des contraintes sur l'**incrément**, ce qui explique le recours aux contraintes homogènes à cette étape. Les contraintes non homogènes sont appliquées à la solution et aux points d'évaluation pendant la progression de Newton. [Copie](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L491-L501), [Newton](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/newton_solver.h#L121-L129).

## Comment φ et μ influencent Navier–Stokes

Le scratch CHNS :
- extrait φ, ∇φ, μ et ∇μ depuis `current_solution` ;
- extrait l'historique de φ pour la dérivée temporelle ;
- limite φ pour calculer les propriétés mélangées ρ et η, ainsi que leurs dérivées utilisées par le Jacobien ;
- construit `diffusive_flux`, qui contient ici **déjà** le produit du gradient de vitesse par le gradient de potentiel, multiplié par M(ρ₁−ρ₀)/2.

Ce dernier nom mérite de la prudence : il ne désigne pas seulement le vecteur de flux diffusif J isolé. [Préparation CHNS](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/scratch_data.h#L1001-L1066), [paramètres](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/scratch_data.cpp#L384-L411).

Dans le résidu de quantité de mouvement, l'assembleur lit ρ, η, le terme `diffusive_flux` et φ∇μ. L'équation du traceur lit la convection et la diffusion de μ ; l'équation du potentiel lit φ(φ²−1) et le gradient de φ. C'est une dépendance **couplée dans les équations**, et pas seulement une proximité de fichiers. [Expressions et accumulation](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/assembly/incompressible_chns_assemblers.cpp#L54-L105), [formes testées](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/assembly/incompressible_chns_assemblers.cpp#L133-L184).

Le Jacobien possède des variations par rapport à la vitesse et au potentiel pour la contribution diffusive. Modifier le modèle du flux impose de relire le calcul dans le scratch **et** ses dérivées dans l'assembleur. [Dérivées](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/assembly/incompressible_chns_assemblers.cpp#L363-L410).

## Sélection, stabilisation et ALE

Les paramètres SUPG/PSPG et SUPG du traceur sélectionnent des spécialisations de `VolumeAssembler` à drapeaux de compilation. Les calculs supplémentaires du scratch sont activés par options d'exécution. Leur accord est une condition de cohérence. Le constructeur de la liste vérifie aussi l'accord entre variante ALE et drapeau pseudo-solide du scratch. [Sélection](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/assembly/incompressible_chns_assemblers.h#L131-L200).

**Limitation explicite de cette révision :** la sélection rejette SUPG ou SUPG du traceur avec le maillage mobile. Il s'agit d'une restriction déclarée par le code, pas d'un bug découvert. Dans le Jacobien stabilisé, τ est tenu constant ; le commentaire précise que résidu et opérateur test sont linéarisés. [Restriction](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/assembly/incompressible_chns_assemblers.h#L155-L159), [τ](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/assembly/incompressible_chns_assemblers.cpp#L384-L404).

L'initialisation CHNS ajoute aussi les assembleurs d'élasticité lorsque `with_moving_mesh=true`. Le scratch calcule alors les données pseudo-solides avant celles de Navier–Stokes, car la vitesse de maillage est nécessaire. [Composition](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L259-L273), [ordre de calcul](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/scratch_data.h#L1153-L1186). Cela situe un point de rencontre avec le domaine FSI sans affirmer que toute la chaîne FSI a été étudiée.

## Sparsité et cohérence du Jacobien

`create_sparsity_pattern` établit une table de couplage par composantes. Avec SUPG, les lignes pression sont élargies aux autres variables, notamment via le résidu fort de quantité de mouvement. La table sert à construire puis distribuer la structure creuse ; `VolumeAssembler` en conserve une référence. [Sparsité](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L363-L418), [référence conservée](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/assembly/incompressible_chns_assemblers.h#L100-L120).

Le code propose deux voies de contrôle : assembler le Jacobien par différences finies, ou comparer le Jacobien analytique à cette approximation. Elles sont repérées, **non exécutées**. Un test pertinent après changement de forme doit tenir compte des choix de linéarisation, notamment τ gelé. [Points d'entrée](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L436-L460), [comparaison](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L503-L513).

## À vérifier dans une session avec build

Commencer par une configuration CHNS fixe sans stabilisation, puis une configuration stabilisée ; contrôler Jacobien et convergence MMS avant d'élargir à ALE et MPI. Les dossiers `tests/incompressible_chns` et `tests/incompressible_chns_ale` sont présents dans l'arbre Git ; leurs sorties existantes ne sont pas un résultat de cette session.

