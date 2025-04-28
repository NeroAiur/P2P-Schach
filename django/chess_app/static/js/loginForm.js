import { setAttributes, setUpHTML, cleanInput, hash, getCookie } from "./helperScripts.js";


window.onload = () =>{

    const loginDiv= document.getElementById("loginForm")
    let login = new loginForm(loginDiv);

}

/*Sets up HTML elements for either login or register form and appends necessary event listeners. Handles also POST requests to backend */

class loginForm {

    eRef=null; pwRef=null;


    constructor(parent){

        this.parent = parent;

        this.children = Array(8)

        this.registerLogin();

    }

    clearChildren(){

        this.children.forEach((child) => {

            child.remove();
            child= null;
            
        })

    }

    registerLogin(){

        this.clearChildren();

        this.eRef = setUpHTML("input",{"type":"text","name":"username",class:"textInput", id:"usernameInput", placeholder: "Username..."},this.parent);

        this.children.push(this.eRef);

        this.pwRef = setUpHTML("input",{"type":"password","name":"password", class:"textInput", id:"pwInput", placeholder: "Password..."},this.parent);

        this.children.push(this.pwRef);

        var button = setUpHTML("input", {type:"button", class:"loginButton", id:"signInButton", value: "Log in!"},this.parent);
        button.addEventListener("click", this.fetchLogin.bind(this))

        this.children.push(button);

        button = setUpHTML("input", {type:"button", class:"loginButton", id:"registerButton", value: "Register here!"},this.parent);
        button.addEventListener("click", this.registerRegister.bind(this))

        this.children.push(button);

    }

    registerRegister(){

        this.clearChildren();
        
        this.eRef = setUpHTML("input",{"type":"text","name":"username",class:"textInput", id:"usernameInput", placeholder:"Username..."},this.parent);

        this.pwRef = setUpHTML("input",{"type":"password","name":"password", class:"textInput", id:"pwInput", placeholder: "Password..."}, this.parent);

        var button = setUpHTML("input", {type:"button", class:"loginButton", id:"signUpButton", value:"Register!"}, this.parent);
        button.addEventListener("click", this.fetchSignUp.bind(this))

        button = setUpHTML("input", {type:"button", class:"loginButton", id:"loginButton", value:"Already a User? Sign in!"},this.parent);
        button.addEventListener("click", this.registerLogin.bind(this))

    }

    /*Reads in Info, cleans it and hashes PW. Sends data in body as JSON:
        {email:string, password: string}, 
    expects 
        {Sucess:bool, UserID: string},
    to  /login
    stores the ID in local Storage and navigates to dashboard*/

    async fetchLogin(){

        var email = this.eRef.value;
        var password = this.pwRef.value;

        if(password.length<8){
            //Password length t o short
            return
        }

        email= cleanInput(email);
        password = cleanInput(password)

        password = await hash(password);

        console.log(password)

        const csrftoken = getCookie('csrftoken');

        var form = setUpHTML("form",{method:"POST", action: "./login"}, document.body);
        var element1 = setUpHTML("input", {value: email, name: "username", class:"hiddenInput"}, form); 
        var element2 = setUpHTML("input", {value: password, name: "password", class:"hiddenInput"}, form);  
    
        form.submit();

    }

    fetchSignUp(){

    }



}
