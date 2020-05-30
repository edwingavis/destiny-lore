fetch('https://raw.githubusercontent.com/jamiegavis/destiny-lore/master/model.json')
  .then(response => response.json())
  .then(data => console.log(data));


/*
Build a Python representation of the Markov model. Returns a dict
of dicts where the keys of the outer dict represent all possible states,
and point to the inner dicts. The inner dicts represent all possibilities
for the "next" item in the chain, along with the count of times it
appears.
*/


