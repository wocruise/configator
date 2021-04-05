function sayHello() {
    this.greet = ()=>{
    console.log("hello!");
    }
}

module.exports = new sayHello();