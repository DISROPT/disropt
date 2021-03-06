Consensus algorithms
=====================

Classical consensus 
--------------------

The classical consensus algorithm is implemented through the :class:`Consensus` class.

From the perspective of agent :math:`i` the classical consensus algorithm works as follows. For :math:`k=0,1,\dots`

.. math::

    x_i^{k+1} = \sum_{j=1}^N w_{ij} x_j^k
    
where :math:`x_i\in\mathbb{R}^n` and :math:`w_{ij}` is the weight assigned by agent :math:`i` to agent :math:`j`. Usually, average consensus (i.e., the convergence of the local estimate sequences to the initial average) is guaranteed only if the weights :math:`w_{ij}` form a doubly-stochastic matrix. Otherwise, agreement is still reached but at some other point.

In order to simulate a consensus algorithm over a static undirected graph (with a doubly-stochastic weight matrix), create a file containing the following code and call it :ref:`launcher-py` 

.. literalinclude:: ../../../../examples/algorithms/consensus/launcher.py
    :caption: launcher.py
    :name: launcher-py

And then execute it with the desired number of agents::

    mpirun -np 12 --oversubscribe python launcher.py

where the flag ``--oversubscribe`` is necessary only if the requested number of agents (12 in this case) is higher than the available number of cores (or computing units).


**Plot the generated sequences**

In order to plot the local sequences generated by the algorithm, we create the file :ref:`results-py`.

.. literalinclude:: ../../../../examples/algorithms/consensus/results.py
    :caption: results.py
    :name: results-py

We execute :ref:`results-py` through::

    python results.py

.. image:: ../../../../examples/algorithms/consensus/results_fig.png

Time-varying graphs
-------------------

Convergence of consensus algorithms is still achieved over time-varying (possibly directed) graphs, provided that they are jointly strongly connected.

In this case, one can use the :class:`set_neighbors` and :class:`set_weights` methods of the :class:`Agent` class in order to modify the communication network when necessary. This can be done in various ways, for example by overriding the :class:`run` method of the algorithm of by calling it multiple times over different graphs. For example, suppose that the graph changes every 100 iterations and that you want to perform 1000 iterations, then::

    for g in range(10):
        # generate a new common graph (everyone use the same seed)
        Adj = construct_graph(nproc, p=0.3, seed=g)
        W = metropolis_hastings(Adj)

        # set new neighbors and weights
        agent.set_neighbors(in_neighbors=np.nonzero(Adj[local_rank, :])[0].tolist(),
                            out_neighbors=np.nonzero(Adj[:, local_rank])[0].tolist())
        agent.set_weights(weights=W[local_rank, :].tolist())

        algorithm.run(iterations=100)

Block-wise consensus
---------------------

Consensus can be also performed block-wise with respect to the decision variable by using the :class:`BlockConsensus` class.

From the perspective of agent :math:`i` the algorithm works as follows. At iteration :math:`k`, if the agent is awake, it selects a random block :math:`\ell_i^k` of its local solution and updates

.. math::

    x_{i,\ell}^{k+1} = \begin{cases}
            \sum_{j\in\mathcal{N}_i} w_{ij} x_{j\mid i,\ell}^k & \text{if} \ell = \ell_i^k \\
            x_{i,\ell}^{k} & \text{otherwise}
            \end{cases}

where :math:`\mathcal{N}_i` is the current set of in-neighbors and :math:`x_{j\mid i},j\in\mathcal{N}_i` is the local copy of :math:`x_j` available at node :math:`i` and :math:`x_{i,\ell}` denotes the :math:`\ell`-th block of :math:`x_i`. Otherwise :math:`x_{i}^{k+1}=x_i^k`.

Moreover, at each iteration, each agent can update its local estimate or not at each iteration according to a certain probability (awakening_probability), thus modeling some `asyncrhony`.

The algorithm can be istantiated by providing a list of blocks of the decision variable and the probabilities of drawing each block::

    algorithm = BlockConsensus(agent=agent,
                               initial_condition=x0,
                               enable_log=True,
                               blocks_list=[(0, 1), (2, 3)],
                               probabilities=[0.3, 0.7],
                               awakening_probability=0.5)



Asynchronous consensus
----------------------

Asynchronous consensus can be seen as a sort of synchronous consensus over time-varying graphs with delays (which may model non negligible computation times and unreliable links) and it is implemented in the :class:`AsynchronousConsensus` class.

When running this algorithm, you can control the computation and sleep times of each agent and the communication channels failure probabilities. Moreover, when running asynchronous algorithms, you have to set the total duration of the execution (and not the number of iterations). We provide the following example.

.. literalinclude:: ../../../../examples/algorithms/consensus_async/launcher.py

**Plot the generated sequences**

.. literalinclude:: ../../../../examples/algorithms/consensus_async/results.py

.. image:: ../../../../examples/algorithms/consensus_async/sequences.png

.. image:: ../../../../examples/algorithms/consensus_async/sleep_awake.png

