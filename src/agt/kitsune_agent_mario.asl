// Configuring RL soft plans
rl_algorithm(go_right, dqn).

rl_parameter(policy, egreedy).
//rl_parameter(alpha, 0.26).
//rl_parameter(gamma, 0.9).
//rl_parameter(epsilon, 0.4).
//rl_parameter(epsilon_decay, 0.9999).
//rl_parameter(epsilon_min, 0).

//rl_observe(go_right, player(_, _, _, _, _)).
//rl_observe(go_right, object(_, _, _, _, _)).
//rl_observe(go_right, obj_player_touching(_, _, _, _, _, _, _, _, _, _, _)).
rl_observe(go_right, path(set(rock))).
//rl_observe(go_right, enemie(_)).

rl_reward(go_right, R) :- reward(R).

rl_terminal(go_right) :- gameover.


// Define where the player is touching the object

// (0,0) is top left conner
touching(X1, Y1, W1, H1, X2, Y2, W2, H2, DX, DY, PX, PY):-
    x_range(X1, W1, X2, W2, DX, PX) &
    (PX \== none) &
    y_range(Y1, H1, Y2, H2, DY, PY) &
    (PY \== none)
.
touching(X1, Y1, W1, H1, X2, Y2, W2, H2, 0, 0, none, none).

player_touching(X, Y, W, H, DX, DY, TPX, TPY):-
    player(_, PX, PY, PW, PH, PVX, PVY) &
    touching(PX, PY, PW, PH, X, Y, W, H, DX, DY, TPX, TPY)
.
player_touching(X, Y, W, H, 0, 0, none, none).

obj_player_touching(N, X, Y, W, H, VX, VY, DX, DY, TPX, TPY):-
    object(N, X, Y, W, H, VX, VY) &
    player(_, PX, PY, PW, PH, PVX, PVY) &
    touching(PX, PY, PW, PH, X, Y, W, H, DX, DY, TPX, TPY)
.
obj_player_touching(none, none, none, none, none, 0, 0, none, none).


// TODO explain DX PX
x_range(X1, W1, X2, W2, ((X2+W2+1) - X1), right):-
    (X1 >= X2) &
    (X1 <= (X2+W2+1))
.
x_range(X1, W1, X2, W2, ((X1+W1+1) - X2), left):-
    (X1 < X2) &
    ((X1+W1+1) >= X2)
.
x_range(_,_,_,_,0, none).

y_range(Y1, H1, Y2, H2, ((Y2+H2+1) - Y1), top):-
    (Y1 >= Y2) &
    (Y1 <= (Y2+H2+1))
.
y_range(Y1, H1, Y2, H2, ((Y1+H1+1) - Y2), bottom):-
    (Y1 < Y2) &
    ((Y1+H1+1) >= Y2)
.
y_range(_,_,_,_,0, none).


// Identifying Enemies
+enemie(N): true <- print("\nNew Enemie: ", N);.

+object(N, X, Y, W, H, VX, VY):
    gameover &
    player_touching(X, Y, W, H, DX, DY, TPX, TPY) &
    (TPX \== none) & (TPY \== none) &
    not path(N)
    <-
    print("\nENEMY: ",N);
    +enemie(N);
.


// Identifying Paths
+path(N): true <- print("\nNew Path: ", N);.

// name, x, y, w, h, velocity_x, velocity_y
+object(N, X, Y, W, H, VX, VY):
    player_touching(X, Y, W, H, DX, DY, TPX, bottom) &
    (TPX \== none) & (TPY \== none) &
    player(_, PX, PY, PW, PH, PVX, PVY) &
    (PVY == 0) &
    (VX == 0) &
    not enemie(N)
    <-
    +path(N);
.

+ready : true <- !start.

+!start : ready <- rl.execute(go_right); !start. //!start in order to continue after the end of the episode

@action1[rl_goal(go_right), rl_param(direction(set(
    noop, right, right_a, right_b, right_a_b,
    left, left_a, left_b, left_a_b, 
    down, up, a, b
)))]
+!move(Direction) <- move(Direction).

//noop, right, left, down, a, b,
//right_a, right_b, right_a_b,
//left_a, left_b, left_a_b,

{ include("$jacamoJar/templates/common-cartago.asl") }

