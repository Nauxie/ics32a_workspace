//Problem 1
function perimeter(w, h) { // takes width and height as parameters
    return (2 * w + 2 * h) // formula for perimeter is 2*width + 2*length
}
console.log(perimeter(5, 6)) //test with node


//Problem 2
function concat(s1, s2) { //takes two parameters, which can be strings 
    return (s1 + s2) //concatenates them
}
console.log((concat('boo', 'lean'))) //twn


//Problem 3
function nameAndAge() {
    let rl = require('readline').createInterface({ input: process.stdin, output: process.stdout }) //calls readline API to access user input from command line
    rl.question('Name? ', (name) => { //callback that prompts user for name
        rl.question('Age? ', (age) => { //callback that prompts user for age
            let yearPluraity = (age == 1) ? "year" : "years" //ternary to determine {years} or {year}
            console.log("Your name is " + name + " and you are " + age + " " + yearPluraity + " old!") //prints statement
            rl.close() //closes readline API
        })
    })
}
//nameAndAge() //uncomment the left side of this line to run problem 3


//Problem 4
function sum(list) { // create sum function
    let sums = 0 // start with 0
    list.forEach(element => { //uses foreach method to iterate through list
        sums += element //adds element
    })
    return sums
}
console.log(sum([2, 3, 4, 1, 5])) //twn


//Problem 5
function longestStr(list) {
    let ans = list[0] //initally sets longest strong to first element
    list.forEach(element => { //iterates through list
        if (element.length > ans.length) { // enters if statement if element is longer than ans
            ans = element // changes ans to this new longest element
        }
    })
    return ans
}
console.log(longestStr(["hi", "baye", "nauxtious", "redg", "DELPHINATEINCANTENTUM", "naux"])) //twn


//Problem 6
function licenseProblem() {
    let rl = require('readline').createInterface({ input: process.stdin, output: process.stdout }) //calls readline API to access user input from command line
    function testLicense() {
        rl.question('License Plate: ', answer => {
            if (answer.match() == 'exit') {
                return rl.close()
            }
            console.log("Not a valid plate. Try again.")
            testLicense()
        })
    }
    testLicense()
}
// licenseProblem() // uncomment the left side of this line to run problem 6


//Problem 7
function searchChar(str,ch){
    let chCount = 0
    for (const c of str) {
        if (c == ch) {
            chCount++
        }
    }
    return chCount
}
console.log(searchChar("Boo is not boolean",'o'))

//Problem 8
function pallindrome(str) {
    let reversedStr = ""
    for (let i = str.length-1; i>=0;i--) {
        reversedStr = reversedStr + str[i]
    }
    if (reversedStr == str) {
        return true
    }
    return false
}
console.log(pallindrome("pallindromemordnillap"))