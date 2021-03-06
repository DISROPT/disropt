.. _tutorial_problems:

Local data of optimization problems
====================================

The class :class:`Problem` allows one to define and solve optimization problems of various types.
It is discussed in detail in :ref:`a dedicated section <advanced_problems>`.

In the distributed framework of **disropt**, the :class:`Problem` class is also meant
to specify local data (available to the agent) of global optimization problems.
The class should be used in different ways, depending on the distributed optimization
set-up (refer to the :ref:`general forms <tutorial_setups>`), and must be provided to
the agent (see also :ref:`quickstart`).

Cost-coupled set-up
---------------------------
For the cost-coupled set-up, the two objects that can be specified are

* the local contribution to the cost function, i.e., the function :math:`f_i(x)`
* the local constraints (if any), i.e., the set :math:`X_i` (which must be described through a list of constraints).

To this end, create an instance of the class :class:`Problem` and set the objective function
to :math:`f_i(x)` and the constraints to :math:`X_i`.

For instance, suppose :math:`x \in \mathbb{R}^2` and assume the agent knows

.. math::

    f_i(x) = \|x\|^2,
    \hspace{1cm}
    X_i = \{x \mid -1 \le x \le 1\}.

The corresponding Python code is::

    from disropt.functions import SquaredNorm, Variable
    from disropt.problems import Problem
    x = Variable(2)
    objective_function = SquaredNorm(x)
    constraints = [x >= -1, x <= 1]
    problem = Problem(objective_function, constraints)

If there are no local constraints (in the example :math:`X_i \equiv \mathbb{R}^2`), then
no constraints should be passed to :class:`Problem`::

    x = Variable(2)
    objective_function = SquaredNorm(x)
    problem = Problem(objective_function) # no constraints


Common-cost set-up
---------------------------
For the common-cost set-up, the objective function :math:`f(x)` is assumed to be known by
all the agents. Theerefore, the two objects that must be specified are

* the global cost function, i.e., the function :math:`f(x)`
* the local constraints, i.e., the set :math:`X_i` (which must be described through a list of constraints).

To this end, create an instance of the class :class:`Problem` and set the objective function
to :math:`f(x)` and the constraints to :math:`X_i`.

For instance, suppose :math:`x \in \mathbb{R}^2` and assume the agent knows

.. math::

    f(x) = \|x\|^2,
    \hspace{1cm}
    X_i = \{x \mid -1 \le x \le 1\}.

The corresponding Python code is::

    from disropt.functions import SquaredNorm, Variable
    from disropt.problems import Problem
    x = Variable(2)
    objective_function = SquaredNorm(x)
    constraints = [x >= -1, x <= 1]
    problem = Problem(objective_function, constraints)


Constraint-coupled set-up
---------------------------

For the constraint-coupled set-up, the three objects that can be specified are

* the local contribution to the cost function, i.e., the function :math:`f_i(x_i)`
* the local contribution to the coupling constraints, i.e., the function :math:`g_i(x_i)`
* the local constraints (if any), i.e., the set :math:`X_i` (which must be described through a list of constraints).

To this end, create an instance of the class :class:`ConstraintCoupledProblem` and set the objective function
to :math:`f_i(x_i)`, the coupling function to :math:`g_i(x_i)` and the constraints to :math:`X_i`.

For instance, suppose :math:`x_i \in \mathbb{R}^2` and assume the agent knows

.. math::

    f_i(x_i) = \|x_i\|^2,
    \hspace{1cm}
    g_i(x_i) = x_i,
    \hspace{1cm}
    X_i = \{x \mid -1 \le x \le 1\}.

The corresponding Python code is::

    from disropt.functions import SquaredNorm, Variable
    from disropt.problems import ConstraintCoupledProblem
    x = Variable(2)
    objective_function = SquaredNorm(x)
    coupling_function = x
    constraints = [x >= -1, x <= 1]
    problem = ConstraintCoupledProblem(objective_function, constraints, coupling_function)

If there are no local constraints (in the example :math:`X_i \equiv \mathbb{R}^2`), then
no constraints should be passed to :class:`ConstraintCoupledProblem`::

    x = Variable(2)
    objective_function = SquaredNorm(x)
    coupling_function = x
    problem = ConstraintCoupledProblem(
        objective_function=objective_function,
        coupling_function=coupling_function) # no local constraints