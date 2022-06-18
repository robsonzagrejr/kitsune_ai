rl_algorithm(game_env, sarsa).

rl_parameter(policy, egreedy).
rl_parameter(alpha, 0.26).
rl_parameter(gamma, 0.9).
rl_parameter(epsilon, 0.4).
rl_parameter(epsilon_decay, 0.9999).
rl_parameter(epsilon_min, 0).

rl_observe(game_env, player_pos(list(1080))).

rl_reward(game_env, R) :- reward(R).

rl_terminal(game_env) :- gameover.

!start.

+!start : true <- rl.execute(game_env); !start. //!start in order to continue after the end of the episode

@action[rl_goal(game_env), rl_param(direction(set(
    noop, right, left, down, a)))
]
+!move(Direction) <- move(Direction).

{ include("$jacamoJar/templates/common-cartago.asl") }

