This is a subnet pygame dedicated to test students' understanding of the subnet mask and calculate the starting and end range of the given subnet.
  **The basic funtionality is described below:**

**Generating questions**   
 The game generates random prefixes and random subent mask from a given set (to prevent the mask being super hard):
` random.choice([1,7,8,9,15,16,17,23,24,25,30,31])`  
 
 **Winning/Losing conditions**   
 The game allows three lives for the player, each failed try cost a life, a timeout also cost a life, when it reaches 0 the player would lose the game automatically. 
 To win the game players need to reach the score of 10, each correct answer gives one point, if solved within 30 seconds an additional point is granted.
 
 **Gameplay**   
 The game is click-type based, meaning that players can click to activate the block and type in their answers in, it also supports deleting and changing the answers.  
 To submit answers, players need to hit _Enter_. After submitting the answer, a result page will show up and tell the players if they win/lose the round, and the game    will continue with updated lives and scores.
 

