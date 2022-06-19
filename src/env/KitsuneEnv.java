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


    public void updatePercepts(StateRest<List<String>> info) {
        //Cleanning the old perceptions
        this.clearPercepts();

        //Defining the perceptions
        for (List<String> obj:info.getState()) {
            Object[] parameters = new Object[obj.size() - 1];
            for (int i=1; i<obj.size() ; i++) {
                parameters[i-1] = obj.get(i);
            }
            this.lastStepPropeties.add(
                defineObsProperty(
                    obj.get(0),
                    parameters
                )
            );
        }
        this.lastStepPropeties.add(defineObsProperty("reward", info.getReward()));

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
