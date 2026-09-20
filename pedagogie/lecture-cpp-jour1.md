# Lecture C++ — jour 1 : suivre une contribution CHNS

Objectif : comprendre le chemin d'une donnée en lisant quelques lignes réelles. Révision étudiée : `master@ccf20caa0745cc2fe640f879d34acf2bf3855e6c`. Aucun exercice ne nécessite aujourd'hui de compiler FEZ.

## 1 — Est-ce que je modifie l'original ?

```cpp
auto &local_matrix = copy_data.local_matrix();
local_matrix = 0;
```

Extrait abrégé de [assemble_local_matrix](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L481-L486).

**Question.** La seconde ligne remet-elle à zéro la matrice de `copy_data` ou une copie ? Que changerait `auto local_matrix` sans `&` ?

<details><summary>Indice</summary>
Regarde le type de retour de CopyDataBase::local_matrix : FullMatrix&lt;double&gt; &.
</details>

<details><summary>Réponse</summary>

Avec `auto &`, la variable est une référence : elle désigne la matrice contenue dans CopyData. La remise à zéro agit sur l'original. Sans `&`, la déduction de `auto` crée une valeur, donc une copie de la matrice ; la remise à zéro n'affecterait que cette copie. Ici la référence est nécessaire pour que les assembleurs et le copieur travaillent sur le même stockage. [Accesseur](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/copy_data.h#L121-L127).
</details>

**Petit exercice.** Écris en C++ un entier `n=3`, une copie `a=n` et une référence `b=n`. Fais `a=4`, puis `b=5`. Prédit les trois valeurs. Réponse : n=5, a=4, b=5.

## 2 — Une option à la compilation ou à l'exécution ?

```cpp
if constexpr (with_moving_mesh)
  Assembly::Elasticity::setup_assemblers<dim, ScratchData, CopyData>(
    this->param, *this->ordering, assemblers);
```

[Extrait](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/incompressible_chns_solver.cpp#L269-L272).

**Question.** En lançant `CHNSSolver<2>`, la lecture du fichier de paramètres peut-elle rendre cette branche vraie ?

<details><summary>Réponse</summary>

Non : `with_moving_mesh` est un paramètre de template dont la valeur par défaut est `false`. Pour cette instanciation, la branche est écartée à la compilation. Il faut choisir une instanciation avec `true` pour inclure ce chemin. Les paramètres lus à l'exécution peuvent ensuite commander des choix à l'intérieur d'un chemin déjà compilé. [Déclaration](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/incompressible_chns_solver.h#L16-L22).
</details>

**Petit exercice.** Compare mentalement `if (flag)` et `if constexpr (flag)` : lequel exige une condition connue à la compilation ? Réponse : le second.

## 3 — Pourquoi deux familles de contraintes ?

```cpp
newton_update = completely_distributed_solution;
zero_constraints.distribute(newton_update);
```

[Après la résolution linéaire](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/linear_solver.cpp#L41-L46).

Plus loin dans Newton :
```cpp
solver->local_evaluation_point.add(alpha, solver->newton_update);
solver->distribute_nonzero_constraints();
```

[Lors d'une recherche linéaire](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/newton_solver.h#L123-L127).

**Question.** Si la vitesse doit rester égale à 2 sur une frontière, quelle valeur y souhaite-t-on pour l'incrément de Newton : 0 ou 2 ?

<details><summary>Réponse</summary>

Pour une valeur déjà imposée à 2, l'incrément doit être 0. Ajouter 2 à chaque itération ferait dériver la valeur. Les contraintes homogènes s'appliquent donc à l'incrément ; les contraintes non homogènes rétablissent la valeur 2 sur la solution. Le raisonnement vise une condition de Dirichlet simple ; les contraintes générales peuvent aussi relier plusieurs DoFs.
</details>

## 4 — Un nom de variable raconte-t-il toute l'équation ?

```cpp
diffusive_flux[q] = diffusive_flux_factor *
                    present_velocity_gradients[q] *
                    potential_gradients[q];
```

[Préparation des données CHNS](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/include/scratch_data.h#L1064-L1066).

**Question.** Cette variable dépend-elle seulement du potentiel chimique μ ? Quels autres éléments faut-il relire avant de modifier son calcul ?

<details><summary>Réponse</summary>

Elle dépend aussi du gradient de vitesse et du facteur `mobility * 0.5 * (density1 - density0)`. Le stockage représente déjà une contribution contractée avec le gradient de vitesse. Il faut relire le résidu de quantité de mouvement **et** les variations du Jacobien par rapport à u et μ. [Facteur](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/scratch_data.cpp#L400-L409), [variations](https://github.com/arthurbawin/fez/blob/ccf20caa0745cc2fe640f879d34acf2bf3855e6c/src/assembly/incompressible_chns_assemblers.cpp#L370-L377). Le nom seul ne garantit pas le sens mathématique.
</details>

## Ce que tu sais retrouver après cette lecture

Tu peux identifier une référence C++, distinguer une spécialisation de template d'un paramètre d'exécution, séparer solution et incrément, puis suivre un terme de son calcul à son utilisation. Le prochain exercice pourra faire cette même lecture sur ta branche de production et comparer ce qui change.

