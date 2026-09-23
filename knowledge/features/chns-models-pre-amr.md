# Physique CHNS avant la nouvelle adaptation h

**État de référence : `cc8dace141900b82e5790fa878e39d9c54898784`.** Cette page décrit ce que cet instantané assemble réellement. « Pré-AMR » signifie avant le nouveau chantier CHNS h-adaptatif ; cela ne signifie pas que l'arbre ne contient aucun ancien code d'adaptation. Les sources et les patches ont été lus ; aucun solveur ni test C++ n'a été exécuté pour cette analyse.

Le parcours général et le passage du présolveur au solveur sont décrits dans [le workflow](workflow-pre-amr.md). Les lois de mobilité, leurs révisions et le contrôle du temps sont détaillés dans [mobilité, correction, pas de temps](../patterns/mobility-corrections-timestep.md).

## Trois axes de configuration indépendants

| Axe | Variantes à cette référence | Ce qui change |
|---|---|---|
| Solveur / géométrie | `CHNSSolver<dim,false>`, `<dim,true>`, `<dim,true,true>` | CHNS fixe ; CHNS avec position de maillage ALE ; ALE avec marqueur élargi ψ |
| Modèle physique | `abels`, `ding_horriche`, `abels_nlm` | Énergie/potentiel, force capillaire, inertie diffusive et variable matérielle transportée |
| Mobilité / correction | constante, dégénérée, adaptatives 1/2/3 ; `none/profile/profile_flux` | Flux diffusif et ses dépendances, avec des gardes de compatibilité |

