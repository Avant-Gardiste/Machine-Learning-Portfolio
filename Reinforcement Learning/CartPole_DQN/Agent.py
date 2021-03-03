import numpy as np 
import random
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

#Define Agent
class DQNA_Agent:
    def __init__(self, state_size, action_size):
        
        self.state_size = state_size
        self.action_size = action_size
        
        self.memory = deque(maxlen=2000) # Double-ended queue; acts like list, but elements can be added/removed from either end
        
        self.gamma = 0.95 # Decay or discount rate: enables agent to take into account future actions in addition to the immediate ones, but discounted at this rate
        
        self.epsilon = 1.0 # Exploration rate: how much to act randomly; more initially than later due to epsilon decay
        self.epsilon_decay = 0.995 # Decrease number of random explorations as the agent's performance (hopefully) improves over time
        self.epsilon_min = 0.01 # Minimum amount of random exploration permitted
        
        self.learning_rate = 0.001 # Rate at which NN adjusts models parameters via SGD to reduce cost 
        
        self.model = self._build_model() # Private method 
        
    # Neural network to approximate Q-value function:
    def _build_model(self): 
        model = Sequential()
        
        model.add(Dense(24, input_dim=self.state_size, activation='relu')) # 1st hidden layer (Input)
        model.add(Dense(24, activation='relu')) # 2nd hidden layer
        model.add(Dense(self.action_size, activation='linear')) # 2 actions, so 2 output neurons: 0 and 1 (L/R)
        
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate)) 
        
        return model
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # List of previous experiences, enabling re-training later
        
    def act(self, state):
        if np.random.rand() <= self.epsilon: # If acting randomly, take random action
            return random.randrange(self.action_size)
        
        act_values = self.model.predict(state)  # If not acting randomly, predict reward value based on current state
        return np.argmax(act_values[0]) # Pick the action that will give the highest reward (i.e., go left or right?)
    
    # Method that trains NN with experiences sampled from memory
    def replay(self, batch_size):
        
        minibatch = random.sample(self.memory, batch_size) # Sample a minibatch from memory
        
        for state, action, reward, next_state, done in minibatch: # Extract data for each minibatch sample
            
            target = reward # If done (boolean whether game ended or not, i.e., whether final state or not), then target = reward
            
            if not done: # If not done, then predict future discounted reward
                target = (reward + self.gamma  * np.amax(self.model.predict(next_state)[0])) # Max target Q based on future action A
            
            target_f = self.model.predict(state) # Approximately map current state to future discounted reward
            target_f[0][action] = target
            
            self.model.fit(state, target_f, epochs=1, verbose=0)  # Single epoch of training with x=state, y=target_f; fit decreases loss btwn target_f and y_hat
            
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
    def load(self, name):
        self.model.load_weights(name)
        
    def save(self, name):
        self.model.save_weights(name)