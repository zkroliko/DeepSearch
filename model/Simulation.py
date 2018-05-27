import os.path
import pickle
import random
import sys
import time

from examples.Scenario1 import Scenario1
from model.SolutionHolder import SolutionHolder
from model.agents.enemy import Enemy
from model.agents.walker import Walker
from model.contact_effects.contact_effects import TransportEffect, WinEffect, KillEffect
from model.decision_makers import random_behaviour
from model.decision_makers.circle_left_behaviour import CircleLeftBehaviour
from model.decision_makers.circle_right_behaviour import CircleRightBehaviour
from model.decision_makers.deep_behaviour import DeepBehaviour
from model.decision_makers.follow_behaviour import FollowBehaviour
from model.decision_makers.random_behaviour import RandomBehaviour
from model.decision_makers.run_away_behaviour import RunAwayBehaviour
from model.decision_makers.stand_behaviour import StandBehaviour
from model.field import Field
from model.lightMap import LightMap
from model.tools.text_printer import TextPrinter
from model.utils.positioningUtil import random_field


class Simulation:
    DEFAULT_SCENARIO = Scenario1
    DEFAULT_N_ITERATIONS = 400

    DEFAULT_RESULTS_FILE = "iteration_results.csv"
    DEFAULT_OPTIMIZED_FILE = "best_path.csv"

    N_OPPONENTS = 3

    decision_makers = [RandomBehaviour, StandBehaviour, FollowBehaviour, RunAwayBehaviour,
                       CircleLeftBehaviour, CircleRightBehaviour]

    contact_effects = [KillEffect, WinEffect, TransportEffect]

    # Algorithm specific

    def __init__(self, scenario=DEFAULT_SCENARIO, on_iteration=(lambda x, y: None),
                 n_iterations=DEFAULT_N_ITERATIONS, ):
        self.scenario = scenario
        self.on_iteration = on_iteration
        self.shadow_file_name = str(self.scenario.name()) + "shadow_map"
        self.n_iterations = n_iterations
        self.iteration = 0
        self.result_file = self.DEFAULT_RESULTS_FILE
        self.path_file = self.DEFAULT_OPTIMIZED_FILE
        self.sh = SolutionHolder()
        self.global_track = []
        self.enemies_config = self._configure_enemies()
        print("Configured {} opponents".format(self.N_OPPONENTS))

    def generate_textual_description(self, actors, walker):
        text_printer = TextPrinter(self.scenario.area())
        text_printer.set_view(walker.light_map.to_discover)
        for actor in actors:
            text_printer.set_position(actor.position, actor.symbol)
        return text_printer.fields

    def get_map(self):
        printer = TextPrinter(self.scenario.area())
        return printer.fields

    def _configure_enemies(self):
        enemy_config = []
        decision_maker = random.choice(self.decision_makers)()
        contact_effect = random.choice(self.contact_effects)(random_field)
        for i in range(self.N_OPPONENTS):
            enemy_config.append((decision_maker, contact_effect, str(i)))
        return enemy_config

    def _generate_enemies(self, enemy_config, main_walker):
        # Placement
        enemies = []
        for d, c, s in enemy_config:
            position = random_field(self.scenario.area(), self.scenario.start())
            enemy = Enemy(self.scenario.area(), position, d, contact_effect=c, symbol=s)
            # Extra info about the main walker
            enemy.decider.target = main_walker
            enemies.append(enemy)
        return enemies

    def start(self, app):
        # For saving results
        with open(self.result_file, 'w') as result_file:
            if os.path.isfile(self.shadow_file_name):
                print("Loading shadow map from file ", self.shadow_file_name)
                with open(self.shadow_file_name, 'rb') as shadow_file:
                    shadow_map = pickle.load(shadow_file)
            else:
                print("Building the shadow map")
                shadow_map = LightMap.build_shadow_map(self.scenario.area())
                with open(self.shadow_file_name, 'wb') as shadow_file:
                    pickle.dump(shadow_map, shadow_file)
                print("Shadow map saved")
            for iteration in range(self.n_iterations):
                w = Walker(self.scenario.area(), self.scenario.start(), random_behaviour.RandomBehaviour(), shadow_map)
                enemies = self._generate_enemies(self.enemies_config, w)
                # Configuring walker for deep behaviour
                w.decider = DeepBehaviour(w, enemies)
                actors = [w]+enemies
                start = time.time()
                self.global_track.clear()
                while not w.finished():
                    # Agent step
                    w.step()
                    self.track(actors, w)
                    # Walker steps
                    for e in enemies:
                        # We need to check both before and after their moves
                        e.check_effect(w)
                        if not w.dead:
                            e.step()
                            self.track(actors, w)
                            e.check_effect(w)
                            self.track(actors, w)
                reward = self.sh.assess_solution(w)
                w.decider.commit_learning_data(reward)
                # Recording data
                data = "%s, %s" % (reward, time.time() - start)
                alive_msg = "dead" if w.dead else "alive"
                result_file.write(data + alive_msg + "\n")
                print(data, alive_msg)
                self.on_iteration(iteration, reward)

            printer = TextPrinter(self.scenario.area())
            printer.set_start(self.scenario.start())

            if self.n_iterations == 1:
                app.commit_sim_data(self)
                app.play(self)
            print("# Best solution's score is %s" % self.sh.bast_reward)
            print("# Best solution is %s" % self.sh.path_to_str())
            print("Iteration progress saved in {}".format(self.result_file))

            with open(self.path_file, 'w') as path_file:
                path_file.write(self.sh.path_to_csv())
                print("Best solution saved in {}".format(self.path_file))

    def agent_moves(self):
        return self.global_track

    def track(self, actors, walker):
        self.global_track.append(self.generate_textual_description(actors, walker))
        walker.decider.consume_learning_data()

