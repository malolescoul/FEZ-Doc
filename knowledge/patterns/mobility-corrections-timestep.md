# Du modèle de mobilité au flux corrigé et au pas de temps

**Référence analysée : `cc8dace141900b82e5790fa878e39d9c54898784`.** Lecture des fichiers et patches ; tests présents décrits ci-dessous, non exécutés. Cette page complète [les modèles CHNS](../features/chns-models-pre-amr.md) et doit être lue avant de changer une formule locale : sa valeur, ses dérivées, ses usages dans l'inertie et sa mesure temporelle appartiennent au même parcours.

## Un contrat de données commun

`MobilityEvaluation<dim>` renvoie quatre scalaires : `value`, `derivative_wrt_tracer`, `second_derivative_wrt_tracer`, `adaptive_sensitivity`. Le dernier représente la sensibilité au capteur \(a=u\cdot\nabla\phi\) pour les modèles qui l'utilisent. Un pointeur de fonction est sélectionné dans le constructeur du scratch ; la boucle quadrature n'effectue pas une grande sélection de modèle à chaque point. [Contrat et dispatch](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L575-L623), [sélection dans le scratch](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/scratch_data.cpp#L420-L447).

Les arguments ne sont pas interchangeables. Le limiteur de mobilité est indépendant du limiteur des propriétés ; après ce filtre, `select_mobility_tracer_argument` fournit le marqueur matériel m et ses deux dérivées au modèle dégénéré, mais φ et les dérivées identités aux modèles adaptatifs. Avec NLM, cela signifie \(M_{deg}(q)\), tandis que la restriction du modèle adaptatif 2 est \(\chi(\phi)\). [Sélection](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L587-L612), [application en quadrature](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/scratch_data.h#L1138-L1171).

## Les cinq lois finales, sans confondre les versions historiques

Dans le tableau, \(a=u\cdot\nabla\phi\), \(\widetilde\sigma=3\sigma/(2\sqrt2)\). Les n et δ de chaque variante sont des paramètres distincts. L'orthographe externe est bien **`adaptative_mobility`**, tandis que plusieurs symboles C++ emploient `adaptive`.

| Paramètre `mobility model` | Valeur M effectivement calculée | Paramètres et valeur par défaut | Dérivées / lecture du code |
|---|---|---|---|
| `constant` | \(M=M_0\) | `mobility=1` | Les trois autres membres valent zéro |
| `degenerate` | \(M=F(z)\), avec z=m après filtre | sous-section `degenerate mobility`, expression par défaut \((1-x^2)^2\), x=z | \(F'(z)z'\), \(F''(z)(z')^2+F'(z)z''\) |
| `adaptative_mobility` | \(\sqrt{(C_1a)^2+\delta_1^2}+2m_a\epsilon^2\vert \nabla\phi\vert ^2\), \(C_1=n_1\sqrt2\epsilon^3/\widetilde\sigma\) | `adaptive mobility n=10`, `m=0`, `delta=1e-12` | Retourne M, 0, 0, \((C_1a/M)C_1\) |
| `adaptative_mobility_2` | \(\sqrt{(C_2\chi(\phi)a)^2+\delta_2^2}\), \(C_2=n_2\sqrt2\epsilon^3/\widetilde\sigma\) | `adaptive mobility 2 n=1`, `delta=1e-12` | Dérivées explicites χ', χ'' et sensibilité \((raw/M)C_2\chi\) |
| `adaptative_mobility_3` | \(C_3\sqrt{\vert u\vert ^2+\delta_3^2}\), \(C_3=n_3\epsilon^2/\widetilde\sigma\) | `adaptive mobility 3 n=1`, `delta=1e-12` | Les trois autres membres du record retournent zéro |

Sources : [constante/dégénérée](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L625-L656), [adaptative 1](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L659-L678), [adaptatives 2/3](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L729-L775), [échelles C](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L815-L846), [paramètres complets](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/parameters.cpp#L1660-L1735).

Le modèle 2 restreint son capteur : χ=1 pour \(\vert \phi\vert \le0.5\), χ=0 pour \(\vert \phi\vert \ge0.9\). Entre les deux, avec \(t=(\phi^2-0.25)/(0.81-0.25)\), \(\chi=1-(6t^5-15t^4+10t^3)\). L'usage de φ² rend χ paire ; les raccords quintiques donnent des dérivées première et seconde nulles aux extrémités. **M vaut δ dans les queues**, et non zéro, puisque la régularisation est appliquée après χ. [Poids final](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L680-L759).

Pour le modèle dégénéré, la magnitude est dans l'expression parsée : le `mobility` constant n'est pas implicitement un multiplicateur. Le helper évalue valeur, gradient et Hessienne de la fonction au point dont la première coordonnée vaut le marqueur. [Helpers parsés](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L540-L572). Les n/δ adaptatifs, σ et ε sont contrôlés strictement positifs ; le coefficient additionnel m est déclaré sans borne de signe. Le calcul du critère temporel vérifie M finie et non négative en chaque point. [Gardes de paramètres](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/parameters.cpp#L1860-L1907), [garde de réduction Mmax](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/incompressible_chns_solver.cpp#L299-L310).

**Portée du record de dérivées.** Le tableau reproduit ce que renvoient les helpers, sans prétendre que tout coefficient optionnel bénéficie d'une différentiation exacte. En particulier le modèle 1 renvoie sa sensibilité avec la valeur totale M au dénominateur, et le modèle 3 renvoie zéro malgré sa dépendance en u. Les usages lisibles dans l'assembleur passent par ces champs. Avant de modifier m ou d'exiger un Newton entièrement consistant pour le modèle 3, une reproduction ciblée de Jacobienne serait nécessaire ; aucune qualification de bug n'est faite ici. [Sensibilités retournées](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L659-L775), [injection dans δM](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/assembly/incompressible_chns_assemblers.cpp#L531-L563).

### La généalogie du modèle 2 explique pourquoi le titre d'un commit ne suffit pas

| Version | Formule / décision observée dans le patch | État à cc8dace |
|---|---|---|
| [0571b9a](https://github.com/arthurbawin/fez/commit/0571b9a8fad2b473bd2cec2f6e5c6545f56eb854) | \(M=n_2(2ε^4/\widetildeσ)\vert ∇φ\vert ^2\sqrt{\vert u\vert ^2+δ_2^2}\) | Remplacée |
| [a101eab](https://github.com/arthurbawin/fez/commit/a101eab4d59fb63e9ecca87eeccac8702ea126b2) | Passe au capteur \(u·∇φ\), coefficient \(\sqrt2ε³/\widetildeσ\), poids de queues W ; W annule la décroissance tanh entre 0.9 et 0.999, raccords C² et plateau borné | Le capteur et le contrat de dérivées persistent ; le poids de queues ne persiste pas |
| [cfaec11](https://github.com/arthurbawin/fez/commit/cfaec11e1efe4b94fa15111249f6496f3ce8872d) | Remplace W par χ : cœur 0.5, extinction 0.9 ; réécrit description et tests | C'est la loi finale du tableau ci-dessus |

Les seuils 0.9 et 0.999 ne désignent donc pas une extension active du modèle 2 final. Le niveau 0.999 existe encore ailleurs, dans les régularisations de correction de profil ; ce sont deux mécanismes différents.

## Parcours en assemblage : M atteint plusieurs équations

1. `reinit_cahn_hilliard_cell` lit φ, μ et leurs gradients sur le mapping courant, reconstruit m/m'/m'' et les propriétés.
2. L'évaluateur reçoit **u physique** et ∇φ mesuré sur le maillage mobile. Il produit M et les informations de variation.
3. Sans correction, le flux de phase est \(K_\phi=M∇μ\) ; la ligne φ reçoit \(\nabla w_\phi·K_\phi\).
4. Pour Abels/NLM, le scratch alimente aussi l'inertie diffusive \((\rho_1-\rho_0)(∇u)K_\phi/2\). Ding–Horriche ignore cette contribution.
5. Les colonnes u/φ/μ/x emploient les variations pertinentes de M, gradients et mesure ; la mobilité dégénérée intervient également dans le résidu fort SUPG et les sources MMS.

Sources : [scratch](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/scratch_data.h#L1033-L1202), [résidu modèle et phase](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/assembly/incompressible_chns_assemblers.cpp#L122-L238), [variation de flux](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/assembly/incompressible_chns_assemblers.cpp#L531-L563), [source MMS](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/incompressible_chns_solver.cpp#L325-L513).

La distinction ALE est volontaire : **mobilité → u**, **advection et τ → u−ẋ**. Une variation nodale de position laisse u nodal constant mais donne \(\delta∇φ=-G^T∇φ\), donc \(\delta M=s_a\,u·\delta∇φ\) pour les capteurs concernés. Remplacer u par u−ẋ dans une seule de ces routines modifierait la loi physique et romprait l'accord entre solveur, MMS, sortie et critère temporel. [Commentaire et variation x](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/assembly/incompressible_chns_assemblers.cpp#L676-L709), [τ sur vitesse relative](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/scratch_data.h#L1200-L1251).

Les mobilités 1 et 2 restent incompatibles avec tracer SUPG dans cette référence ; le développement ALE a levé l'interdiction de maillage mobile, pas celle de tracer SUPG. [Patch ALE](https://github.com/arthurbawin/fez/commit/e6ff32bf737dc0fc657829fca4ee06d3d95810ca), [garde finale](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/assembly/incompressible_chns_assemblers.h#L390-L404).

## Correction de profil et projection du flux

`interface profile correction=none|profile|profile_flux` choisit un **flux commun** aux équations de phase et d'inertie. Seul Abels standard est accepté, avec tracer SUPG désactivé. La force s'appelle `profile correction strength`, vaut 0.3 par défaut, est bornée dans [0,1] et doit être strictement positive dans un mode actif. σ et ε doivent être positifs. [Parsing](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/parameters.cpp#L1665-L1679), [validation](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/parameters.cpp#L1844-L1907), [garde de modèle](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L236-L249).

Pour décrire exactement le calcul, posons \(g=∇φ\), \(h=∇μ\), \(q_e=(1-φ²)/(\sqrt2ε)\). Le code emploie deux activations C² :
\(A=A(φ)\), transition de \(1-φ²\) entre \(0.25s_t\) et \(0.5s_t\), et \(B=B(\vert g\vert )\), mêmes seuils multipliés par \(1/(\sqrt2ε)\), avec \(s_t=1-0.999²\). A s'annule dans les phases pures et pour les dépassements \(\vert φ\vert >1\). B évite de construire une normale unitaire sur un gradient non résolu. [Activations](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L10-L87).

Le correcteur de profil est
\[
P=A\left(1-\frac{\sqrt{1+\beta^2}\,q_e}
{\sqrt{|g|^2+\beta^2q_e^2}}\right)g,\qquad \beta=0.05.
\]
Il est nul pour un profil tanh à l'équilibre \(\vert g\vert =q_e\), y compris avec cette régularisation relative. La normale de projection, distincte, est \(n_\delta=AB\,g/\vert g\vert \) dans la zone activée, et zéro sinon. [Correcteur P](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L90-L154), [normale](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L156-L188).

| Mode | Flux positif \(K_\phi=-J_\phi\) | Conséquence de lecture |
|---|---|---|
| none | \(M h\) | Retour direct de l'expression historique |
| profile | \(M h+\kappa P\) | Ajuste le profil sans projeter h |
| profile_flux | \(M[h-n_\delta(n_\delta·h)]+\kappa P\) | Retire la composante normale de diffusion là où les activations sont pleines ; atténuation pondérée dans leurs transitions |
| Tous modes actifs | \(\kappa=\alpha_{PC}\,2M\widetildeσ/ε\) | L'échelle suit **M locale**, pas le paramètre constant `mobility` |

Source : [construction du flux](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L224-L273). La projection est tangentielle exacte quand \(\vert n_\delta\vert =1\) ; avec une normale pondérée plus courte, ce n'est pas une projection orthogonale idempotente. Dans les phases pures et dépassements, \(P=0,n_\delta=0\), donc le flux revient à \(M∇μ\).

La variation de K contient \(\delta M\,h_{corr}+M\,\delta h_{corr}+\delta\kappa\,P+\kappa\,\delta P\). Elle dérive A, B et la direction de normale, sans construire explicitement le tenseur \(I-n_\delta\otimes n_\delta\). Le scratch calcule le même K pour la ligne φ et l'inertie ; l'assembleur injecte ses variations u/φ/μ et x. [Dérivée directionnelle](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L276-L356), [réutilisation](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/scratch_data.h#L1180-L1198), [variation ALE](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/assembly/incompressible_chns_assemblers.cpp#L686-L709).

### Les révisions changent le comportement, pas seulement les noms

| Commit | Modification effective | Résultat conservé |
|---|---|---|
| [96ea49a](https://github.com/arthurbawin/fez/commit/96ea49a422b724d3df1778feddac31716614c087) | Introduit profil et flux avec une normale régularisée par δ absolu, flux commun, gardes Abels et SUPG | Architecture commune et gardes |
| [9d885ba](https://github.com/arthurbawin/fez/commit/9d885bab795c3ef6c0d77973948338acc7ea5b2f) | Remplace cette normale pour le profil par une régularisation relative q ; ajoute activations et normale unitaire pondérée pour le flux | Préservation de l'équilibre tanh, extinction dans les phases pures, séparation P/n |
| [3353420](https://github.com/arthurbawin/fez/commit/3353420c2331dbbecdb240a7b8dd77e7dec7fff6) | Découple κ de M locale via \(M_{PC}=ε^p\), introduit `profile correction mobility exponent`, retire δκ | Étape intermédiaire entièrement dépassée |
| [74d9e06](https://github.com/arthurbawin/fez/commit/74d9e06ed2fcff3d614600a8029d5b3642cf1156) | Rétablit κ(M) et δκ(δM), retire l'exposant du parsing | Comportement final lu à cc8dace |

Ainsi, une ancienne configuration avec `profile correction mobility exponent` décrit un état antérieur ; ce paramètre n'existe plus dans la référence étudiée.

## Le critère temporel fondé sur la mobilité

Le critère n'est calculé que si `adaptation strategy=adaptive mobility`. Le solveur relit la solution courante sur le mapping mobile, réutilise l'évaluateur de mobilité, trouve le maximum sur les points de quadrature des cellules possédées, puis fait un **maximum MPI**. Il forme
\[
N_M=\Delta t\,\widetilde\sigma M_{\max}/ε^3
\]
et le transmet à `TimeHandler::set_max_adaptive_mobility_number`. Ce n'est ni une moyenne nodale, ni un CFL de maillage, ni le diagnostic \(D_\phi\) de la sortie CSV. [Réduction complète](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/incompressible_chns_solver.cpp#L239-L322), [formule et gardes](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/include/cahn_hilliard.h#L849-L871).

| Paramètre | Défaut / domaine | Usage |
|---|---|---|
| `target adaptive mobility number` | 1 ; \(0<N_\star\le1\) | Cible de \(N_M\) |
| `reject timestep with large adaptive mobility` | true | Autorise le rejet du pas convergé |
| `adaptive mobility ratio to reject` | 1 ; ratio ≥1 | Rejet si \(N_M/N_\star\) dépasse ce facteur |
| Bornes de temps et ratios généraux | Paramètres de l'adaptation temporelle | Appliqués par `clamp_timestep` après la prédiction |

[Déclaration](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/parameters.cpp#L1484-L1501), [validation cible](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/parameters.cpp#L1594-L1602).

La boucle d'acceptation suit cet ordre : échec Newton traité ; stationnaire ou adaptation absente acceptés ; démarrage BDF accepté avec avertissement si le seuil est dépassé ; sinon application du critère choisi. Sur succès, le pas prédit est \(\Delta t\,N_\star/N_M\), ou le maximum autorisé lorsque \(N_M=0\). Après rejet pour mobilité, il est multiplié en plus par 0.9 ; après échec non linéaire, il est divisé par deux. Les bornes et ratios restent appliqués. [Acceptation](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/time_handler.cpp#L311-L455), [prédiction](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/time_handler.cpp#L575-L650).

Le rejet restaure `present_solution=previous_solutions[0]`, recule le temps et les compteurs, et marque `rolledback_step`. Au-delà de cinq rejets consécutifs permis, il interrompt par exception. Les options d'adaptation sont une **stratégie sélectionnée** ; le code montré ne calcule pas automatiquement \(\min(\Delta t_{CFL},\Delta t_M,\Delta t_{BDF})\). [Rollback](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/time_handler.cpp#L457-L491), [branches de stratégie](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/src/time_handler.cpp#L575-L600).

## Tests lus et expériences utiles avant une extension

| Test présent | Observations directement lisibles | Ce qu'il ne faut pas en déduire |
|---|---|---|
| [profile_correction.cc](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/tests/unit_tests/profile_correction.cc#L24-L176) | Équilibre du profil ; gradient nul ; projection ; différence finie centrée du flux complet avec variation de M | Pas une mesure de conservation globale après transport ALE complet |
| [Gardes et modes](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/tests/unit_tests/profile_correction.cc#L179-L338) | Défauts, incompatibilité modèle/SUPG ; queues résolues ; gradients non résolus ; phases pures et dépassements | Pas une validation de NLM avec correction : c'est précisément refusé |
| [time_handler_adaptive_mobility.cc](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/tests/unit_tests/time_handler_adaptive_mobility.cc#L54-L141) | Rejet de 0.2 à 0.09, restauration de solution, acceptation du retry, démarrage BDF2 non rejeté | Le test construit un nombre de mobilité ; il ne remplace pas le calcul spatial Mmax |
| [Échelles et poids χ](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/tests/unit_tests/time_handler_adaptive_mobility.cc#L143-L312) | Coefficients des trois variantes, restriction paire, dérivées FD, sélection φ contre q | Pas une Jacobienne complète du modèle 3 en u |
| [adaptive_mobility_timestep.prm](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/tests/incompressible_chns/adaptive_mobility_timestep.prm#L17-L61) | Intégration solveur avec modèle 3, cible 0.1, rejet explicitement désactivé | Ne couvre pas la branche de rollback à lui seul |
| [Jacobian ALE enlarged modèle 2](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/tests/incompressible_chns_ale_enlarged/jacobian_matrix_adaptative_mobility_2.prm#L27-L102) | FD activée, seuils 1e−4, φ initial `0.8+0.1995*x`, forçage ψ actif | Le commentaire annonce cœur/transition/coupure ; l'étendue réelle doit se lire avec le domaine |
| [Jacobian ALE enlarged modèle 1](https://github.com/arthurbawin/fez/blob/cc8dace141900b82e5790fa878e39d9c54898784/tests/incompressible_chns_ale_enlarged/jacobian_matrix_adaptative_mobility.prm#L29-L84) | Loi adaptative 1, ALE, enlarged, comparaison FD | Le paramètre additionnel m n'y est pas défini : sa valeur par défaut est zéro |

Pour étendre une loi, le parcours à examiner est : paramètres → sélection de l'argument → valeur et sensibilités → scratch → colonnes Jacobienne → source MMS → post-traitement et sondes → Mmax → acceptation du temps. Les expériences de lecture C++ associées sont dans [le cahier d'exercices](../../pedagogie/lecture-cpp-pre-amr.md). Cette liste indique où une dépendance se propage ; elle ne transforme pas les tests présents en tests exécutés.

