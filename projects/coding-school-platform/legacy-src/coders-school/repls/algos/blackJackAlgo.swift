// https://edabit.com/challenge/enDkd7H53FN3PMuyh

/*


Create a function that takes an array of card numbers and checks if the sum of their value exceeds 21. If the sum exceeds 21, return true and if the sum is under or equal to 21, return false. Values of the cards are as follows:

2-10 are their value.
J-K (face cards) count as 10.
Aces count either as 1 or 11 - play conservatively, so that if giving an ace a value of 11 causes you to lose and 1 allows you to win, then go with 1.


overTwentyOne([2, 8, "J"]) ➞ false

overTwentyOne(["A", "J", "K"]) ➞ false

overTwentyOne([5, 5, 3, 9]) ➞ true

overTwentyOne([2, 6, 4, 4, 5]) ➞ false

overTwentyOne(["J", "Q", "K"]) ➞ true

overTwentyOne([5, 3, 6, 6, 7, 9]) ➞ true



*/


func overTwentyOne(_ cards: [Any]) -> Bool {
	var total: Int = 0;
	for i in cards {
		if i is String {
			if ("A" == i as! String) {
				if (total > 11) {
					total += 11;
				} else {
					total += 1;
				}
			} else {        
			total += 10;  
			}
		} else {
			total += i as! Int;
		}
	}
	return total > 21;
}



// calling functions down here
print(overTwentyOne( [ 1 , 5 , 2 , "J"  ]  ))