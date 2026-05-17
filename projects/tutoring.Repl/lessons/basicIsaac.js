
//DEFINING FUNCTIONS

//Print 1 - 255
function algo1(){
    //for loop - how the computer counts in code
    
      //Sart point ; end point ; goes up by
    for( var l = 1; l < 256; l+=1 ){
      console.log(l)
    }
  
  }
  
  
  //print all odd numbers from 1-255
  function algo2(){
  
    for( var l = 1; l < 256; l+=2 ){
      console.log(l)
    }
  
  }
  
  
  // print the sum of all the numbers from 1-255
  function algo3(){
  
    var total = 0
    console.log(total)
  
  
    
    for( var z = 1 ; z < 256 ; z+=1 ){
      total = total + z;
    }
    
    console.log(total)
    
  }
  
  
  
  
  //print all values inside of an array
  function algo4(){
  
    //ARRAY holds a bunch of data inside of a box
    var box = ["Isaac",5,4,10,11,10,54,64,31,46,18,87]
  
                //array[INDEX]
    console.log( box[0] ) //gets the fist item because its 0
  
    for (var z = 0 ; z < box.length ; z+=1){
  
      console.log( box[ z ] )
    }
  
  }
  
  
  //print the maximum number inside of an array
  function algo5(){
  
    var box = [5,4,10,11,100,54,64,31,46,18]
    var maximum = 0 ;
  
    for (var o = 0 ; o < box.length ; o+=1){
  
          if(  maximum < box[o]  ){
            maximum = box[o]
          }
      }
  
  console.log(maximum)
  
  }
  
  
  //print the the average of a set of numbers
  
  function algo6(){
  
    //average = the total of all the numners, divided by how many numnbers there are
    var tests = [100 , 75 , 90 , 60]
  
    var total = 0;
    var average = 0;
    
    for (var o = 0 ; o < tests.length ; o+=1){
      total = total + tests [o] 
  
  
    average = total/tests.length 
    console.log(average) 
    }
     
    
  }
  
  
  
  
  
  
  
  
  //print all NEGATIVE inside of a box
  function algo7(){
  
    var box = [1,-2,-3,4,-5,-6,-7,8,-9,10]
  
  
    for(var o = 0 ; o < box.length ; o+=1){
  
      //check to see if box o is smaller than zero IE: NEGATIVE NUMBER
      if( box[o] < 0  ){
  
        console.log(box[o]) 
  
      }
        
      }
      
      
    }
  
  
  //square all the values inside of an array
  function algo8(){
  
    var box = [2,5,7,3,9,8,3,16,4,54,78,32,39,82,37,64,51,64 ] 
  
    for(var lolypop = 0 ; lolypop < box.length ; lolypop+=1){
      //code written here will repeat as many times as the forloop tells it too 
      box[lolypop] = box[lolypop] * box[lolypop]
  
    }
  
    console.log(box)
  
  
  }
  
  
  
  //
  function algo9(){
    var given_number = 25
    var box = [10,11,19,9,5,60,48,1,298,54,354,754,74,77777777777777777666666666666];
    
    //go through box and display every number bigger than "given number"
    
    
    for(var lolypoop = 0 ; lolypoop < box.length ; lolypoop+=1){
  
        //if box[lolypop] is bigger than given number
  
      if(  given_number < box[lolypoop]  ){
              console.log(box[lolypoop]);
      }
    }
  
  }
  
  
  
  //replace all negative numbers inside box with a word
  function algo10(){
    var box = [10,11,19,-9,5,-60,-48,-1,-298,-54,-354,-5,74,-77777777777777777666666666666];
    console.log("BEFORE")
    console.log(box)
  
      for(var lolypoop = 0 ; lolypoop < box.length ; lolypoop+=1){
  
      if( box[lolypoop] < 0 ){
         //change the negative number into a word
  
         box[lolypoop] = 'lollypoop'
      }
    }
  
    console.log("after")
    console.log(box)
  }
  
  
  
  //calculating  tax of something you wanna buy
  function algo11(price , taxRate)
  {
    percentage = taxRate / 100;
  
    total=percentage*price;
  
    console.log("you will pay:")
    console.log (total);
  
  }     
  
  function story()
  {
    
  }
  
  
  
  //CALLING FUNCIONS
  algo11()
  
  