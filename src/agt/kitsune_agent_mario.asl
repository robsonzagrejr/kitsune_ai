// Configuring RL soft plans
rl_algorithm(go_right, qlearning).

//rl_parameter(policy, egreedy).
//rl_parameter(alpha, 0.26).
//rl_parameter(gamma, 0.9).
//rl_parameter(epsilon, 0.4).
//rl_parameter(epsilon_decay, 0.9999).
//rl_parameter(epsilon_min, 0).

rl_observe(go_right,
player(
    int(0, 17),
    int(0, 500), //x
    int(0, 500), //y
    int(0, 500), //w
    int(0, 500), //h
    int(-500, 500), //velocity_x
    int(-500, 500) //velocity_y
)).
rl_observe(go_right,
object(
    int(0, 17),
    int(0, 500), //x
    int(0, 500), //y
    int(0, 500), //w
    int(0, 500), //h
    int(-500, 500), //velocity_x
    int(-500, 500) //velocity_y
)
).
//rl_observe(go_right, obj_player_touching(_, _, _, _, _, _, _, _, _, _, _)).
rl_observe(go_right, t_path(int(0, 17))).
rl_observe(go_right, t_enemie(int(0, 17))).

rl_reward(go_right, R) :- reward(R).

rl_terminal(go_right) :- gameover.


// Convert int to name
obj_name(0, block).
obj_name(1, brick).
obj_name(2, coin).
obj_name(3, flagpole).
obj_name(4, flower).
obj_name(5, g_mushroom).
obj_name(6, goomba).
obj_name(7, item).
obj_name(8, koopa).
obj_name(9, koopa_shell).
obj_name(10, l_mushrrom).
obj_name(11, mario).
obj_name(12, pipe).
obj_name(13, princess).
obj_name(14, question).
obj_name(15, rock).
obj_name(16, star).
obj_name(17, toad).
obj_name(_, none).


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

+object(TN, X, Y, W, H, VX, VY):
    gameover &
    player_touching(X, Y, W, H, DX, DY, TPX, TPY) &
    (TPX \== none) & (TPY \== none) &
    not t_path(TN)
    <-
    ?obj_name(TN, N);
    print("\nENEMY: ",N);
    +enemie(N);
    +t_enemie(TN);
.


// Identifying Paths
+path(N): true <- print("\nNew Path: ", N);.

// name, x, y, w, h, velocity_x, velocity_y
+object(TN, X, Y, W, H, VX, VY):
    player_touching(X, Y, W, H, DX, DY, TPX, bottom) &
    (TPX \== none) &
    player(_, PX, PY, PW, PH, PVX, PVY) &
    (PVY == 0) &
    (VX == 0) &
    not t_enemie(TN)
    <-
    ?obj_name(TN, N);
    +path(N);
    +t_path(TN);
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

