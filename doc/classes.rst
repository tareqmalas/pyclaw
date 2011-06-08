.. _pyclaw_classes:
  
*****************************************
Introduction to the main Pyclaw Classes
*****************************************
.. contents::


Flow of a Pyclaw Simulation
===========================

The basic idea of a pyclaw simulation is to construct a
:class:`~pyclaw.solution.Solution` object, hand it to a
:class:`~pyclaw.solver.Solver` object, and request a solution at a new
time.  The solver will take whatever steps are necessary to evolve the solution
to the requested time.

.. image:: images/pyclaw_architecture_flow.*

The bulk of the work in order to run a simulation then is the creation and
setup of the appropriate :class:`~pyclaw.grid.Grid`,
:class:`~pyclaw.solution.Solution`, and :class:`~pyclaw.solver.Solver`
objects needed to evolve the solution to the requested time.

.. note::

    Here we will assume that you have run ``import numpy as np`` before we do
    any of the tutorial commands.

Creation of a Pyclaw :class:`~pyclaw.solution.Solution`
=======================================================

A Pyclaw :class:`~pyclaw.solution.Solution` is a container for a collection of
:class:`~pyclaw.grid.Grid` objects in order to support adaptive mesh 
refinement and multi-block simulations. The :class:`~pyclaw.solution.Solution` 
object keeps track of a list of :class:`~pyclaw.grid.Grid` objects then 
and controls the overall input and output of the entire collection of 
:class:`~pyclaw.grid.Grid` objects.  Inside of a 
:class:`~pyclaw.grid.Grid` object, a set of 
:class:`~pyclaw.grid.Dimension` objects define the extents and basic 
grids of the :class:`~pyclaw.grid.Grid`.

.. image:: images/pyclaw_solution_structure.*

The process needed to create a :class:`~pyclaw.solution.Solution` object then
follows from the bottom up.

::

    >>> from pyclaw.solution import Solution, Grid, Dimension
    
    >>> x = Dimension('x', -1.0, 1.0, 200)
    >>> y = Dimension('y', 0.0, 1.0, 100)
    
This code creates two dimensions, a dimension ``x``  on the interval 
``[-1.0, 1.0]`` with ``200`` grid points and a dimension ``y`` on the interval
``[0.0, 1.0]`` with ``100`` grid points.  

.. note:: 

    Many of the attributes of a :class:`~pyclaw.grid.Dimension`
    object are set automatically so make sure that the values you want are set
    by default.  Please refer to the :class:`~pyclaw.grid.Dimension`
    classes definition for what the default values are.

Next we have to create a :class:`~pyclaw.grid.Grid` object that will
contain our :class:`~pyclaw.grid.Dimension` objects.

::

    >>> grid = Grid([x,y])
    >>> grid.meqn = 2

Here we create a grid with the dimensions we created earlier to make a single
2D :class:`~pyclaw.grid.Grid` object and set the number of equations it
will represent to 2.  As before, many of the attributes of the
:class:`~pyclaw.grid.Grid` object are set automatically.

We now need to set the initial condition ``q`` and possibly ``aux`` to the correct
values.  There are multiple convenience functions to help in this, here we
will use the method :meth:`~pyclaw.grid.Grid.zeros_q` to set all the
values of ``q`` to zero.

::

    >> sigma = 0.2
    >> omega = np.pi
    >> grid.zeros_q()
    >> q[:,0] = np.cos(omega * grid.x.center)
    >> q[:,1] = np.exp(-grid.x.center**2 / sigma**2)
    
We now have initialized the first entry of q to a cosine function 
evaluated at the cell centers and the second entry of q to a gaussian, again
evaluated at the grid cell centers.

Many Riemann solvers also require information about the problem we are going
to run which happen to be grid properties such as the impedence ``Z`` and 
speed of sound ``c`` for linear acoustics.  We can set these values in the 
``aux_global`` dictionary in one of two ways.  The first way is to set them
directly as in:

