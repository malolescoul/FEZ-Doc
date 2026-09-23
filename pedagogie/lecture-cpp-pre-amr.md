# Lire le C++ CHNS pré-AMR : trois exercices guidés

Ces exercices portent sur la référence **`cc8dace141900b82e5790fa878e39d9c54898784`**. Ils se font par lecture et calcul manuel ; aucun test ci-dessous n'est annoncé comme exécuté. Les fichiers `.prm` mentionnés sont les exemples et tests du dépôt, pas une reconstitution des réglages personnels de l'utilisateur.

## 1. Qui choisit le modèle : le compilateur ou le fichier de paramètres ?

**Objectif.** Distinguer `if constexpr`, masque de bits, sélection à l'exécution et pointeur de fonction. Expliquer pourquoi Ding–Horriche et NLM n'utilisent pas la même technique de sélection.

Lire [les flags et VolumeAssembler](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/assembly/incompressible_chns_assemblers.h#L29-L62), [setup_assemblers](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/assembly/incompressible_chns_assemblers.h#L369-L455), [dispatch de m](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L931-L1008) et [emploi du marqueur](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/assembly/incompressible_chns_assemblers.cpp#L111-L141).

Travail à faire :

1. Pour ALE enlarged, SUPG vitesse actif, tracer SUPG inactif et modèle Ding–Horriche, écrire les flags qui atteignent le type de `VolumeAssembler`.
2. Expliquer la fonction de `std::integral_constant<unsigned int,...>` et de `decltype(base_flags_constant)::value`.
3. Remplacer mentalement le modèle par NLM : quel flag disparaît ? Où est stockée l'alternative à l'identité \(m=\phi\) ?
4. Suivre une seule valeur de φ à travers m, m', la ligne potentiel et la reconstruction de pression. À aucun moment q ne devient-il un nouveau degré de liberté ?
5. Pourquoi BDF(m(φ)) n'est-il pas remplaçable sans réflexion par m'(φ)·BDF(φ) ?

**Réponse attendue.** Les flags de base comprennent `stabilization|moving_mesh|enlarged` ; le choix runtime DH instancie le type qui ajoute `ding_horriche`. `integral_constant` transporte une valeur dans un type, permettant de la réutiliser comme argument template constant. Avec NLM, le flag DH n'est pas ajouté : la structure des termes reste Abels, et des pointeurs vers les fonctions tanh/m'/m'' changent les valeurs. Le scratch les sélectionne une fois, puis la boucle quadrature les appelle. μ est μq en NLM ; la ligne potentiel contient m'μ, et la pression reconstruite p+mμ. q reste calculé depuis φ.

Le BDF de m utilise m(φ) de **chaque état historique** : pour une fonction non linéaire, appliquer m après une combinaison temporelle n'est pas équivalent à une dérivée locale multipliée par cette combinaison. [Sélection des fonctions](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/scratch_data.cpp#L440-L448), [BDF exact dans le scratch](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/scratch_data.h#L1084-L1112), [pression NLM](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/incompressible_chns_solver.cpp#L1067-L1080).

**Point de vigilance.** Une garde runtime comme l'interdiction « correction + tracer SUPG » est différente du `static_assert` enlarged ⇒ ALE. Lire l'une ne permet pas de conclure que toutes les autres combinaisons sont testées.

## 2. Une variation de mobilité doit traverser le profil et l'inertie

**Objectif.** Lire une dérivée directionnelle C++ comme une règle de chaîne, puis retrouver les appelants qui lui donnent ses variations.

Lire [le flux](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L224-L273), [sa variation](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L276-L356), [les colonnes de champs](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/assembly/incompressible_chns_assemblers.cpp#L531-L563) et [la colonne de géométrie](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/assembly/incompressible_chns_assemblers.cpp#L676-L709).

Travail à faire :

1. Écrire les quatre termes de δK dans le mode `profile`.
2. Garder φ, ∇φ et ∇μ fixes et ne faire varier que M. Quels termes restent ? Pourquoi la version intermédiaire indépendante de M n'aurait-elle pas donné la même réponse ?
3. Dans `profile_flux`, déplier `potential_gradient - normal*(normal*potential_gradient)`. Distinguer produit scalaire intérieur et multiplication scalaire-vecteur extérieure.
4. Suivre le `mobility_variation` passé à la fonction selon que la colonne j est u, φ ou μ.
5. Pour une colonne x, expliquer pourquoi `tracer_variation=0` peut coexister avec `tracer_gradient_variation != 0`.
6. Retrouver où le même K est réemployé dans le terme momentum. Le nom `diffusive_flux` contient-il seulement J ?

**Réponse attendue.** δK = δM·h_corr + M·δh_corr + δκ·P + κ·δP, avec κ = α·2Mσ̃/ε. À champs fixes : δK = δM·h_corr + (α·2δMσ̃/ε)·P. Le commit [3353420](https://github.com/arthurbawin/fez/commit/3353420c2331dbbecdb240a7b8dd77e7dec7fff6) supprimait ce deuxième terme en rendant κ indépendante de M ; [74d9e06](https://github.com/arthurbawin/fez/commit/74d9e06ed2fcff3d614600a8029d5b3642cf1156) le rétablit.

La colonne u donne la sensibilité du capteur fois δu·∇φ ; la colonne φ combine Mφδφ et la sensibilité fois u·∇δφ ; la colonne μ fournit ∇δμ au helper. En variation x, les valeurs FE nodales restent fixes mais le gradient sur la géométrie mobile varie comme −Gᵀ∇φ. Le scratch stocke déjà \((\rho_1-\rho_0)(∇u)K/2\) dans `diffusive_flux\). [Réemploi dans l'inertie](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/scratch_data.h#L1180-L1198).

**Expérience proposée, non exécutée.** Dans [le test unitaire existant](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/tests/unit_tests/profile_correction.cc#L87-L176), suivre le calcul centré K(z+hδz)−K(z−hδz), divisé par 2h. Repérer la variation explicite de mobilité, puis prédire quelle contribution disparaîtrait si δκ était oubliée. C'est une vérification de chaîne plus instructive qu'un test recopiant la formule du helper.

## 3. Le pas de temps est une décision avec retour d'état

**Objectif.** Relier réduction MPI, stratégie choisie, rejet et restauration de solution, sans confondre un diagnostic avec une loi d'adaptation.

Lire [Mmax](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/incompressible_chns_solver.cpp#L239-L322), [le nombre NM](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L849-L871), [acceptation/rollback](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/time_handler.cpp#L311-L492) et [prédiction](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/time_handler.cpp#L575-L650).

Cas manuel : pas courant 0.2, nombre NM=2, cible 1, ratio de rejet 1, rejet activé ; Newton a convergé, on est hors démarrage BDF et les bornes n'empêchent pas la réduction.

Travail à faire :

1. Décider acceptation ou rejet ; calculer le nouveau Δt.
2. Dire quelle solution remplace la solution rejetée et comment évoluent temps et indices.
3. Après retry, NM vaut 0.9 au pas 0.09 : calculer le prochain pas accepté.
4. Refaire la décision initiale pendant le démarrage BDF2.
5. Montrer pourquoi cette stratégie n'est pas automatiquement le minimum du CFL et d'une erreur BDF.
6. Expliquer pourquoi la table de sortie `D_phi` peut raconter autre chose que Mmax pour une mobilité variable.

**Réponse attendue.** Hors démarrage, ratio 2>1 : rejet. Le pas devient 0.9×0.2×1/2=0.09, puis la solution courante est restaurée depuis `previous_solutions[0]`, le temps recule de l'ancien pas et les compteurs reculent. Le retry accepté prédit 0.09×1/0.9=0.1. Pendant les pas de démarrage BDF, le chemin d'acceptation passe avant le rejet mobilité et émet un avertissement ; il faut suivre le code de démarrage pour la suite des pas, pas appliquer mécaniquement la prédiction hors démarrage.

L'enum de stratégie choisit une branche ; les bornes génériques interviennent après la prédiction. La sortie d'échelles utilise `chp.mobility` constant dans \(D_\phi=2Mσ̃/ε\), alors que l'adaptation réévalue M en quadrature et réduit un maximum MPI. [Test existant avec les nombres ci-dessus](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/tests/unit_tests/time_handler_adaptive_mobility.cc#L54-L96), [test BDF2](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/tests/unit_tests/time_handler_adaptive_mobility.cc#L98-L141), [diagnostic constant](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/incompressible_chns_solver.cpp#L1788-L1797).

Pour revenir au parcours complet : [workflow](../knowledge/features/workflow-pre-amr.md), [modèles physiques](../knowledge/features/chns-models-pre-amr.md), [mobilité et corrections](../knowledge/patterns/mobility-corrections-timestep.md).

