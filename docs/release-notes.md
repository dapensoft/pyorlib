---
hide:
  - navigation
---

<style>
	.divider {
		margin-top: -0.5em !important;
		margin-bottom: -0.2em !important;
	}
</style>

[//]: # (--------------------------------------------------------------------------------------------------------------)

## [v0.1.1](https://github.com/dapensoft/pyorlib/releases/tag/0.1.1) <small>March 2, 2024</small> { id="0.1.1" }

<hr class="divider">

##### Changed

- The `print_info` and `print_solution` methods in the `Model` class have been enhanced to improve visibility and
  provide deeper insights.
- The `get_pretty_string` method in the `Term` class has been refactored as an `@abstractmethod` for subclass
  customization and delegation based on specific term needs.
- Badges on the main page of the documentation and the readme file have been updated to improve visibility and align
  with the package's color palette.
- The `git-committers` plugin in the `mkdocs.yml` file has been updated to exclude the `index.md`, `examples/index.md`,
  and `api/index.md` files for consistency in the current configuration with the `git-revision-date-localized` plugin.

[//]: # (--------------------------------------------------------------------------------------------------------------)

## [v0.1.0](https://github.com/dapensoft/pyorlib/releases/tag/0.1.0) <small>March 2, 2024</small> { id="0.1.0" }

<hr class="divider">

##### Initial Implementation

&emsp;&emsp;This release introduces the initial version of PyORlib, a powerful Python library for operations research
and optimization. PyORlib provides a set of abstractions to easily define, solve, and interact with mathematical models
in a standardized manner across different optimization packages. It serves as a user-friendly and powerful platform for
students, researchers, and practitioners to explore optimization concepts, experiment with algorithms, and expand their
knowledge.

- **Implementation Details:** The first implementation includes all the core functionalities of the package,
  encompassing built-in optimization package integrations, algebraic modeling, validators, and more.
- **Testing and Coverage:** This release includes a test suite that verifies the correctness of the package
  implementation. It also integrates code coverage, achieving 100% test coverage. The tests are configured to run
  automatically via GitHub Actions on both push and pull requests to the master branch.
- **Formatter and Lint Configuration:** A formatter and lint configuration have been added to the project. This ensures
  consistent code style, maintainability, and adherence to the established coding standards defined in the project
  documentation.
- **Documentation:** Additionally, this release includes comprehensive documentation for the package. The documentation
  covers the main page, a detailed getting started guide, examples, API reference, and release notes.

[//]: # (--------------------------------------------------------------------------------------------------------------)

<br>
