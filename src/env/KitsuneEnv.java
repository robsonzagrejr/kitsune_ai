import java.util.HashMap;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import cartago.Artifact;
import cartago.OPERATION;
import cartago.ObsProperty;
import rest.RestClient;
import rest.StateRest;

//import jason.asSyntax.Atom;

public class KitsuneEnv extends Artifact{
    
    private RestClient<List<String>> kitsune_env= new RestClient<>();
    private ArrayList<ObsProperty> lastStepPropeties = new ArrayList<ObsProperty>();
    

    @OPERATION
    public void init() {
        Map<String, String> parameters = new HashMap<>();
        StateRest<List<String>> info = kitsune_env.initialize("KitsuneEnv", parameters);
        updatePercepts(info);
        defineObsProperty("ready");
    }

    @OPERATION
    public void move(String move) {
        StateRest<List<String>> info;
        switch(move) {
            case "noop":
                info = kitsune_env.step(0);
                break;
            case "right":
                info = kitsune_env.step(1);
                break;
            case "right_a":
                info = kitsune_env.step(2);
                break;
             case "right_b":
                info = kitsune_env.step(3);
                break;
             case "right_a_b":
                info = kitsune_env.step(4);
                break;
            case "left":
                info = kitsune_env.step(5);
                break;
            case "left_a":
                info = kitsune_env.step(6);
                break;
             case "left_b":
                info = kitsune_env.step(7);
                break;
             case "left_a_b":
                info = kitsune_env.step(8);
                break;
            case "down":
                info = kitsune_env.step(9);
                break;
            case "a":
                info = kitsune_env.step(11);
                break;
            case "b":
                info = kitsune_env.step(12);
                break;
            default:
                info =  kitsune_env.step(0);
                break;

        }
        updatePercepts(info);
    }


    public void updatePercepts(StateRest<List<String>> info) {
        //Cleanning the old perceptions
        this.clearPercepts();

        //Defining the perceptions
        for (List<String> obj:info.getState()) {
            Object[] parameters = new Object[obj.size() - 1];
            for (int i=1; i<obj.size() ; i++) {
                parameters[i-1] = obj.get(i);
            }
            String propertie_type = "object";
            if (obj.get(0).equals("player")) {
                propertie_type = "player";
            }

            this.lastStepPropeties.add(
                defineObsProperty(
                    propertie_type,
                    parameters
                )
            );
        }
        this.lastStepPropeties.add(defineObsProperty("reward", info.getReward().get(0)));
        this.lastStepPropeties.add(defineObsProperty("score", info.getReward().get(1)));

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

    private void clearPercepts () {
        for (ObsProperty obs:this.lastStepPropeties)
            removeObsProperty(obs.getName());
        this.lastStepPropeties.clear();
    }
}
