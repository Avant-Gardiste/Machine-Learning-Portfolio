# Import dependencies
import gym
import random
import numpy as np 
import os
import Agent

# Intialize environment
env = gym.make('CartPole-v0')

# Set parameters
state_size = env.observation_space.shape[0]
print('State size : ', state_size)

action_size = env.action_space.n
print('Action size : ', action_size)

batch_size = 32
n_episodes = 1001 # n games we want our agent to play (default 1001)

output_dir = 'model_output/cartpole'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize agent
agent = Agent.DQNA_Agent(state_size, action_size) 

#Interact with environment
done = False

for e in range(n_episodes): # Iterate over new episodes of the game
    
    state = env.reset() # Reset state at start of each new episode of the game
    state = np.reshape(state, [1, state_size])
    
    for time in range(5000): # Time represents a frame of the game
        env.render()
        
        action = agent.act(state) # Action is either 0 or 1 (move cart or not)
        
        next_state, reward, done, _ = env.step(action)  # Agent interacts with env, gets feedback; 4 state data points, e.g., pole angle, cart position        
        
        reward = reward if not done else -10 # Reward +1 for each additional frame with pole upright    
        
        next_state = np.reshape(next_state, [1, state_size])
        
        agent.remember(state, action, reward, next_state, done) # Remember the previous timestep's state, actions, reward, etc.        
        
        state = next_state  # Set "current state" for upcoming iteration to the current next state  
        
        if done: # Episode ends if agent drops pole or reach timestep 5000
            print("episode : {}/{}, score : {}, e : {:.2}".format(e, n_episodes, time, agent.epsilon)) # Print the episode's score and agent's epsilon
            break 
            
    if len(agent.memory) > batch_size:
        agent.replay(batch_size) # Train the agent by replaying the experiences
            
    if e % 50 == 0:
        agent.save(output_dir + "weights_" + '{:04d}'.format(e) + ".hdf5")
