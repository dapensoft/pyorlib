---
hide:
  - navigation
---

<style>
	.go:before {
		content: "$";
		padding-right: 1.17647em;
	}
</style>

<p style='text-align: justify;' markdown>
    &emsp;&emsp;Welcome to the Getting Started section! This guide will help you install and configure PyORlib in your
	optimization project. For more detailed information about the library, you can refer to the PyORlib 
	[examples](/pyorlib/examples) or [API Reference](/pyorlib/api).
</p>

## Requirements

<p style='text-align: justify;' markdown>
	&emsp;&emsp;By default, PyORlib's core functionalities and optimization utilities only require Python 3.10+. 
	However, additional optional dependencies may be needed to work with optimization models and solver 
	integrations based on your use case. For more information on supported integrations, see the 
	[Optional Dependencies](/pyorlib/getting-started/#optional-dependencies) section below.
</p>

## Installation

<p style='text-align: justify;' markdown>
	&emsp;&emsp;PyORlib is available as a Python package and can be easily installed using `pip`. To install the core 
	functionalities, open your terminal and execute the following command:
</p>

```console
pip install pyorlib
```

## Optional Dependencies

<p style='text-align: justify;' markdown>
	&emsp;&emsp;While PyORlib's core functionality relies primarily on Python's standard library, the package is 
	designed from the ground up to seamlessly integrate with popular solvers through a modular and unified API.
</p>

<details markdown="1" class="warning" open>
<summary>Solver License Notice</summary>

<p style='text-align: justify;'>
    &emsp;&emsp;PyORlib integrates with solvers through their Python APIs but does not bundle the solvers 
	themselves. Access to solvers is governed by individual licenses and requirements set by each provider. 
	Please check the solver documentation for details on installation, configuration and licensing.
</p>

</details>

### Supported Solver Integrations

<ul style='text-align: justify;' markdown>

<li class="annotate" markdown>
<a href="https://www.ibm.com/docs/en/icos/22.1.1?topic=cplex-optimizers" target="_blank">**CPLEX**</a> ─ 
PyORlib integrates with the powerful CPLEX solver through the [`CplexEngine`](/pyorlib/api/engines/cplex) 
interface. This integration allows you to optimize models using CPLEX's advanced algorithms and features. To install 
PyORlib with CPLEX support, please use the following command:

```console
pip install pyorlib[cplex]
```

</li>

---
<li class="annotate" markdown>
<a href="https://www.gurobi.com/documentation/current/refman/py_python_api_overview.html" target="_blank">**Gurobi**</a> ─ 
PyORlib integrates with Gurobi, a powerful solver renowned for its high-performance optimization capabilities, through
the [`GurobiEngine`](/pyorlib/api/engines/gurobi) interface. This integration enables efficient optimization of models
using Gurobi's advanced algorithms and features. To install PyORlib with Gurobi support, use the following command:

```console
pip install pyorlib[gurobi]
```

</li>


---
<li class="annotate" markdown>
<a href="https://developers.google.com/optimization/introduction/python" target="_blank">**OR-Tools**</a> ─ 
PyORlib integrates with OR-Tools through the [`ORToolsEngine`](/pyorlib/api/engines/ortools) interface. This enables
efficient optimization of linear and integer programming models using OR-Tools' advanced algorithms. To install 
PyORlib with OR-Tools support, use:

```console
pip install pyorlib[ortools]
```

</li>

---
<li class="annotate" markdown>
<a href="https://coin-or.github.io/pulp/" target="_blank">**PuLP**</a> ─ 
PyORlib integrates with PuLP through the [`PuLPEngine`](/pyorlib/api/engines/pulp) interface. This enables optimization
of models using PuLP's Python modeling language and interface to various solvers. To install PyORlib with PuLP support,
use:

```console
pip install pyorlib[pulp]
```

</li>

</ul>


---

You can install all of them with:

```console
pip install pyorlib[all]
```

<br>
