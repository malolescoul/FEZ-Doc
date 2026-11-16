# Documentation maintenance and preview organization

## Version and provenance

The documented FEZ revision is `c6c4dd08b4ab3376062f031d577406a30a6e06bf`, verified through GitHub's `master` branch endpoint on 16 November 2026. Documentation changes belong only to `malolescoul/FEZ-Doc`, branch `docs/fez-master-guide`. No source changes in FEZ are part of this work.

The historical atlas remains at the repository root and in `assets/`, `data/`, `knowledge/`, `pedagogie/` and `doxygen/`. Preserve those files in place. New reference content is contained in `docs/`; historical snapshots must not be mixed into the current-master navigation or search corpus.

## Information architecture

The organization follows the separation of applications, theory, parameters and practical guides in [Lethe's contents](https://github.com/chaos-polymtl/lethe/blob/master/doc/source/index.rst), while keeping model parameters next to their model and shared methods in one place. The distinction between meshes, finite elements, mappings, DoF handlers, assembly and algebra follows [deal.II's reference organization](https://www.dealii.org/current/doxygen/deal.II/index.html). Neither project's physics is used as evidence for FEZ capabilities.

An eventual documentation renderer should expose the same grouped navigation as the home page, a page table of contents, full-text search over the new guide, equation rendering, source links and an explicit revision label. A local MkDocs configuration is supplied under `docs/preview/` as an isolated preview candidate. It does not alter an existing hosting configuration, add a deployment workflow, or publish a site.

## Coverage and remaining work

This edition provides a page for each of the nine executable entry points, shared numerical-method pages, explicit FEZ-owned parameter declaration tables and a linked index. The tables include dynamic boundary/material/metric families, both linear-solver blocks, quadrature helpers and postprocessing helpers. Library-delegated parsed-function settings and the full manufactured-field vocabulary are not yet exhaustively indexed; no claim of complete parameter coverage is made for those entries.

Source inspection established model residuals and several rejected or ineffective options. Remaining scientific questions are grouped in [limitations](limitations.md). Numerical examples, runtime solver combinations, performance, restart compatibility and convergence validation require subsequent work. A source audit is not a substitute for those checks.

## Review checks

Before updating the branch, check all relative links and parameter anchors, source paths and line ranges against the pinned FEZ tree, table names/defaults against declarations, and the complete Git tree diff. Only `docs/` entries may change in this edition; all other tree entries must retain their SHA. Recheck the branch head before an atomic update to avoid overwriting concurrent work.

## Local preview candidate

From the repository root, use a separate Python environment, install `docs/preview/requirements.txt`, then run `mkdocs build --strict --config-file docs/preview/mkdocs.yml` or `mkdocs serve --config-file docs/preview/mkdocs.yml`. Generated files go to `/tmp/fez-doc-preview`. The navigation and search corpus contain the new reference pages only. Mathematical display uses MathJax from a pinned CDN URL and therefore requires network access for equation rendering. An offline bundle and any hosting configuration remain separate decisions.

## Checks for this edition

The local documentation build passed `mkdocs build --strict` with MkDocs 1.6.1 and pymdown-extensions 10.16.1. Static checks covered 22 Markdown pages, 303 distinct parameter records, internal file links and explicit parameter anchors, and pinned FEZ source paths. The generated search index contains only the new guide. The rendered HTML contains equation wrappers and parameter anchors. No FEZ compilation or numerical solver test was run; browser-level visual and interaction testing remains separate from these build checks.
