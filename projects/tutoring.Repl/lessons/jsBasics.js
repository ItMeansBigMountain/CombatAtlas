function listExample() {
    let animal = ["tortoise", "dog", "cat"]
    let tortoise = animal[0]
    let dog = animal[1]
    let hoopla = animal[2]

    console.log(animal);
    console.log(tortoise);
    console.log(dog);
    console.log(hoopla);
}


function Ifstatement() {
    var z = 2
    if (z === 2) {
        console.log(z)
    }
}


function Forloop() {
    // for loop quiz :)
    let vacation = ["Smoothie", "Resort", "WaterPark"]
    for (let v = 0; v < 3; v++) {
        vacation[v] = vacation[v] + "!!!"
        console.log(vacation[v]);
    }
}


function Whileloop() {
    //while loop
    let z = 0;
    while (z < 3) {
        z++;
        console.log(z)
    }
}






function main() {
    console.log("Main Menu");
    console.log("Forloop - 1");
    console.log("Whileloop - 2");
    console.log("If statement - 3");
    console.log("Arrays Example - 4");

    option = prompt("please enter an option: ");

    console.log('');
    console.log('');

    if (option === "1") {
        Forloop()
    }

    if (option === "2") {
        Whileloop()
    }

    if (option === "3") {
        Ifstatements()
    }

    if (option === "4") {
        listExample()
    }

    console.log('');
    console.log('');
    console.log('');
    main()

}



main()