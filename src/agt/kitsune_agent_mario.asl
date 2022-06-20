rl_algorithm(go_right, sarsa).
rl_algorithm(find_enemie, sarsa).

rl_parameter(policy, egreedy).
rl_parameter(alpha, 0.26).
rl_parameter(gamma, 0.9).
rl_parameter(epsilon, 0.4).
rl_parameter(epsilon_decay, 0.9999).
rl_parameter(epsilon_min, 0).

rl_observe(go_right, player(_, _, _, _, _)).
rl_observe(go_right, object(_, _, _, _, _)).

rl_reward(go_right, R) :- reward(R).

rl_terminal(go_right) :- gameover.

//!start.

+ready : true <- !start.

+!start : ready <- rl.execute(go_right); !start. //!start in order to continue after the end of the episode

@action[rl_goal(go_right), rl_param(direction(set(
    right
)))]
+!move(Direction) <- move(Direction).

//noop, right, left, down, a, b,
//right_a, right_b, right_a_b,
//left_a, left_b, left_a_b,


// Identifying Enemies

+object(N, X, Y, W, H):
    player(_, PX, PY, PW, PH) &
    (
     (PY <= Y)
    ) &
    not path(N)
    <-
    +path(N);
    .

+path(N): true <- print("\nNew Path: ", N);.

+object(N, X, Y, W, H):
    player(_, PX, PY, PW, PH) &
    (
     (PX+PW+5 >= X)
    ) &
    not path(N)
    <-
    +enemie(N);
    .

+enemie(N): true <- print("\nNew Enemie: ", N);.


{ include("$jacamoJar/templates/common-cartago.asl") }

