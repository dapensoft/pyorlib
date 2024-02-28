---
hide:
  - navigation
---

<style>
    .md-content .md-content__inner.md-typeset h1 { height: 0; margin: 0; color: transparent; }
    .md-content .md-content__inner.md-typeset::before { height: 0; } 
</style>

<br>

<p align="center">
   <img src="./images/logo/pyorlib-logo-name-slogan.svg" alt="PyORlib" width="900px">
</p>

<br>

---

**Documentation**: <a href="https://dapensoft.github.io/pyorlib" target="_blank">https://dapensoft.github.io/pyorlib</a>

**Source Code**: <a href="https://github.com/dapensoft/pyorlib" target="_blank">https://github.com/dapensoft/pyorlib</a>

---

<p style='text-align: justify;' markdown>
    &emsp;&emsp;PyORlib is a powerful Python library for operations research and optimization. It provides a set of 
    abstractions to easily define, solve, and interact with mathematical models in a standardized manner across 
    different optimization packages. With PyORlib, you can easily implement mathematical models using a user-friendly 
    interface, while seamlessly identifying the ideal solver or optimization package, such as CPLEX, Gurobi, 
    OR-Tools, or PuLP, that perfectly aligns with your specific requirements.
</p>

## Key Features

<p style='text-align: justify;'>
    PyORlib offers a powerful yet easy-to-use set of tools for mathematical modeling and optimization:
</p> 

<ul style='text-align: justify;'>

<li><b>Intuitive API</b> ─ 
PyORlib provides a user-friendly API that allows you to define, solve, and interact with mathematical models in a 
standardized manner across different optimization packages.
</li>

<li><b>Seamless Solver Integration</b> ─ 
Optimize models across different solvers, including custom ones, without modifying the model's definition. Tailor the 
behavior and capabilities of the solvers to perfectly align with your unique requirements.
</li>

<li><b>Simplified Mathematical Modeling</b> ─ 
Define mathematical models effortlessly using PyORlib's comprehensive set of abstractions and classes. Focus on the 
problem at hand instead of getting lost in implementation details.
</li>

<li><b>Scalability and Maintainability</b> ─ 
Keep your code organized, readable, and maintainable over time with the PyORlib's workflow. Structure your variables,
parameters, constraints, and objective functions in a clean and extensible manner.
</li>

<li><b>No Overhead</b> ─ 
PyORlib ensures full compatibility between models and different solvers by seamlessly translating models to each 
solver's native format, acting as a standardized communication interface.
</li>

<li><b>Data Validation</b> ─ 
PyORlib offers comprehensive format and content validations to ensure the integrity of your model data. These 
validation features help identify errors early and maintain consistent, error-free model data for robust optimization.
</li>

<li><b>Comprehensive Documentation</b> ─ 
PyORlib provides a comprehensive documentation suite that includes API references and usage examples, to effectively
leverage all the features and capabilities of the library.
</li>

</ul>

## A Simple Example

<p style='text-align: justify;'>
    &emsp;&emsp;Experience the power of PyORlib through a simple example that illustrates the core concepts and basic 
	usage of the package by formulating and solving a mixed integer programming (MIP) problem from the 
	<a href="https://developers.google.com/optimization/mip/mip_example" target="_blank">OR-Tools documentation</a>.
	This example will provide you with a clear and concise introduction to the package's functionalities and its 
	application in real-world optimization challenges.
</p>

### Problem Definition

<p style='text-align: justify;'>
    &emsp;&emsp;In this example, we will find the highest integer coordinates <i>(x, y)</i> on the <i>Y-axis</i> within 
	a defined shape. Our objective is to maximize the value of an objective function while satisfying linear 
	constraints, as shown below with a mathematical formulation:
</p>

$$
\begin{align}
\text{Maximize:} \quad & x + 10y \\
\text{Subject to:} \quad & x + 7y = 17.5 \\
& 0 \leq x \leq 3.5 \\
& 0 \leq y \leq 2.5 \\
\end{align}
$$

<p style='text-align: justify;'>
    &emsp;&emsp;Since the constraints are linear, we can classify this problem as a linear optimization problem in 
	which the solutions are required to be integers. The feasible region and integer points for this problem are 
	shown below:
</p>

<p align="center">
   <img src="./images/examples/simple-example-graph.svg" alt="Simple graph illustrating the feasible region and integer points" width="800px" style="margin-top: -10px;margin-bottom: -20px;">
</p>

### Solution Using PyORlib

<p style='text-align: justify;'>
	&emsp;&emsp;In order to model and solve this problem, we'll be using the PyORlib package. In this example, we'll 
	utilize the OR-Tools optimization package, which is one of the built-in integrations provided by PyORlib. However,
	you can also choose to use other integration options described in the <a href="https://dapensoft.github.io/pyorlib/getting-started/#optional-dependencies" target="_blank">Optional Dependencies</a>
	section, or even implement your own custom integration. Before proceeding, make sure you have installed the OR-Tools
	integration. Once that is done, let's get started:
</p>