::

    >>> grid.aux_global['c'] = 1.0
    >>> grid.aux_global[`Z`] = 0.25
    
If you're using a Fortran Riemann solver, these values will automatically get
copied to the corresponding variables in the cparam common block of the
Riemann solver.  This is done in solver.setup(), which calls grid.set_cparam().

Last we have to put our :class:`~pyclaw.grid.Grid` object into a 
:class:`~pyclaw.solution.Solution` object to complete the process.  In this
case, since we are not using adaptive mesh refinement or a multi-block
algorithm, we do not have multiple grids.

::

    >>> sol = Solution(grid)
    
We now have a solution ready to be evolved in a 
:class:`~pyclaw.solver.Solver` object.


Creation of a Pyclaw :class:`~pyclaw.solver.Solver`
==========================================================

A Pyclaw :class:`~pyclaw.solver.Solver` can represent many different
types of solvers so here we will concentrate on a 1D, classic Clawpack type of
solver.  This solver is located in the :mod:`~pyclaw.clawpack` module.

First we import the particular solver we want and create it with the default 
configuration.

::

    >>> from pyclaw.clawpack import ClawSolver1D
    >>> solver = ClawSolver1D()
    >>> solver.mthbc_lower[0] = pyclaw.BC.periodic
    >>> solver.mthbc_upper[0] = pyclaw.BC.periodic

Next we need to tell the solver which Riemann solver to use from the
:doc:`Riemann solver package </pyclaw/evolve/rp>` .  We can always check what 
Riemann solvers are available to use via the 
:meth:`~pyclaw.ClawSolver1D.list_riemann_solvers` method.  Once we have
picked one out, we let the solver pick it out for us via:

::

    >>> solver.set_riemann_solver('acoustics')

In this case we have decided to use the linear acoustics Riemann solver.  You 
can also set your own solver by importing the module that contains it and 
setting it directly to the :attr:`~pyclaw.clawpack.ClawSolver1D.rp`
attribute to the particular function.

::

    >>> import my_rp_module
    >>> solver.rp = my_rp_module.my_acoustics_rp

Last we finish up by specifying the specific values for our solver to use.

::

    >>> solver.mthlim = pyclaw.limiters.vanleer
    >>> solver.dt = 0.01
    >>> solver.cfl_desired = 0.9
    
If we wanted to control the simulation we could at this point by issuing the 
following commands:

::

    >>> solver.evolve_to_time(sol,1.0)
    
This would evolve our solution ``sol`` to ``t = 1.0`` but we are then
responsible for all output and other setup considerations.

Creating and Running a Simulation with :class:`~pyclaw.controller.Controller`
=============================================================================

The :class:`~pyclaw.controller.Controller` coordinates the output and setup of
a run with the same parameters as the classic Clawpack.  In order to have it 
control a run, we need only to create the controller, assign it a solver and
initial condition, and call the :meth:`~pyclaw.controller.Controller.run`
method.

::

    >>> from pyclaw.controller import Controller

    >>> claw = Controller()
    >>> claw.solver = solver
    >>> claw.solutions['n'] = sol
    
Here we have imported and created the :class:`~pyclaw.controller.Controller` 
class, assigned the :class:`~pyclaw.solver.Solver` and 
:class:`~pyclaw.solution.Solution`.

These next commands setup the type of output the controller will output.  The
parameters are similar to the ones found in the classic clawpack claw.data 
format.

::

    >> claw.outstyle = 1
    >> claw.nout = 10
    >> claw.tfinal = 1.0
    
When we are ready to run the simulation, we can call the 
:meth:`~pyclaw.controller.Controller.run` method.  It will then run the
simulation and output the appropriate time points.  If the 
:attr:`~pyclaw.controller.Controller.keep_copy` is set to *True* the 
controller will keep a copy of each solution output in the frames array.  For
instance, you can then immediately plot the solutions output into the *frames*
array.