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
        //StateRest<List<Double>> state = kitsune_env.initialize("KitsuneEnv", parameters);
	}

	@OPERATION
	public void move(String move) {
        StateRest<List<Double>> state;
        switch(move) {
            case "NOOP":
                state = kitsune_env.step(0);
                break;
            case "right":
                state = kitsune_env.step(1);
                break;
            case "jump": //A
                state = kitsune_env.step(11);
                break;
            default:
                kitsune_env.step(0);
                break;

        }
		//updatePercepts(state);
	}
	
}