```Python title="Solving a MIP Problem with PyORlib" linenums="1"
from math import inf

from pyorlib import Model
from pyorlib.engines.ortools import ORToolsEngine
from pyorlib.enums import ValueType, OptimizationType

# Create a Model instance using the ORTools engine
model: Model = Model(engine=ORToolsEngine())

# Add two integer variables for coordinates x and y
x = model.add_variable("x", ValueType.INTEGER, 0, inf)
y = model.add_variable("y", ValueType.INTEGER, 0, inf)

# Define problem constraints
model.add_constraint(x + 7 * y <= 17.5)
model.add_constraint(x <= 3.5)

# Set objective to maximize x + 10y
model.set_objective(OptimizationType.MAXIMIZE, x + 10 * y)

# Solve model
model.solve()

# Print solution
model.print_solution()
```

<details markdown="1" class="tip">
<summary>You can also work with other engines...</summary>

<p style='text-align: justify;'>
    &emsp;&emsp;With PyORlib, you have the flexibility to utilize various engines, such as the <code>GurobiEngine</code>,
	to solve the same model without altering its definition. To learn more about supported integrations, please refer to
	the <a href="https://dapensoft.github.io/pyorlib/getting-started/#optional-dependencies" target="_blank">Optional Dependencies</a>
	section.
</p>

```Python title="Solving a MIP Problem with PyORlib (Gurobi engine)" linenums="1" hl_lines="8"
from math import inf

from pyorlib import Model
from pyorlib.engines.gurobi import GurobiEngine
from pyorlib.enums import ValueType, OptimizationType

# Create a Model instance using the Gurobi engine
model: Model = Model(engine=GurobiEngine())

# Add two integer variables for coordinates x and y
x = model.add_variable("x", ValueType.INTEGER, 0, inf)
y = model.add_variable("y", ValueType.INTEGER, 0, inf)

# Define problem constraints
model.add_constraint(x + 7 * y <= 17.5)
model.add_constraint(x <= 3.5)

# Set objective to maximize x + 10y
model.set_objective(OptimizationType.MAXIMIZE, x + 10 * y)

# Solve model
model.solve()

# Print solution
model.print_solution()
```

</details>

<p style='text-align: justify;'>
    &emsp;&emsp;As we can see from the previous example, PyORlib follows a simple and user-friendly workflow for 
	defining, solving, and interacting with mathematical models. Let's review the key steps:
</p>

<ol style='text-align: justify;'>

<li>
<b>Import necessary modules:</b> We first imported the required modules from PyORlib, including the <code>Model</code> 
class, <code>ORToolsEngine</code> class, and necessary enums (<code>ValueType</code> and <code>OptimizationType</code>).
</li>

<li>
<b>Create a new model:</b> Then we created a new <code>Model</code> object and specified that we want to use the 
OR-Tools engine for solving the optimization problem.
</li>

<li>
<b>Define the variables:</b> We added 2 integer variables, <i>x</i> and <i>y</i>, to represent the coordinates on the
<i>Y-axis</i> within the defined shape.
</li>

<li>
<b>Define the constraints:</b> We added linear constraints to the model to restrict the feasible region of the 
optimization problem and ensure the coordinates <i>(x, y)</i> satisfy specific conditions.
</li>

<li>
<b>Define the objective function:</b> We set the objective of the model using the <code>set_objective</code> method to 
maximize the objective function <i>x + 10 * y</i>.
</li>

<li>
<b>Solve the model:</b> We invoked the solve method on the model to find the optimal values for variables <i>(x, y)</i>
that satisfy the constraints and maximize the objective function.
</li>

<li>
<b>Display the solution:</b> Finally, we called the print_solution method to showcase the optimal values of variables 
<i>(x, y)</i> and the corresponding value of the objective function.
</li>

</ol>

<p style='text-align: justify;'>
    &emsp;&emsp;Now, let's run the previous code example to solve the defined model and compare it to the solution 
	obtained using only the OR-Tools API, as demonstrated in the examples provided in the <a href="https://developers.google.com/optimization/mip/mip_example" target="_blank">OR-Tools documentation</a>.
	By executing the code, you should obtain the following optimal solution:
</p>

```console hl_lines="1 4-5 7-8"
------ MODEL SOLUTION ------

Objective function:
	Status: OPTIMAL
	Value:  23 
Terms:
	Name: x | Type: Variable | Value type: Integer | lb: 0 | ub: inf | val: 3 
	Name: y | Type: Variable | Value type: Integer | lb: 0 | ub: inf | val: 2 


Process finished with exit code 0
```

<p style='text-align: justify;'>
    &emsp;&emsp;Having gained a clear understanding of the workflow showcased in the Simple Example, you are now 
	well-equipped to explore more intricate optimization scenarios and fully harness the capabilities of PyORlib in 
	your own projects.
</p>

<details markdown="1" class="example" open>
<summary>Next steps...</summary>

<p style='text-align: justify;'>
    &emsp;&emsp;Feel free to experiment and build upon this example to explore the full potential of PyORlib in your 
	projects. With PyORlib, you can define and implement complex mathematical models and algorithms, test multiple 
	optimization packages to identify the ideal one that perfectly aligns with your unique requirements, define 
	and organize the vital components of your optimization model, and much more!
