package rl.algorithm.tf;

public class PyAlgorithm extends TensorFlowAgent{
	public PyAlgorithm(String goal, String algorithm) {
		super(goal, algorithm);
	}

	protected String getMethod() { return this.algorithm; }
}
