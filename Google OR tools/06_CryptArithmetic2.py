"""Cryptarithmetic puzzle.

First attempt to solve equation CP + IS + FUN = TRUE
where each letter represents a unique digit.

This problem has 72 different solutions in base 10.
"""
from xml.parsers.expat import model

from ortools.sat.python import cp_model
from sklearn import base



class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables: list[cp_model.IntVar]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self) -> None:
        self.__solution_count += 1
        for v in self.__variables:
            print(f"{v}={self.value(v)}", end=" ")
        print()

    @property
    def solution_count(self) -> int:
        return self.__solution_count


def main() -> None:
    """solve the CP+IS+FUN==TRUE cryptarithm."""
    # Constraint programming engine
    model = cp_model.CpModel()

    base = 10
    b = model.new_int_var(1, base - 1, "B")
    a = model.new_int_var(0, base - 1, "A")
    s = model.new_int_var(0, base - 1, "S")
    e = model.new_int_var(0, base - 1, "E")
    l = model.new_int_var(0, base - 1, "L")
    g = model.new_int_var(1, base - 1, "G")
    m = model.new_int_var(0, base - 1, "M")
    
   

    # We need to group variables in a list to use the constraint AllDifferent.
    letters = [b, a, s, e, l, g, m]

    # Verify that we have enough digits.
    assert base >= len(letters)

    # Define constraints.
    model.add_all_different(letters)

    # CP + IS + FUN = TRUE
    model.add(
        b * base * base * base + a * base * base + s * base + e + b * base * base * base + a * base * base + l * base + l 
        == g * base * base * base * base + a * base * base * base + m * base * base + e * base + s
    )

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter(letters)
    # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True
    # Solve.
    status = solver.solve(model, solution_printer)

    # Statistics.
    print("\nStatistics")
    print(f"  status   : {solver.status_name(status)}")
    print(f"  conflicts: {solver.num_conflicts}")
    print(f"  branches : {solver.num_branches}")
    print(f"  wall time: {solver.wall_time} s")
    print(f"  sol found: {solution_printer.solution_count}")


if __name__ == "__main__":
    main()