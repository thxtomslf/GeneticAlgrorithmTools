import random
from typing import List, Tuple


from creature_factory.creature_factory import CreatureFactory
from creature.creature import Creature


class OptimizationEngine:

    _creature_factory: CreatureFactory

    _start_population_number: int = 2 ** 8

    def __init__(self,
                 creature_factory: CreatureFactory,
                 start_population: int = None):
        self._creature_factory = creature_factory

        if start_population:
            self._start_population_number = start_population

    def optimize(self) -> Tuple[float, float]:
        population: List[Creature] = self._creature_factory.create_start_population(self._start_population_number)

        counter = 0
        minimum_fitness = None
        minimum_point = None
        for i in range(10):
            children: List[Creature] = []
            for _ in range(0, len(population) - 1, 2):
                parent_1, parent_2 = self.choose_parents_pair(population)

                child_1, child_2 = self._creature_factory.hybridize(parent_1, parent_2)
                if child_1:
                    children.append(child_1)

                if child_2:
                    children.append(child_2)

                child_1_fitness = child_1.get_fitness()
                if minimum_fitness is None or child_1_fitness < minimum_fitness:
                    minimum_fitness = child_1_fitness
                    minimum_point = child_1._coordinates  # это надо поправить - нарушение инкапсуляции

                child_2_fitness = child_2.get_fitness()
                if minimum_fitness is None or child_2_fitness < minimum_fitness:
                    minimum_fitness = child_2_fitness
                    minimum_point = child_2._coordinates  # это надо поправить - нарушение инкапсуляции

            for child in children:
                child.mutate()

            population.clear()
            population.extend(children)
            counter += 1

        return minimum_point

    def choose_parents_pair(self, population: List[Creature]) -> Tuple[Creature, Creature]:
        mean = sum(map(lambda x: x.get_fitness(), population)) / len(population)
        dev = sum([((x.get_fitness() - mean) ** 2) for x in population]) / len(population)

        scaled_population = []
        if dev == 0:
            scaled_population = [1 for _ in range(len(population))]
        else:
            for elem in population:
                value = 1 - ((abs(elem.get_fitness() - mean)) / dev)
                if value <= 0:
                    value = 1e-100
                scaled_population.append(value)
        picked_parents = random.choices(population,
                                        weights=[value for value in scaled_population], k=2)
        return picked_parents[0], picked_parents[1]
