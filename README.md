<br>

<p align="center">
   <img src="https://dapensoft.github.io/pyorlib/images/logo/pyorlib-logo-name-slogan.svg" alt="PyORlib" width="750px">
</p>

<br>

<p align="center">

<a href="https://github.com/dapensoft/pyorlib/actions?query=workflow%3ATests+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/dapensoft/pyorlib/actions/workflows/run-tests.yml/badge.svg?branch=master" alt="Tests">
</a>

<a href="https://github.com/dapensoft/pyorlib/actions?query=workflow%3ADocs+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/dapensoft/pyorlib/actions/workflows/deploy-docs.yml/badge.svg?branch=master" alt="Docs">
</a>

<a href='https://coveralls.io/github/dapensoft/pyorlib?branch=master'>
	<img src='https://coveralls.io/repos/github/dapensoft/pyorlib/badge.svg?branch=master' alt='Coverage Status'/>
</a>

<a href="https://pypi.org/project/pyorlib" target="_blank">
    <img src="https://img.shields.io/pypi/v/pyorlib?color=deeppink" alt="Package version">
</a>

<a href="https://pypi.org/project/pyorlib" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/pyorlib?color=deeppink" alt="Supported Python versions">
</a>

<a href="https://github.com/psf/black">
	<img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
</a>

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

## Requirements

<p style='text-align: justify;'>
	&emsp;&emsp;By default, PyORlib's core functionalities and optimization utilities only require Python 3.10+. 
	However, additional optional dependencies may be needed to work with optimization models and solver 
	integrations based on your use case. For more information on supported integrations, see the 
	<a href="https://dapensoft.github.io/pyorlib/getting-started/#optional-dependencies" target="_blank">Optional Dependencies</a> section.
</p>

## Installation

<p style='text-align: justify;'>
	&emsp;&emsp;PyORlib is available as a Python package and can be easily installed using <code>pip</code>. To install the core 
	functionalities, open your terminal and execute the following command:
</p>

```console
pip install pyorlib
```

<p style='text-align: justify;'>
	&emsp;&emsp;For optimization models and solver integrations, please refer to the <a href="https://dapensoft.github.io/pyorlib/getting-started/#optional-dependencies" target="_blank">Optional Dependencies</a>
	section to learn more about the supported integrations and the dependencies you may need to install.
</p>

## A Simple Example

<p style='text-align: justify;'>
    &emsp;&emsp;Experience the power of PyORlib through a simple example that illustrates the core concepts and basic 
	usage of the package by formulating and solving a mixed integer programming (MIP) problem from the 
	<a href="https://developers.google.com/optimization/mip/mip_example" target="_blank">OR-Tools documentation</a>.
	This example will provide you with a clear and concise introduction to the package's functionalities and its 
	application in real-world optimization challenges.
</p>

### Problem Formulation

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
   <img src="https://dapensoft.github.io/pyorlib/images/examples/simple-example-graph.svg" alt="Simple graph illustrating the feasible region and integer points" width="800px" style="margin-top: -10px;margin-bottom: -20px;">
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

## A Practical Example

<p style='text-align: justify;' markdown>
	&emsp;&emsp;To demonstrate PyORlib in a realistic scenario, we will implement a transportation problem from the 
	<a href="https://www.gams.com/docs/pdf/Tutorial.PDF" target="_blank">GAMS Tutorial</a> by Richard E. Rosenthal, 
	which provides a comprehensive case study for testing PyORlib's optimization capabilities and features.
</p>

### Problem Formulation

<p style='text-align: justify;'>
    &emsp;&emsp;The transportation problem we will address is a classic instance of linear programming's transportation
	problem, which has historically served as a testing ground for the development of optimization technology. This 
	transportation problem involves determining the optimal flow of a product from multiple sources (plants) to 
	destinations (markets) to minimize costs while satisfying demands.
</p>

