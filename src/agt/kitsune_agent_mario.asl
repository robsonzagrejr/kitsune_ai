// Configuring RL soft plans
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


// Define where the player is touching the object

// (0,0) is top left conner
touching(X1, Y1, W1, H1, X2, Y2, W2, H2, DX, DY, PX, PY):-
    x_range(X1, W1, X2, W2, DX, PX) &
    (DX \== 0) &
    y_range(Y1, H1, Y2, H2, DY, PY)
.
touching(X1, Y1, W1, H1, X2, Y2, W2, H2, 0, 0, none, none).


x_range(X1, W1, X2, W2, ((X2+W2+1) - X1), right):-
    (X1 > X2) &
    (X1 <= (X2+W2+1))
.
x_range(X1, W1, X2, W2, ((X1+W1+1) - X2), left) :-
    (X1 < X2) &
    ((X1+W1+1) >= X2)
.
x_range(_,_,_,_,0, none).

y_range(Y1, H1, Y2, H2, ((Y2+H2+1) - Y1), top)    :- (Y1-1 > Y2) & ( Y1 <= (Y2 + H2)).
y_range(Y1, H1, Y2, H2, ((Y1+H1+1) - Y2), bottom) :- (Y1 <= Y2) & ( (Y1+H1+1) > Y2).
y_range(_,_,_,_,0, none).


+object(N, X, Y, W, H, VX, VY):
    player(_, PX, PY, PW, PH, PVX, PVY) &
    ((VX \== 0) | (VY \== 0)) &
    touching(PX, PY, PW, PH, X, Y, W, H, TDX, TDY, TPX, TPY) &
    (TPX \== none | TPY \== none) &
    gameover
    <-
    print("\n=======");
    print("\nNew: ", N, " VX: ", VX, " VY: ", VY, "PLAYER: ",PN);
    print("\nDistance X: ",TDX," And : ",TPX);
    print("\nDistance Y: ",TDY," And : ",TPY);
    print("\nVelocity X: ",VX," Y: ",VY);
    print("\nEnemy: ",N);
    +enemie(N);
.

+object(N, X, Y, W, H, VX, VY):
    gameover &
    ((VX \== 0) | (VY \== 0)) &
    player(PN, PX, PY, PW, PH, PVX, PVY)
    <-
    ?touching(PX, PY, PW, PH, X, Y, W, H, TDX, TDY, TPX, TPY);
    print("\n=======");
    print("\nMORREU: ", N, " VX: ", VX, " VY: ", VY, "PLAYER: ",PN);
    print("\nDistance X: ",TDX," And : ",TPX);
    print("\nDistance Y: ",TDY," And : ",TPY);
    print("\nNew: ", N, " X: ", X, " Y: ", Y);
.


//(X,Y,0,-1):- (X>=-1 & X<=1 & Y<=-1) | Y<=-2.
//touch_position(X1, Y1, W1, H1, X2, Y2, W1, H1, top):- ().
//bottom
//left
//right

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

//+object(N, X, Y, W, H, VX, VY):
//    player(_, PX, PY, PW, PH, PVX, PVY) &
//    (
//     (PY <= Y)
//    ) &
//    not path(N)
//    <-
//    +path(N);
//    .

+path(N): true <- 
    print("\nNew Path: ", N);.

+enemie(N): true <- print("\nNew Enemie: ", N);.


{ include("$jacamoJar/templates/common-cartago.asl") }