L'ordre des composantes est **u, p, x si ALE, φ, μ, ψ si enlarged**. ψ est ajouté après μ, et l'option enlarged est statiquement limitée à ALE. Ce n'est ni le remplacement de φ, ni un raffinement h : φ demeure l'inconnue de phase physique. [Ordre des composantes](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/components_ordering.h#L399-L459), [garde enlarged](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/assembly/incompressible_chns_assemblers.h#L375-L386), [instanciations](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/incompressible_chns_solver.cpp#L1923-L1929).

## Les équations : partir du résidu assemblé

Notation : \(\widetilde\sigma=3\sigma/(2\sqrt2)\), \(m=m(\phi)\), \(v=u-\dot x\) en ALE et \(v=u\) sur maillage fixe. En ignorant ici les sources manufacturées et les termes de bord, la lecture des lignes φ et μ donne :

\[
D_t^{ALE}m+v\cdot\nabla m-\nabla\cdot K_\phi=0,\qquad
m'(\phi)\mu=A\,\phi(\phi^2-1)-B\,\Delta\phi .
\]

Sans correction, \(K_\phi=M\nabla\mu\). La ligne test du traceur contient \(w_\phi(D_tm+v\cdot\nabla m)+\nabla w_\phi\cdot K_\phi\). Le vecteur local stocke **−R** et la matrice **dR** : ce signe est essentiel pour comparer une formule physique à `local_rhs -= ...`. [Assemblage volume, lignes φ/μ](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/assembly/incompressible_chns_assemblers.cpp#L122-L246).

| Modèle | Marqueur transporté et matériaux | \(A;B\) | Terme capillaire dans le résidu momentum | Inertie diffusive | Pression reconstruite |
|---|---|---|---|---|---|
| Abels | \(m=\phi\) ; propriétés affines en φ filtré si limiteur actif | \(\widetilde\sigma/\epsilon;\widetilde\sigma\epsilon\) | \(+\phi\nabla\mu\) | Oui | \(p+\phi\mu\), `pressure_abels` |
| Ding–Horriche | \(m=\phi\) | \(1;\epsilon^2\) | \(-\gamma\mu\nabla\phi,\ \gamma=\widetilde\sigma/\epsilon\) | Non | \(p\), `pressure_hat` |
| Abels NLM | \(m=q=\tanh(k\phi)/\tanh k\) ; propriétés affines en q | mêmes A, B qu'Abels | \(+q\nabla\mu_q\) | Oui | \(p+q\mu_q\), `pressure_sharp` |

Ces signes sont ceux du résidu, pas d'une force recopiée isolément au second membre. La différence Ding–Horriche est une branche `if constexpr` du masque d'assemblage : coefficients du potentiel, capillarité et inertie changent ensemble. NLM conserve la structure Abels et sélectionne au démarrage des pointeurs de fonctions \(m,m',m''\). [Coefficients et modèles](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L359-L431), [choix de l'assembleur](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/assembly/incompressible_chns_assemblers.h#L405-L455), [forces](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/assembly/incompressible_chns_assemblers.cpp#L122-L168).

Le terme `diffusive_flux[q]` du scratch est déjà la contribution d'inertie \((\nabla u)J\), avec \(J=(\rho_1-\rho_0)K_\phi/2\), et non seulement le vecteur de flux \(J\). La même expression \(K_\phi\) est utilisée dans la diffusion de phase et, quand une correction est active, dans cette inertie Abels. Cela évite de lire la correction comme une source ajoutée uniquement à φ. [Calcul du flux et de l'inertie](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/scratch_data.h#L1172-L1198).

### Pourquoi NLM garde φ et μ comme inconnues

Pour `abels_nlm`, μ est conjugué à q : \(\mu=\mu_q\), et \(\mu_\phi=m'(\phi)\mu_q\). Le programme **multiplie** donc μ par \(m'\) dans la ligne potentiel ; il n'y divise pas par une dérivée qui devient petite dans les phases pures. φ reste une inconnue, q est reconstruit. Le BDF est appliqué à **m des états présents et passés**, pas à \(m'(\phi)\,\mathrm{BDF}(\phi)\), deux opérations généralement différentes en discret. [Rationale dans les helpers](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L874-L887), [BDF sur m](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/scratch_data.h#L1084-L1112).

Il faut distinguer trois usages du traceur : m brut pour transport/capillarité ; m du traceur filtré pour densité et viscosité ; argument propre à la mobilité après son limiteur indépendant. La mobilité dégénérée prend m (donc q en NLM), tandis que les mobilités adaptatives prennent φ. [Scratch et règle de chaîne](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/scratch_data.h#L1114-L1171), [sélection de l'argument](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L587-L612).

## ψ : un problème de Helmholtz couplé à la géométrie

Avec \(L=\texttt{psi interface width factor}\,\epsilon\), le résidu effectivement codé est

\[
R_{\psi,i}=\int_{\Omega(x)}
w_i\{\psi-\phi+s_\psi-c_\mu(1-\phi^2)^2\mu\}
+L^2\nabla w_i\cdot\nabla\psi,
\quad c_\mu=\alpha_\mu L^2/(\epsilon\widetilde\sigma).
\]

Les valeurs par défaut sont facteur de largeur 1 et \(\alpha_\mu=0\). Sans source et sans correction μ, cela donne \(\psi-L^2\Delta\psi=\phi\) : un lissage spatial instantané de φ, sans équation temporelle propre. ψ fournit un marqueur moins étroit pour déplacer le maillage autour de l'interface ; les termes de CHNS physiques continuent d'utiliser φ ou m(φ). [Résidu exact et préfacteur](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/assembly/incompressible_chns_assemblers.h#L82-L142), [paramètres](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/parameters.cpp#L1774-L1801).

La Jacobienne ajoute les blocs ψ←ψ, ψ←φ, ψ←μ et ψ←x. Pour la variation de x, les valeurs nodales sont gardées, mais les gradients varient comme \(-G^T\nabla f\) et la mesure comme \(\operatorname{tr}(G)JxW\). Ces dérivées sont nécessaires même si ψ n'est qu'un « marqueur de maillage » : son opérateur est intégré sur la géométrie déformée. [Jacobienne ψ](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/assembly/incompressible_chns_assemblers.h#L149-L233).

**Limite documentaire localisée.** Le commentaire d'en-tête écrit \(\phi-\text{mu\_correction}\), alors que les instructions du résidu ci-dessus placent \(-\text{mu\_correction}\) à gauche, donc un signe plus à droite sans source. Le préfacteur reste la forme Abels, sans branche Ding–Horriche dans cette fonction ; un commentaire y annonce encore une variante future. La page conserve l'expression exécutable sans conclure à un défaut numérique non reproduit. [Commentaire et implémentation côte à côte](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/assembly/incompressible_chns_assemblers.h#L65-L142).

Le forçage élargi fait intervenir le gradient de ψ et une transformation du marqueur par \(\operatorname{sign}(\psi)\vert \psi\vert ^q\), alors que le forçage de compression physique utilise φ. Les détails de normalisation des lobes et du présolveur sont dans [présolveur et géométrie](../patterns/presolver-cache-geometry.md). ψ n'est donc pas une seconde fraction de phase conservée, et la mobilité n'est pas calculée à partir de ψ.

## Stabilisation : résidu fort, tests modifiés, géométrie ALE

`enable supg` active SUPG vitesse et PSPG pression ; `enable tracer supg` active séparément SUPG sur le transport de m. Le résidu fort momentum est conservé en unités de force : \(\rho(D_tu+\nabla u\,v-f)+(\nabla u)J+F_c+\nabla p-\eta(\Delta u+\nabla\nabla\cdot u)-2\eta_\phi D(u)\nabla\phi\), en tenant compte du modèle. Les opérateurs de test associés sont \(v\cdot\nabla w_u\) et \(\nabla w_p/\rho\). Le résidu fort de phase inclut \(M\Delta\mu+M_\phi\nabla\phi\cdot\nabla\mu\) pour mobilité dépendant du marqueur. [Expressions assemblées](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/assembly/incompressible_chns_assemblers.cpp#L154-L231).

Le paramètre \(\tau\) combine temps, convection et diffusion :
\[
\tau^{-2}=\Delta t^{-2}+(2|v|p/h)^2+
9(4Dp^2/h^2)^2.
\]
Le terme temporel est omis en stationnaire. En 2D, h est directionnel ; en 3D cette implémentation utilise le diamètre de cellule. Le scratch fournit \(D=\eta/\rho\) pour la vitesse et le scalaire membre `mobility` (paramètre constant) pour τ du traceur. Cette dernière expression n'est pas `mobility_values[q]` : ne pas supposer une diffusion chimique locale automatiquement recalculée dans τ. [Formule effective de τ](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/stabilization_tools.h#L110-L189), [appels vitesse et traceur](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/scratch_data.h#L1200-L1251).

La Jacobienne fige τ, tout en dérivant le résidu fort et l'opérateur de test. Les tests Jacobienne SUPG expliquent ainsi pourquoi une différence analytique/finie n'est pas attendue à zéro et emploient des tolérances explicites ; ce n'est pas une preuve automatique d'erreur de Jacobienne. Les blocs ALE dérivent aussi gradients, Hessiennes, mesure et vitesse convective. [τ figé](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/assembly/incompressible_chns_assemblers.cpp#L617-L674), [variation de géométrie](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/assembly/incompressible_chns_assemblers.cpp#L676-L820), [explication du test NLM](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/tests/incompressible_chns/jacobian_matrix_supg_abels_nlm.prm#L21-L50).

| Combinaison | Garde réellement présente |
|---|---|
| Abels, Ding–Horriche, NLM + constante/dégénérée | Pas d'interdiction de tracer SUPG dans la sélection |
| Adaptative 1 ou 2 | Tracer SUPG interdit ; ALE permis |
| Adaptative 3 | Pas bloquée par cette garde spécifique |
| `profile` ou `profile_flux` | Seulement `abels`, tracer SUPG désactivé ; NLM est également refusé |
| Enlarged sans ALE | Refus à la compilation |

Ce tableau décrit la sélection et ses gardes, pas une validation numérique exhaustive du produit cartésien des options. [Gardes centralisées](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/assembly/incompressible_chns_assemblers.h#L375-L404), [garde corrections](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L236-L249).

## Pression et diagnostics : comparer les bonnes quantités

La pression résolue p n'a pas le même sens de reconstruction dans les trois modèles. La sortie continue nodale calcule les quantités du tableau de modèles ; NLM expose aussi `q` et `potential_phi=m'μ`. Le degré de l'espace de sortie est le maximum de 1 et des degrés p/φ/μ. Cette reconstruction ponctuelle évite la marche en escalier d'une moyenne DG0. [Sortie continue](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/incompressible_chns_solver.cpp#L995-L1085).

La table d'échelles de temps est un **diagnostic Abels à mobilité constante de référence** : \(D_\phi=2\,\texttt{chp.mobility}\,\widetilde\sigma/\epsilon\), \(V=\int(1-\phi)/2\), rayon équivalent disque/sphère, \(U=\max\vert u\vert \), \(U_\sigma=\sigma/\eta_{ref}\). Elle produit notamment \(R/U\), \(R^2/D_\phi\), \(\epsilon^2/D_\phi\), \(\eta R/\sigma\), \(\sqrt{\rho R^3/\sigma}\), Pe, Cn, Ca, Re et \(S=\sqrt{M\eta}/\epsilon\). Elle ne commute pas vers \(M_{\max}\), ni vers une fraction basée sur q en NLM. Pour une mobilité adaptative, le critère temporel dédié décrit dans l'autre page est un calcul distinct. [Calcul et export](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/incompressible_chns_solver.cpp#L1777-L1919).

Le fichier porte l'extension `.csv`, mais `TableHandler::write_text` y écrit une table **séparée par espaces**. Le commentaire l'indique explicitement. Le code prend les propriétés de `fluids[0]` comme référence, sans que cela suffise à identifier universellement une goutte : le choix dépend de la convention de phase de la configuration. [Référence physique](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/incompressible_chns_solver.cpp#L1788-L1802), [format](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/incompressible_chns_solver.cpp#L1913-L1919).

## Douze jalons à relire dans les patches

Ces jalons ont été rapprochés du code final ; ils ne sont pas une simple liste de titres de commits.

| Étape | Introduction / révisions | Ce qui persiste à la référence |
|---|---|---|
| 1. Stabilisation | [3fc7512](https://github.com/arthurbawin/fez/commit/3fc75123bcac5bce6430b7bc865e534a472b63cc), [238e0af](https://github.com/arthurbawin/fez/commit/238e0afeb84181c30be57484d5cc3a259782f56e), [558a30e](https://github.com/arthurbawin/fez/commit/558a30efd84acd37148fa853d6fc0e533d7d7fb2) | SUPG/PSPG puis résidu en force et bloc ALE/Hessiennes ; l'interdiction initiale de stabiliser ALE disparaît |
| 2. ψ enlarged | [d0090cc](https://github.com/arthurbawin/fez/commit/d0090cc234fa78b0b720c2cd9c62ad9b4b45a178), [157c441](https://github.com/arthurbawin/fez/commit/157c4412a7a7d2c66e3f62aede5d4fe544ac9f98), [8a59267](https://github.com/arthurbawin/fez/commit/8a5926785bb87f770b9b641d5b1fc6c58e36e253) | Composante supplémentaire → Helmholtz → ψ pilote le forçage et ajoute le bloc x←ψ |
| 3. Diagnostic physique | [7804d3c](https://github.com/arthurbawin/fez/commit/7804d3cc1b2f0532ff3f7577b7273a8c0429b28a) | Pression Abels nodale et table d'échelles ; les reconstructions de pression sont ensuite adaptées aux autres modèles |
| 4. Mobilité dégénérée | [b5cf71d](https://github.com/arthurbawin/fez/commit/b5cf71ddebbed225631a071ed6c24758ea430dfd), [6c555a0](https://github.com/arthurbawin/fez/commit/6c555a0ccc1a7721a0206134674391612a7a61ca), [5a180ff](https://github.com/arthurbawin/fez/commit/5a180ff8919f948f69d67621e9fb6f4b62187d14) | Fonction parsée et deux dérivées, diffusion/SUPG/inertie/MMS cohérents, tests dédiés ; parsing du modèle constant rectifié |
| 5. Ding–Horriche | [50096a2](https://github.com/arthurbawin/fez/commit/50096a2f72370286561ebeea47ecca231ed62bff), [afe2c57](https://github.com/arthurbawin/fez/commit/afe2c57688b00be848c331e9739966625c71119e) | Masque d'assemblage, coefficients 1/ε², force −γμ∇φ et retrait de l'inertie diffusive ; MMS et FD |
| 6. Abels NLM | [438fb45](https://github.com/arthurbawin/fez/commit/438fb453383bac7444d53843c5d5fff9f0ca9085), [213f11b](https://github.com/arthurbawin/fez/commit/213f11b9347d5c63d04de1097c8089f04fe3f338), [714d559](https://github.com/arthurbawin/fez/commit/714d55984b3286e6e0afa7d7520fa81948c07e8b) | Abstraction m/m'/m'', BDF sur m, μq ; suppression ultérieure des variables dφ/dt devenues inutilisées |
| 7. Adaptative 1 et ALE | [5a5a98e](https://github.com/arthurbawin/fez/commit/5a5a98e8a016f5d503cfa943c1ce4e8bd6db49da), [e6ff32b](https://github.com/arthurbawin/fez/commit/e6ff32bf737dc0fc657829fca4ee06d3d95810ca), [28f26ad](https://github.com/arthurbawin/fez/commit/28f26adfd976ed172876aa4a2f771c747ce9ee4d) | Structure unifiée MobilityEvaluation ; variation géométrique autorisant ALE ; terme additionnel en \(\vert ∇φ\vert ²\) |
| 8. Adaptatives 2/3 | [0571b9a](https://github.com/arthurbawin/fez/commit/0571b9a8fad2b473bd2cec2f6e5c6545f56eb854), [5f58194](https://github.com/arthurbawin/fez/commit/5f58194c708077a2697e6eaff777d494415a850c), [179630a](https://github.com/arthurbawin/fez/commit/179630afa97e542988f47dbebb0fc80503b44fbc) | Deux nouvelles lois ; sortie de mobilité corrigée pour employer le coefficient et δ du modèle sélectionné |
| 9. Temps adaptatif | [d4e8bb4](https://github.com/arthurbawin/fez/commit/d4e8bb48bd99e944fd76d03f223f37b7946a5946) | Maximum quadrature/MPI de M, nombre \(Δt\widetildeσM_{max}/ε³\), acceptation/rejet et prédiction |
| 10. Mobilité 2 révisée | [a101eab](https://github.com/arthurbawin/fez/commit/a101eab4d59fb63e9ecca87eeccac8702ea126b2), [cfaec11](https://github.com/arthurbawin/fez/commit/cfaec11e1efe4b94fa15111249f6496f3ce8872d) | L'extension des queues est remplacée par une restriction au cœur ; la formule initiale \(\vert ∇φ\vert ²\\vert u\\vert \) n'est plus la formule finale |
| 11. Corrections d'interface | [96ea49a](https://github.com/arthurbawin/fez/commit/96ea49a422b724d3df1778feddac31716614c087), [9d885ba](https://github.com/arthurbawin/fez/commit/9d885bab795c3ef6c0d77973948338acc7ea5b2f) | Flux commun phase/inertie ; puis activations quintiques, normale pondérée et régularisation préservant l'équilibre tanh |
| 12. Échelle de correction | [3353420](https://github.com/arthurbawin/fez/commit/3353420c2331dbbecdb240a7b8dd77e7dec7fff6), [74d9e06](https://github.com/arthurbawin/fez/commit/74d9e06ed2fcff3d614600a8029d5b3642cf1156) | La tentative \(M_{PC}=ε^p\) est retirée ; κ et dκ dépendent à nouveau de la mobilité locale |

## Lire les tests avec leur portée

| Source présente | Ce qu'elle couvre explicitement | Limite de conclusion |
|---|---|---|
| [MMS mobilité dégénérée](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/tests/incompressible_chns/mms_chns_2d_spacetime_degenerate_mobility.prm#L1-L85) | Mobilité parsée, convergence spatio-temporelle prévue par la configuration | Présence du test, pas réussite constatée ici |
| [Jacobian SUPG Ding–Horriche](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/tests/incompressible_chns/jacobian_matrix_supg_ding_horriche.prm#L21-L101) | Deux stabilisations et modèle DH, tolérance absolue 1e−1 expliquée par τ figé | Ne pas la comparer naïvement à une tolérance Galerkin non stabilisée |
| [Jacobian SUPG NLM](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/tests/incompressible_chns/jacobian_matrix_supg_abels_nlm.prm#L21-L102) | NLM à k=3, mobilité constante, SUPG/PSPG et tracer SUPG | Ne démontre pas toutes les lois de mobilité avec NLM |
| [MMS ALE enlarged](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/tests/incompressible_chns_ale_enlarged/mms_chns_ale_enlarged_2d_spacetime.prm#L1-L90) | Système avec ψ et géométrie mobile | Ce test ne valide pas à lui seul la correction μ opt-in |
| [Jacobian adaptative 2 enlarged](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/tests/incompressible_chns_ale_enlarged/jacobian_matrix_adaptative_mobility_2.prm#L27-L102) | Traceur initial traversant transition/coupure χ et gradient non nul | Lire la configuration finale, pas l'ancien titre « tail » |

La condition de contact statique ajoute un flux de bord à la ligne μ, \(n\cdot∇φ=-\cos θ(1-φ²)/(\sqrt2ε)\), avec dérivées φ et géométrie. Elle n'est pas une quatrième loi de mobilité ni une reconstruction ψ. Son parcours de configuration est traité dans le workflow. [Helpers contact](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L500-L537), [assembleur de bord](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/assembly/incompressible_chns_assemblers.cpp#L1245-L1333).