$$
\begin{align}
\text{Minimize:} \quad & \sum_{i=1}^{n} \sum_{j=1}^{m} c_{ij} x_{ij} \\
\\
\text{Subject to:} \quad & \sum_{j=1}^{m} x_{ij} \leq a_{i} \quad \forall_{i} \\
& \sum_{i=1}^{n} x_{ij} \geq b_{j} \quad \forall_{j} \\
& x_{ij} \geq 0 \quad \forall_{ij}, \thinspace integer \\
& i=1,...,n; \quad j=1,...,m \\
\end{align}
$$

<p style='text-align: justify;'>
    &emsp;&emsp;Before diving into the implementation, let's take a moment to familiarize ourselves with the key 
	components of the model. This brief exploration will provide a better understanding of how these components 
	work together.
</p>

- **Indices:**

	&emsp; $i=$ plants; $\quad j=$ markets.

- **Parameters (Given Data):**

	&emsp; $a_{i}=$ supply of commodity of plant $i$ (in cases).

	&emsp; $b_{j}=$ demand for commodity at market $j$ (cases).

	&emsp; $c_{ij}=$ cost per unit shipment between plan $i$ and market $j$ ($/case).

- **Decision Variables:**

	&emsp; $x_{ij}=$ amount of commodity to ship from plant $i$ to market $j$ (cases).

- **Constraints:**

    &emsp;Observe supply limit at plant $i$: $\sum_{j=1}^{m} x_{ij} \leq a_{i} \quad \forall_{i}$

	&emsp;Satisfy demand at market $j$: $\sum_{i=1}^{n} x_{ij} \geq b_{j} \quad \forall_{j}$

<p style='text-align: justify;'>
    &emsp;&emsp;The GAMS tutorial describes a scenario with two canning plants and three markets. It provides sample 
	supply, demand and cost data. We will use this same data to define our model.
</p>

<table align="center">
    <thead>
		<tr>
            <th></th>
            <th>New York</th>
            <th>Chicago</th>
            <th>Topeka</th>
            <th>Supply</th>
        </tr>
    </thead>
    <tbody>
		<tr>
            <td>Seattle</td>
            <td>2.5</td>
            <td>1.7</td>
            <td>1.8</td>
            <td>350</td>
        </tr>
		<tr>
            <td>San Diego</td>
            <td>2.5</td>
            <td>1.8</td>
            <td>1.4</td>
            <td>600</td>
        </tr>
		<tr>
            <td>Demand</td>
            <td>325</td>
            <td>300</td>
            <td>275</td>
            <td></td>
        </tr>
		<tr>
            <td style="text-align: center" colspan="5">
				<a href="https://miro.gams.com/gallery/app_direct/transport/" target="_blank">
					<img src="https://dapensoft.github.io/pyorlib/images/examples/practical-example-graph.png" alt="A Transportation Problem">
				</a>
			</td>
        </tr>
    </tbody>
</table>

<p style='text-align: justify;'>
    &emsp;&emsp;To model and solve the problem in Python, we will use PyORlib and its CPLEX integration. However, it’s 
	important to note that you can choose any of the supported optimization engine integrations described in the 
	<a href="https://dapensoft.github.io/pyorlib/getting-started/#optional-dependencies" target="_blank">Optional Dependencies</a> 
	or even use your own custom implementations.
</p>

### Solution Using PyORlib

<p style='text-align: justify;'>
    &emsp;&emsp;Before proceeding, ensure that PyORlib is installed, along with its integration for the CPLEX engine. 
	Once everything is set up, let's build our transportation model:
</p>

