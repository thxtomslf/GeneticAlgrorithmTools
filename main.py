import math

from optimization.optimization_engine import OptimizationEngine
from creature_factory.two_variables_function_factory import TwoVariablesFunctionPointsFactory
from hybridization.simple_hybridization import SimpleHybridization
import matplotlib.pyplot as plt

# Add labels
plt.title('Histogram of Arrival Delays')
plt.xlabel('Delay (min)')
plt.ylabel('Flights')


n = 2
search_area = ((-5.12, 5.12), (-5.12, 5.12))
engine = OptimizationEngine(
    TwoVariablesFunctionPointsFactory(
        SimpleHybridization(),
        lambda x, y: 10 * 2 + x ** 2 - 10 * math.cos(2 * math.pi * x) + y ** 2 - 10 * math.cos(2 * math.pi * y),
        search_area
    )
)


answers = []
for i in range(200):
    answers.append(engine.optimize())

answers = list(map(lambda x: (x[0] + x[1]) / 2, answers))

# matplotlib histogram
plt.hist(answers, color='blue', edgecolor='black', bins=int(180/5))

plt.title('Histogram of result points')
plt.xlabel('Average between x, y')
plt.ylabel('Amount')

plt.show()
