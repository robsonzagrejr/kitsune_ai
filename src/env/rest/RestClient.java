package rest;

import java.util.Map;
import java.util.concurrent.TimeUnit;

import javax.ws.rs.client.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

@SuppressWarnings("unchecked")
public class RestClient<T> {
	
	public static String TARGET = "http://localhost:5003/env/";
	
	private Client client = ClientBuilder.newClient();
	private String envName; 

	public StateRest<T> initialize(String envName, Map<String, String> parameters) {
		this.envName = envName;
		
		EnvironmentRest env = new EnvironmentRest();
		env.setName(envName);
		env.setParameters(parameters);
		
        int connect_trys = 0;
        StateRest<T> response = new StateRest();
        while(connect_trys < 10) {
            try {
                response = client.target(TARGET + envName)
                        .request(MediaType.APPLICATION_JSON)
                        .post(Entity.entity(env, MediaType.APPLICATION_JSON))
                        .readEntity(StateRest.class);
                break;
            } catch (Exception e) {
                connect_trys ++;
                try {
                    TimeUnit.SECONDS.sleep(1);
                } catch (Exception et) {

                }
            }
        }
        System.out.println("Connection trys: " + connect_trys);
		return response;
	}
	
	public StateRest<T> step(int action){
		Response response = client.target(TARGET + envName + "/" + action)
                .request(MediaType.APPLICATION_JSON)
                .post(Entity.entity(action, MediaType.APPLICATION_JSON));
		return response.readEntity(StateRest.class);
	}
	
	
}
