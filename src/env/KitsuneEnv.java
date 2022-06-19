import java.util.HashMap;
import java.util.List;
import java.util.Map;

import cartago.Artifact;
import cartago.OPERATION;
import cartago.ObsProperty;
import rest.RestClient;
import rest.StateRest;

//import jason.asSyntax.Atom;

public class KitsuneEnv extends Artifact{
    
    RestClient<List<Double>> kitsune_env= new RestClient<>();
    

    @OPERATION
    public void init() {
        Map<String, String> parameters = new HashMap<>();
        StateRest<List<Double>> info = kitsune_env.initialize("KitsuneEnv", parameters);
        updatePercepts(info);
        defineObsProperty("ready");
    }

    @OPERATION
    public void move(String move) {
        StateRest<List<Double>> info;
        switch(move) {
            case "noop":
                info = kitsune_env.step(0);
                break;
            case "right":
                info = kitsune_env.step(1);
                break;
            case "left":
                info = kitsune_env.step(5);
                break;
            case "down":
                info = kitsune_env.step(9);
                break;
            case "a": //A
                info = kitsune_env.step(11);
                break;
            default:
                info =  kitsune_env.step(0);
                break;

        }
        updatePercepts(info);
    }


    public void updatePercepts(StateRest<List<Double>> info) {
        Double[] player_pos = info.getState().get(0).toArray(new Double[0]);
        defineObsProperty("player_pos", (Object[]) player_pos);
        defineObsProperty("reward", info.getReward());

        // Defining if is a terminal state
        if (info.isTerminal()) {
            if (!hasObsProperty("gameover"))
                defineObsProperty("gameover");
        } else {
            try {
                removeObsProperty("gameover");
            } catch (IllegalArgumentException e) {}
        }
    }
}
