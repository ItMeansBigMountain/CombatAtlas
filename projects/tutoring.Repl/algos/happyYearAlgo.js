// I DID IT OMG
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// BASICALLY 
// unique = false
// while its false... keep trying a year
// masterString is our year in string version
// we iterate to get they year substring
// then we go through all the rest of the sub strings
//   if there is a bad one,
//   count up how many bad ones we get
// then outside both loops, we check how many errors we got...
// if those errors are greater than 0, add one to year and try again... keep trying until it has zero errors!

// RETURN THE YEAR!!!!!!



function happyYear(year){
	
	var unique = false;

  while(unique == false)
  {
    var errorz = 0; // errors is always zero every new year we try

    var masterString = year.toString()
    // console.log(masterString)

    
    for (var i =0 ; i < masterString.length ; i++)
    {
      // console.log("\n-----------" + masterString[i] + "-----------")
      for (var x =0 ; x < masterString.length ; x++)
      {
        if (x == i){continue;}
        if (masterString[i] == masterString[x])
        {
          // console.log("bad")
          errorz += 1  //we add an error if there is a match
        }  
      }
    }

    if (errorz == 0) // this checks how many errors we tallied
    {
      return year
    }
    else
    {
      year +=1
    }

  }

}




// MAIN
console.log(happyYear(1990))
//https://edabit.com/challenge/ruW8bbjeMdb9jNsW7