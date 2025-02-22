# Assertions on Agent Rationality

## 1. An agent that senses only partial information about the state cannot be perfectly rational.  
**Answer: False**  

### Explanation  
Perfect rationality is defined by taking the best possible action given the available information. Even with partial information, an agent can still act optimally based on what it perceives.

---

## 2. There exist task environments in which no pure reflex agent can behave rationally.  
**Answer: True**  

### Explanation  
Pure reflex agents act solely based on the current percept without maintaining history or internal state. In environments where decisions depend on past percepts, reflex agents fail to make rational choices.

---

## 3. There exists a task environment in which every agent is rational.  
**Answer: True**  

### Explanation  
If all actions in a given environment yield the same outcome, then no action can be considered less rational than another. Every agent, regardless of its decision-making process, would be rational in such an environment.

---

## 4. The input to an agent program is the same as the input to the agent function.  
**Answer: False**  

### Explanation  
The agent function conceptually receives the entire percept history, while the agent program may process only the current percept or a subset of past percepts. This distinction means that the two inputs are not necessarily identical.

---

## 5. Every agent function is implementable by some program/machine combination.  
**Answer: False**  

### Explanation  
Certain agent functions require solving problems that are non-computable, such as undecidable problems. These functions cannot be implemented by any computational model, including Turing machines.

---

## 6. Suppose an agent selects its action uniformly at random from the set of possible actions. There exists a deterministic task environment in which this agent is rational.  
**Answer: True**  

### Explanation  
If all possible actions in a deterministic environment result in equally optimal outcomes, then random action selection does not diminish rationality. The agent remains rational as no action is superior to another.

---

## 7. It is possible for a given agent to be perfectly rational in two distinct task environments.  
**Answer: True**  

### Explanation  
An agent can be designed to maximize performance measures that apply across multiple environments. If the performance criteria align with the agent’s decision-making strategy, it remains rational in both cases.