</p>
</details>

## Runtime Flexibility and Customization

<p style='text-align: justify;'>
    &emsp;&emsp;At its core, PyORlib provides a modular optimization design that allows you to seamlessly switch between
	different built-in or custom optimization engine implementations on the fly. Whether you opt for official 
	optimization package integrations or decide to create your own custom ones, PyORlib allows you to tailor 
	the behavior and capabilities of the optimization engine to perfectly align with your unique requirements.
</p>

<p style='text-align: justify;'>
    &emsp;&emsp;By leveraging the principles of dependency inversion and open-closed design, PyORlib decouples the 
	model's optimization from the underlying implementation, allowing you to optimize models across different 
	optimization engines, including custom ones, without modifying the model definition or employing complex logic.
</p>

### Seeing it in Action

<p style='text-align: justify;'>
    &emsp;&emsp;To showcase the flexibility of PyORlib, let's revisit the <a href="#a-simple-example">Simple Example</a>
	we discussed earlier and use it as our foundation. After copying the example, we will make some modifications to 
	decouple the dependency from a specific optimization engine to its interface, and encapsulate the model definition
	and resolution within a function to ensure reusability across different optimization engines, as shown below:
</p>

```Python linenums="1" hl_lines="4-5 9 11 32 35"
from math import inf

from pyorlib import Model, Engine
from pyorlib.engines.gurobi import GurobiEngine
from pyorlib.engines.ortools import ORToolsEngine
from pyorlib.enums import ValueType, OptimizationType


def mip_problem(engine: Engine):
    # Create a Model instance
    model: Model = Model(engine)

    # Add two integer variables for coordinates x and y
    x = model.add_variable("x", ValueType.INTEGER, 0, inf)
    y = model.add_variable("y", ValueType.INTEGER, 0, inf)

    # Define problem constraints
    model.add_constraint(x + 7 * y <= 17.5)
    model.add_constraint(x <= 3.5)

    # Set objective to maximize x + 10y
    model.set_objective(OptimizationType.MAXIMIZE, x + 10 * y)

    # Solve model
    model.solve()

    # Print solution
    model.print_solution()


# Solving the MIP problem using the ORTools engine
mip_problem(engine=ORToolsEngine())

# Solving the MIP problem using the Gurobi engine
mip_problem(engine=GurobiEngine())
```

<p style='text-align: justify;'>
    &emsp;&emsp;As we can see from the example, by just depending on the engine interface instead of a concrete 
	implementation and applying dependency injection, we were able to solve the same MIP problem from the Simple 
	Example across multiple optimization engines, including custom ones, without modifying the underlying model 
	definition and optimization.
</p>

### Built-in & Custom Integrations

<p style='text-align: justify;'>
    &emsp;&emsp;Out of the box, PyORlib provides integrations for popular solvers like CPLEX, Gurobi, OR-Tools and PuLP,
	leveraging their proven algorithms to optimize models reliably. These integrations give you access to top-tier 
	solvers without additional work. However, the options are not limited only to built-in integrations.
</p>

<p style='text-align: justify;'>
    &emsp;&emsp;PyORlib also supports custom engine implementations through its extensible and flexible architecture. 
	You can create your own optimization engines by subclassing the base <code>Engine</code> class and implementing the 
	necessary methods, whether using third-party or custom algorithms.
</p>

## Continuous Evolution

&emsp;&emsp;PyORlib continuously adapts to support developers across various technological and programming domains. Its
primary goal is to remain a useful tool for learning about operations research, mathematical model optimization, and
testing different optimization packages. While future development may introduce some changes to enhance and expand
certain characteristics of the current functionality, we don't anticipate any significant changes that would
fundamentally alter the nature of the library.

<details markdown="1" class="info" open>
<summary>Driving Innovation Through Collaboration</summary>

<p style='text-align: justify;'>
    PyORlib is an open source project that welcomes community involvement. If you wish to contribute
	additional optimization suites, improvements, or bug fixes, please check the <a href="/pyorlib/contributing/">Contributing</a> section for guidelines on collaborating.
</p>
</details>

## Get Started Today!

<p style='text-align: justify;' markdown>
    &emsp;&emsp;Are you ready to get started with mathematical modeling and optimization using PyORlib? Follow these 
    steps to integrate PyORlib into your project and start leveraging its powerful modeling tools. Click the button
    below to navigate to the PyORlib Getting Started page and explore detailed instructions, examples, and more:
</p>

---

<p style='text-align: center;' markdown>
    [:material-star-outline:&emsp;Getting Started&emsp;:material-star-outline:](/pyorlib/getting-started/){ .md-button }
</p>

---

## License

<p style='text-align: justify;' markdown>
    &emsp;&emsp;PyORlib is distributed as open source software and is released under the <a href="https://choosealicense.com/licenses/mit/" target="_blank">MIT License</a>. 
    You can view the full text of the license in the <a href="https://github.com/dapensoft/pyorlib/blob/master/LICENSE" target="_blank"><code>LICENSE</code></a> 
    file located in the PyORlib repository.
</p>

