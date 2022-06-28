package rl.algorithm.tf;

public class QLearning extends TensorFlowAgent{
	public QLearning(String goal) {
		super(goal);
	}

	protected String getMethod() { return "qlearning"; }
}