```Python title="Solving a Transportation Problem with PyORlib" linenums="1" hl_lines="7 10 16 24 36 45 54 64"
from math import inf

from pyorlib import Model
from pyorlib.engines.cplex import CplexEngine
from pyorlib.enums import ValueType, OptimizationType

# Create a transportation model using the CplexEngine.
model = Model(engine=CplexEngine(), name="A Transportation Model")

# Define the dimensions of the problem
n = 2  # Number of plants
m = 3  # Number of markets
n_range = range(1, n + 1)  # Range of plant indices
m_range = range(1, m + 1)  # Range of market indices

# Define the parameters of the model
a_i = [350, 600]  # Supply limit at each plant
b_j = [325, 300, 275]  # Demand at each market
c_i_j = [  # Transportation costs
    2.5, 1.7, 1.8,
    2.5, 1.8, 1.4,
]

# Define the decision variables
x_i_j = {
    (i, j): model.add_variable(
        name=f"x_{i}_{j}",
        value_type=ValueType.INTEGER,
        lower_bound=0,
        upper_bound=inf
    )
    for i in n_range
    for j in m_range
}

# Add supply limit at plants constraints
for i in n_range:
    model.add_constraint(
        expression=sum(
            x_i_j[i, j]
            for j in range(1, m + 1)
        ) <= a_i[i - 1]
    )

# Add satisfy demand at markets constraints
for j in m_range:
    model.add_constraint(
        expression=sum(
            x_i_j[i, j]
            for i in range(1, n + 1)
        ) >= b_j[j - 1]
    )

# Set the objective function to minimize the total transportation cost
model.set_objective(
    opt_type=OptimizationType.MINIMIZE,
    expression=sum(
        c_i_j[(i - 1) * m + (j - 1)] * x_i_j[i, j]
        for i in n_range
        for j in m_range
    )
)

# Solve the model and print the solution
model.solve()
model.print_solution()
```

<p style='text-align: justify;'>
    &emsp;&emsp;As we can see from this practical example, PyORlib enables us to easily build a transportation model, 
	define its necessary components, optimize the model, and obtain the optimal solution. The simple yet powerful 
	syntax of PyORlib allows us to focus on the problem at hand without getting lost in implementation details.
</p>

## Organized & Readable Workflow

<p style='text-align: justify;'>
    &emsp;&emsp;PyORlib goes beyond the optimization process and offers a powerful modeling workflow that emphasizes 
	code organization, readability, and maintainability over time. This workflow is built upon a set of abstractions 
	and classes from the structures module, that allows you to centralize and standardize the definition of your 
	model's components, such as dimensions, parameters, decision variables, and constant properties.
</p>

<p style='text-align: justify;'>
    &emsp;&emsp;One significant advantage of PyORlib's workflow is the ability to easily rename and modify components 
	throughout your codebase. Instead of manually searching and replacing strings, you can make changes in one place, 
	ensuring consistency and reducing errors.
</p>

```Python linenums="1" hl_lines="12-13 17-24 28-32"
from abc import ABC
from dataclasses import dataclass

from pyorlib.enums import ParameterType, ValueType
from pyorlib.structures import DimensionDefinition, ParameterDefinition, TermDefinition


class GenericModelDefinition(ABC):
	
    @dataclass(frozen=True)
    class Dimensions(ABC):
        n = DimensionDefinition(name="n", display_name="Total number of 'i' indices", min=1)
        m = DimensionDefinition(name="m", display_name="Total number of 'j' indices", min=1)

    @dataclass(frozen=True)
    class Parameters(ABC):
        c_i_j = ParameterDefinition(
            set_name="c_i_j",
            name=lambda i, j: f"c_{i}_{j}",
            display_name="Cost per unit shipment between 'i' and 'j'",
            parameter_types={ParameterType.FIXED, ParameterType.BOUNDED},
            value_types={ValueType.CONTINUOUS},
            min=0,
        )

    @dataclass(frozen=True)
    class DecisionVariables(ABC):
        x_i_j = TermDefinition(
            set_name="x_i_j",
            name=lambda i, j: f"x_{i}_{j}",
            display_name="Amount of commodity to ship from 'i' to 'j'",
        )


# Usage within a model
print(GenericModelDefinition.Dimensions.n.min)  # Access the minimum value for dimension 'n'
print(GenericModelDefinition.Parameters.c_i_j.name(1, 1))  # Generate the name for parameter 'c_1_1'
print(GenericModelDefinition.DecisionVariables.x_i_j.display_name)  # Access the display name for the decision variable 'x_i_j'
```

<p style='text-align: justify;'>
    &emsp;&emsp;By leveraging PyORlib's structured approach, you can improve the maintainability and scalability of 
	your models. The clean and organized codebase makes for easy navigation, understanding, and modification, making
	it easier to collaborate with other team members and adapt your models to changing requirements.
