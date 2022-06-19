rl_algorithm(go_right, sarsa).

rl_parameter(policy, egreedy).
rl_parameter(alpha, 0.26).
rl_parameter(gamma, 0.9).
rl_parameter(epsilon, 0.4).
rl_parameter(epsilon_decay, 0.9999).
rl_parameter(epsilon_min, 0).

rl_observe(go_right, player(list(4))).
rl_observe(go_right, obstacle(list(4))).
rl_observe(go_right, enemie(list(4))).

rl_reward(go_right, R) :- reward(R).

rl_terminal(go_right) :- gameover.

!start.

+!start : ready <- rl.execute(go_right); !start. //!start in order to continue after the end of the episode

@action[rl_goal(go_right), rl_param(direction(set(
    noop, right, left, down, a, b,
    right_a, right_b, right_a_b,
    left_a, left_b, left_a_b
)))]
+!move(Direction) <- move(Direction).

//noop, right, left, down, a, b,
//right_a, right_b, right_a_b,
//left_a, left_b, left_a_b,

{ include("$jacamoJar/templates/common-cartago.asl") }

