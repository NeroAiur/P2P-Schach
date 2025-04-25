import { setAttributes, setUpHTML } from "./helperScripts.js";


window.onload = () =>{

    const loginDiv= document.getElementById("loginForm")
    let login = new loginForm(loginDiv);

}

class loginForm {

    eRef=null; pwRef=null;


    constructor(parent){

        this.parent = parent;

        this.registerLogin();

    }

    clearChildren(){

        var children = this.parent.children;

        const iterations =children.length;

        for(let i=0; i<iterations;i++){

            children[0].remove();

        }

    }

    registerLogin(){

        this.clearChildren();

        var label = setUpHTML("label", {"for":"email", class:"inputLabel"}, this.parent);
        this.eRef = setUpHTML("input",{"type":"text","name":"email",class:"textInput", id:"emailInput"},this.parent);
        var txt = document.createTextNode("Email: ");
        label.appendChild(txt);

        label = setUpHTML("label", {"for":"password", class:"inputLabel"}, this.parent);
        this.pwRef = setUpHTML("input",{"type":"password","name":"password", class:"textInput", id:"pwInput"},this.parent);
        txt = document.createTextNode("Passwort: ");
        label.appendChild(txt);

        var button = setUpHTML("input", {type:"button", class:"loginButton", id:"signInButton"},this.parent);
        button.addEventListener("click", this.fetchLogin.bind(this))

        button = setUpHTML("input", {type:"button", class:"loginButton", id:"registerButton"},this.parent);
        button.addEventListener("click", this.registerRegister.bind(this))

    }

    registerRegister(){

        this.clearChildren();
        
        var label = setUpHTML("label", {"for":"username", class:"inputLabel"}, this.parent);
        this.eRef = setUpHTML("input",{"type":"text","name":"username",class:"textInput", id:"usernameInput"},this.parent);
        var txt = document.createTextNode("Nutzername: ");
        label.appendChild(txt);

        var label = setUpHTML("label", {"for":"email", class:"inputLabel"}, this.parent);
        this.eRef = setUpHTML("input",{"type":"text","name":"email",class:"textInput", id:"emailInput"},this.parent);
        var txt = document.createTextNode("Email: ");
        label.appendChild(txt);

        label = setUpHTML("label", {"for":"password", class:"inputLabel"}, this.parent);
        this.pwRef = setUpHTML("input",{"type":"password","name":"password", class:"textInput", id:"pwInput"},this.parent);
        txt = document.createTextNode("Passwort: ");
        label.appendChild(txt);

        var button = setUpHTML("input", {type:"button", class:"loginButton", id:"signUpButton"},this.parent);
        button.addEventListener("click", this.fetchSignUp.bind(this))

        button = setUpHTML("input", {type:"button", class:"loginButton", id:"loginButton"},this.parent);
        button.addEventListener("click", this.registerLogin.bind(this))

    }

    async fetchLogin(){

        const queryparams = {
            email: this.eRef.value,
            password:  this.pwRef.value
        };

        var values = await (await fetch("http://127.0.0.1:5500/frontend/dashboard.html", {

            method: "POST",
            body: JSON.stringify(queryparams),
            headers: {"Content-type": "application/json; charset=UTF-8"}

        })).text();

        var html = await (await fetch("http://127.0.0.1:5500/frontend/dashboard.html")).text();

        document.body.innerHTML=html;
    }

    fetchSignUp(){

    }

}