</p>

## Ensuring Model Integrity

<p style='text-align: justify;'>
    &emsp;&emsp;In addition to PyORlib's workflow capabilities, this package provides a set of abstractions 
	designed to apply validations and ensure the integrity of your model data. These validation features play a 
	crucial role in identifying errors early on and maintaining consistent, error-free model data, resulting in
	more robust optimization.
</p>

<ol style='text-align: justify;'>

<li><b>Defining Validation Rules</b> ─ 
PyORlib utilizes Python <code>descriptors</code> and <code>dataclasses</code> to define validation rules for model 
schemas. Attributes like <code>DimensionField</code> and <code>ParameterField</code> allow specifying requirements 
like minimum/maximum values.

```Python linenums="1" hl_lines="9-15"
from dataclasses import dataclass

from pyorlib.enums import ParameterType, ValueType
from pyorlib.structures import MultiValueParameter
from pyorlib.validators import DimensionField, ParameterField


@dataclass
class ExampleSchema:
    n: int = DimensionField(min=1)  # Specifies the minimum value allowed for 'n'
    a_i: MultiValueParameter = ParameterField(
        parameter_types={ParameterType.FIXED},  # Specifies the allowed param types for 'a_i'
        value_types={ValueType.INTEGER},  # Specifies the allowed value types for 'a_i'
        min=0,  # Specifies the minimum value allowed for 'a_i'
    )
```
</li>

<li><b>Putting it into Practice</b> ─ 
To apply validations, instantiate the <code>ExampleSchema</code> class with the model data. If initialization succeeds
without errors, the data passed all validations and can be used safely for optimization. However, if the data is 
invalid, an error will be raised immediately upon initialization, before the invalid data can be optimized.

```Python linenums="1"
schema = ExampleSchema(
	n=2,
	a_i=MultiValueParameter(
        value_type=ValueType.INTEGER,
        parameter_type=ParameterType.FIXED,
        values=(1, 2),
    ),
) # succeeds

schema = ExampleSchema(
	n=0,
	a_i=MultiValueParameter(
        value_type=ValueType.INTEGER,
        parameter_type=ParameterType.FIXED,
        values=(1, 2.6),
    ),
) # raises ValueError
```
</li>
</ol>

<p style='text-align: justify;'>
    &emsp;&emsp;By validating data upon instantiation, any issues are caught immediately before the model is optimized.
	This helps maintain data integrity and prevents errors downstream in the optimization process.
</p>

## Runtime Flexibility & Customization

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

<p style='text-align: justify;'>
	&emsp;&emsp;PyORlib continuously adapts to support developers across various technological and programming domains. 
	Its primary goal is to remain a useful tool for learning about operations research, mathematical model optimization,
	and testing different optimization packages with ease.
</p>

<p style='text-align: justify;'>
	&emsp;&emsp;While future development may introduce some changes to enhance and expand certain current 
	functionalities, the highest priority remains providing a simple yet powerful platform for students, researchers,
	and practitioners to explore optimization concepts, test algorithms, and further their own knowledge. Large-scale
	changes that could introduce significant complexity are less likely in order to maintain accessibility as the core
	focus.
</p>

<details markdown="1" class="tip" open>
<summary>Driving Innovation Through Collaboration</summary>

<p style='text-align: justify;'>
    &emsp;&emsp;PyORlib is an open source project that welcomes community involvement. If you wish to contribute
	additional optimization suites, improvements, or bug fixes, please check the <a href="https://dapensoft.github.io/pyorlib/contributing/" target="_blank">Contributing</a> 
	section for guidelines on collaborating.
</p>
</details>

## License

<p style='text-align: justify;' markdown>
    &emsp;&emsp;PyORlib is distributed as open source software and is released under the <a href="https://choosealicense.com/licenses/mit/" target="_blank">MIT License</a>. 
    You can view the full text of the license in the <a href="https://github.com/dapensoft/pyorlib/blob/master/LICENSE" target="_blank"><code>LICENSE</code></a> 
    file located in the PyORlib repository.
</p>
