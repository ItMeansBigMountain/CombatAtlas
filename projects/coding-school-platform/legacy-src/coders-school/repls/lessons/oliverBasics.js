
//JUST LIKE IMPORTING ON PYTHON, REQUIRE WILL GIVE US EXTRA COMMANDS
var random_number = require('random-number');


// print 1 - 255
function algo1() {
    for (var i = 1; i <= 255; i++) {
        console.log(i)
    }
}

// print all odd numbers from 1-255
function algo2() {
    for (var i = 1; i <= 255; i += 2) {
        console.log(i)
    }
}


// all odd numbers from 101 - 225
function algo3() {
    var apple = "apple"
    for (var i = 1; i <= 300; i += 1) {
        console.log(i)
        console.log(apple)
        console.log("________________________")
    }
}


function algo4() {
    var I_did_it = "I did it";
    for (var i = 100; i <= 200; i = + 2) {
        console.log(I_did_it)
    }
}



//print the sum of all numbers to 255
function algo5() {


    var total = 0
    console.log(total)


    for (var i = 0; i <= 255; i += 1) {

        // every loop will add i to the total
        total += i
    }
    console.log(total)


}




//print the average of an array
function algo6() {
    //setting up our variables "INITIALIZATION"
    test_scores = [80, 60, 100, 95, 73, 100, 50, 67, 92, 80]
    var added_total = 0



    //we are using this for loop to go through the array
    //"i" will be used as our array[INDEX]
    for (var oliver = 0; oliver < test_scores.length; oliver++) {

        var iteration_item = test_scores[oliver]
        added_total += iteration_item;

    }

    console.log(added_total / test_scores.length)



}



// print every negative number inside of array
function algo7() {

    test = [-80, 60, 100, 95, -73, 100, 50, 67, 92, -80]

    //  START     ;       END       ; GO UP BY
    for (var i = 0; i < test.length; i++) {
        //***code repeats in here***



        if (test[i] < 0) {
            console.log(test[i])
        }
    }


}


//SQUARE EACH VALUE IN ARRAY
function algo8() {

    box = [2, 4, 6, 8, 10, 12]
    console.log(box)


    for (var i = 0; i < box.length; i += 1) {
        box[i] = box[i] * box[i]
    }

    console.log(box)

}


//return a count of how many numbers in the array are bigger than a given value

function algo9() {
    var value = 10
    var box = [2, 44, 6, 8, 10, 12]
    var count = 0
    for (var i = 0; i < box.length; i++) {
        if (box[i] > value) {
            count += 1
        }
    }
    console.log(count)
}





//zero out every negative number inside of array 
function cahootpatato() {
    var box = [2, -44, 6, 8, -10, 12]

    console.log(box);

    //goes through the array , i is just a number that we use for the index 
    for (var i = 0; i < box.length; i++) {

        //if less than zero, turn it into zero 
        if (box[i] < 0) {
            box[i] = 0
        }

    }

    console.log(box);


}




//THIS IS WHERE THE ACTUAL CODE STARTS
//BECAUSE EVERYTHING ABOVE IT IS "DEFINING FUNCTIONS"
//calling functions
// cahootpatato()

//REMEMBER PREFABS!!!!!!



//Random number practice
function random() {
    var box = [
        (random_number() * 100),
        (random_number() * 100),
        (random_number() * 100),
        (random_number() * 100), (random_number() * 100),
        (random_number() * 100), (random_number() * 100),
        (random_number() * 100), (random_number() * 100),
        (random_number() * 100), (random_number() * 100),
        (random_number() * 100), (random_number() * 100),
        (random_number() * 100), (random_number() * 100),
        (random_number() * 100), (random_number() * 100),
        (random_number() * 100), (random_number() * 100),
        (random_number() * 100), (random_number() * 100),
        (random_number() * 100), (random_number() * 100),
        (random_number() * 100), (random_number() * 100),
        (random_number() * 100), (random_number() * 100),
        (random_number() * 100), (random_number() * 100),
        (random_number() * 100), (random_number() * 100),
        (random_number() * 100)

    ]

    for (var i = 0; i < box.length; i++) {
        box[i] = Math.floor(box[i])
    }



    console.log(box);
}

random()