# glpk code here with pyomo that solves the sudoku puzzle
import pyomo.environ as pe

model = pe.ConcreteModel()

# declare decision variables
model.x = pe.Var(domain=pe.NonNegativeReals)

# declare objective
model.profit = pe.Objective(
    expr = 40*model.x,
    sense = pe.minimize)

# declare constraints
model.demand = pe.Constraint(expr = model.x <= 40)
model.laborA = pe.Constraint(expr = model.x <= 80)
model.laborB = pe.Constraint(expr = 2*model.x <= 100)

# solve
pe.SolverFactory('appsi_highs').solve(model).write()