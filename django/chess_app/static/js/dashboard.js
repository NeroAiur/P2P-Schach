import { setAttributes, setUpHTML, setUpSVG, getCookie } from "./helperScripts.js";



window.onload = () => {

    const userID = getCookie("userID")
    localStorage.setItem("userID", userID);

    var parent = document.getElementById("roomBrowser");
    const browser = new lobbyBrowser(userID, parent);

    parent = document.getElementById("globalRanking");
    const globalRanking = new rankingBoard(userID, parent, "global");

    parent = document.getElementById("friendRanking");
    const friendRanking = new rankingBoard(userID, parent, "friend");

    parent = document.getElementById("friendbar");
    const friendbar = new friendList(userID, parent);

}

/*Requests all active lobbys from /lobby and displays the results in form {oppoName:string, gameID:string, type: string}. Clicking on a certain room will join that game via the gameID.
Clicking on Create Room will register {userID:string} the new lobby to the lobby list via the /newLobby endpoint. The app will navigate to /game and display a waiting for opponent message*/

class lobbyBrowser {



    constructor(user, Ref) {

        this.user = user;
        this.Ref = Ref;

        this.registerLobbyNav();
        this.fetchLobbys();

    }



    registerLobbyNav() {

        const navBar = document.getElementById("roomBrowserBanner");
        const createButton = setUpHTML("input", { type: "button", class: "createRoom", id: "createRoom", value: "Create Room!" }, navBar);

        createButton.addEventListener("click", () => {

            var form = setUpHTML("form", { method: "POST", action: "./create_game" }, document.body);
            var element1 = setUpHTML("input", { value: this.user, name: "userID", class: "hiddenInput" }, form);

            form.submit();

        })

        this.lobbyList = setUpHTML("div", { class: "lobbyList", id: "lobbyList" }, this.Ref);

    }

    /*Gets all loby and stores the roomID in the onClick() of the button for joining the room*/

    async fetchLobbys() {

        const csrftoken = getCookie('csrftoken');

        const response = await (await fetch("/lobby", {

            method: "POST",
            headers: {
                "Content-Type": "application/json; charset=UTF-8",
                "X-CSRFToken": csrftoken
            },
            credentials: "include"

        })).json();

        response.map((lobby, i) => {

            const card = setUpHTML("div", { class: "lobbyCard" }, this.lobbyList);

            const txt = setUpHTML("p", { class: "lobbyText" }, card);
            txt.textContent = "Opponent: " + lobby.userID + " has " + lobby.score + " ELO";

            const joinButton = setUpHTML("input", { type: "button", class: "joinRoom", id: "joinRoom " + i, value: "Join Room!" }, card)

            joinButton.addEventListener("click", () => {

                var form = setUpHTML("form", { method: "POST", action: "/join" }, document.body);

                setUpHTML("input", { value: this.user, name: "userID", class: "hiddenInput" }, form);
                setUpHTML("input", { value: lobby.room_id, name: "roomID", class: "hiddenInput" }, form);

                form.submit();

            })

        })

    }

}

/*Requests ranking data from /ranking in form {userID:string, either SQL or type:string} and displays returned data {userName:string, score: string}. Not Working!*/

class rankingBoard {



    constructor(user, ref, type) {

        this.user = user;
        this.ref = ref;
        this.type = type;

        this.fetchRanking();

    }



    async fetchRanking() {

        const response = [1, 2, 3, 4, 5];

        this.rankingList = setUpHTML("div", { class: "list", id: "rankingList" }, this.ref);

        response.forEach((ranks) => {

            setUpHTML("div", { class: "rankingCard" }, this.rankingList);

        })

    }

}

/*Sends {userID:string}, recieves {userName:string, score:string} Not Working!*/

class friendList {



    constructor(user, ref) {

        this.user = user;
        this.ref = ref;

        this.fetchFriends();

    }



    async fetchFriends() {

        const response = ["Carl", "Peter", "Flötenmann"];

        this.friendList = setUpHTML("div", { class: "list", id: "friendList" }, this.ref);

        response.forEach((friend) => {

            const card = setUpHTML("div", { class: "friendCard", id: "friendCard" }, this.friendList);

            const txt = document.createTextNode(friend);
            card.appendChild(txt);

        })

    }

}