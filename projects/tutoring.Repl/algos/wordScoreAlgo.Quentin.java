package algos;
class Main {
  
    // DECLARE VARIABLES 
    // ....
    // ....
    public static String word;
  
    public static int ascii ;
  
    public static int champion = 0;
      public static int champion_pos = 0;
    public static int loser ;
    public static char lower ;
    public static String answer;
    public static boolean top_dog = false;
  
  
  
  
    public static void main(String[] args) {
      String sentence = "What was the person thinking when they discovered cow's milk was fine for human consumption... and why did they do it in the first place!? zzzzzzzzzzzz ";
      String[] arrOfStr = sentence.split(" ")  ;
      
          // for every word in array
          for ( int i = 0; i < arrOfStr.length; i++    )
          {
            loser = 0;
            word = arrOfStr[i];
            top_dog = false;
            
            
            // LOOP THROUGH THE WORD
            for ( int x = 0; x < word.length(); x++    )
            {
              
              ascii = (int) word.charAt(x) ;
  
              // UPPERCASE
              if( ascii >= 65  & ascii <= 90)
              {
                lower = Character.toLowerCase(word.charAt(x));
                ascii = (int) lower ;
                loser = loser + ascii;
              }
  
              //LOWERCASE
              else if( ascii >= 97  & ascii <= 122)
              {
                loser = loser + ascii;
              }
  
            }
  
            // if word is bigger than current winner
            if(   loser > champion  )
            {
              champion = loser;
              top_dog = true;
              champion_pos = i;
            }
            if (top_dog == true)
            {
              answer = "";
              // LOOP THROUGH THE WORD AGAIN
              for ( int x = 0; x < word.length(); x++    )
              {
                
                ascii = (int) word.charAt(x) ;
  
                // UPPERCASE
                if( ascii >= 65  & ascii <= 90)
                {
                  answer = answer + word.charAt(x);
                }
  
                //LOWERCASE
                else if( ascii >= 97  & ascii <= 122)
                {
                  answer = answer + word.charAt(x);
                }
  
              }
            }
  
  
  
          }
  
  
  
  
  
          // printing the winner
  
           System.out.println( answer  );
  
          }
  }
  
  
  
  
  
  
  // CHALLENGE
  // PLEASE....
  // Given a sentence... please find the highest rated word
  // every letter inside of the word adds up the total 
  // a -1 
  // b-2
  // c-3
  
  