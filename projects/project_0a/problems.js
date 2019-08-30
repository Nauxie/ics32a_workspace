//Problem 1
function perimeter(w, h) { //takes width and height as parameters
    return (2 * w + 2 * h) //formula for perimeter is 2*width + 2*length
}
//console.log(perimeter(5, 6)) //uncomment to test with node


//Problem 2
function concat(s1, s2) { //takes two parameters, which can be strings 
    return (s1 + s2) //concatenates them
}
//console.log((concat('boo', 'lean'))) //uncomment to twn


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
function sum(list) { //create sum function
    let sums = 0 //start with 0
    list.forEach(element => { //uses foreach method to iterate through list
        sums += element //adds element
    })
    return sums
}
//console.log(sum([2, 3, 4, 1, 5])) //uncomment to twn


//Problem 5
function longestStr(list) {
    let ans = list[0] //initally sets longest strong to first element
    list.forEach(element => { //iterates through list
        if (element.length > ans.length) { //enters if statement if element is longer than ans
            ans = element //changes ans to this new longest element
        }
    })
    return ans
}
//console.log(longestStr(["hi", "baye", "nauxtious", "redg", "DELPHINATEINCANTENTUM", "naux"])) //uncomment to twn


//Problem 6
function licenseProblem() {
    let rl = require('readline').createInterface({ input: process.stdin, output: process.stdout }) //calls readline API to access user input from command line
    function testLicense() {
        rl.question('License Plate: ', answer => { //prompts user for plate and saves it as answer variable
            let validity = true //assumes that plate is valid intially
            let digitCount = 0 //variable to count # of digits
            let firstChar = answer.charCodeAt(0) //saves first char ASCII value as variable
            let lastChar = answer.charCodeAt(answer.length - 1)//saves last char ASCII value as variable
            for (let i = 0; i < answer.length; i++) { //iterates through length of answer
                let val = answer.charCodeAt(i) 
                if (val > 48 && val < 57) //if char ASCII is 0-9, increment digitCount (can also use regex for this)
                    digitCount++
                if (val < 48 || val > 57 && val < 65 || val > 90)//if char ASCII is 0-9 or A-Z, plate is invalid (can also use regex for this)
                    validity = false
            }
            if (digitCount == 0) //if no digits in plate, plate is invalid
                validity = false
            if (firstChar < 65 || firstChar > 90 || lastChar < 65 || lastChar > 90) //if first and last character aren't A-Z, plate is invalid
                validity = false
            if (validity) //if plate is valid, end user input sequence
                return rl.close()
            console.log("Not a valid plate. Try again.") //otherwise, specify plate is invalid
            testLicense() //recursion to rerun the method to prompt the user again
        })
    }
    testLicense() // initial run
}
//LicenseProblem() //uncomment the left side of this line to run problem 6


//Problem 7
function searchChar(str, ch) {
    let chCount = 0
    for (const c of str) {
        if (c == ch) {
            chCount++
        }
    }
    return chCount
}
//console.log(searchChar("Boo is not boolean", 'o')) //uncomment to twn


//Problem 8
function pallindrome(str) {
    let reversedStr = ""
    for (let i = str.length - 1; i >= 0; i--) {
        reversedStr = reversedStr + str[i]
    }
    if (reversedStr == str) {
        return true
    }
    return false
}
//console.log(pallindrome("pallindromemordnillap")) //uncomment to twn