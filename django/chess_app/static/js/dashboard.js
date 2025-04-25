import { setAttributes, setUpHTML, setUpSVG } from "./helperScripts.js";


window.onload = () => {

    var parent = document.getElementById("roomBrowser");

    const browser = new lobbyBrowser(null, parent);

    parent = document.getElementById("globalRanking");

    const globalRanking = new rankingBoard(null, parent, "global");

    parent = document.getElementById("friendRanking");

    const friendRanking = new rankingBoard(null, parent, "friend");

    parent = document.getElementById("friendbar");

    const friendbar = new friendList(null, parent);
}



class lobbyBrowser {


    constructor(user, Ref){
        this.user = user;
        this.Ref = Ref;
        
        this.registerLobbyNav();
    }

    registerLobbyNav(){
        const navBar = setUpHTML("div",{class:"wrapperS"},this.Ref);
        const createButton = setUpHTML("input", {type:"button", class:"createRoom", id:"createRoom", value:"Create Room!"}, navBar);

        createButton.addEventListener("click", () => {

            window.location = "./game"

        })

        const lobbyList = setUpHTML("div", {class: "lobbyList", id:"lobbyList"}, this.Ref);

        for(let i=0; i<20; i++){
            setUpHTML("div",{class:"lobbyCard"}, lobbyList);
        }

    }

    async fetchLobbys(){

    }
}

class rankingBoard {


    constructor(user, ref, type){
        this.user = user;
        this.ref = ref;
        this.type = type;

        this.fetchLobbys();

    }

    async fetchLobbys(){
        const response = [1,2,3,4];

        response.forEach((ranks)=> {
            setUpHTML("div",{class:"rankingCard"}, this.ref);
        })
    }
}

class friendList {

    constructor(user, ref){

        this.user = user;
        this.ref = ref;

        this.fetchFriends();
    }

    async fetchFriends(){
        const response =["Carl", "Peter", "Flötenmann"]

        response.forEach((friend)=>{

            const card = setUpHTML("div",{class:"friendCard", id:"friendCard"},this.ref)

            const txt = document.createTextNode(friend);

            card.appendChild(txt);

        })
    }
}