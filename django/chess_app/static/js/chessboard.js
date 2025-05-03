{ }

import { setAttributes, setUpHTML, setUpSVG, encodeRow, getCookie } from "./helperScripts.js";
import { gamePiece } from "./pieces.js"

window.onload = () => {

    var parent = document.getElementById("gameBoard")

    const side = getCookie('side')

    const roomID = getCookie('room_id')

    console.log(side)

    const userID = localStorage.getItem('userID')

    const gameboard = new chessboard(roomID, userID, null, side, "fast", parent)

    console.log(gameboard)
    
}

class chessboard {

    constructor(roomID, user, oppo, side, type, ref) {

        this.roomID = roomID;
        this.turn = 1;
        this.user = user;
        this.side = side;
        this.oppo = oppo;
        this.type = type;
        this.ref = ref;

        this.moveHistory = [];

        this.gameInfo = document.getElementById("gameInfo");

        this.gameTiles = [...Array(8)].map(e => Array(8));
        this.pieces=[];

        this.timer = 900;

        this.setUpGame()
        this.setUpInfo();

        if(this.side=="white"){this.interID = setInterval(() => {this.awaitGame();}, 1000);}
        if(this.side=="black"){this.interID = setInterval(() => {this.requestGameState();}, 1000);}

    }

    async awaitGame(){

        const queryparams = {
            userID: this.user,
            roomID:this.roomID,
        };
        

        var response = await fetch("./await_game", {

            method: "POST",
            body: JSON.stringify(queryparams),
            headers: {"Content-type": "application/json; charset=UTF-8"}

        });

        response = await response.json()

        console.log("response.black: "+ response.black)
        console.log("this.user: "+ this.user)

        if(response.black != "none"){

            this.pieces.map((tile) => {
                if (tile instanceof gamePiece) {
                    tile.startListen();
                }
            });

            
            clearInterval(this.interID)
    
            this.interID = setInterval(() => { this.timer--; this.timerTxt.textContent = Math.floor(this.timer / 60) + " : " + (this.timer % 60) }, 1000);

        }

    }

    async requestGameState(){

        const queryparams = {
            userID: this.user,
            roomID:this.roomID,
        };

        console.log(queryparams)

        var response = await fetch("./request_game", {

            method: "POST",
            body: JSON.stringify(queryparams),
            headers: {"Content-type": "application/json; charset=UTF-8"}

        });

        response = await response.json()

        this.updateGameState(response)

    }

    updateGameState(JSON){

        if(JSON.turn == this.turn){return}

        clearInterval(this.interID)

        var rows = JSON.game.board.split('/');

        var iPiece= 0;

        this.pieces.forEach((piece)=>{
            piece.remove();
            piece = null
        })

        rows.forEach((row, i)=>{
            var y= 0;
            var tile = rows[i].split('');

            console.log(tile)

            tile.forEach((tile, j)=>{

                if(!isNaN(tile)){

                    y = y + tile

                    return;

                }

                switch(tile){
                    case 'R': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Turm_w.svg",       "white",    { x: i, y: y }, this.whiteGroup, JSON.game.all_moves[iPiece])); break;
                    case 'N': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Springer_w.svg",   "white",    { x: i, y: y }, this.whiteGroup, JSON.game.all_moves[iPiece])); break;
                    case 'B': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Läufer_w.svg",     "white",    { x: i, y: y }, this.whiteGroup, JSON.game.all_moves[iPiece])); break;
                    case 'Q': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Dame_w.svg",       "white",    { x: i, y: y }, this.whiteGroup, JSON.game.all_moves[iPiece])); break;
                    case 'K': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/König_w.svg",      "white",    { x: i, y: y }, this.whiteGroup, JSON.game.all_moves[iPiece])); break;
                    case 'P': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Bauer_w.svg",      "white",    { x: i, y: y }, this.whiteGroup, JSON.game.all_moves[iPiece])); break;

                    case 'r': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Turm.svg",        "black",    { x: i, y: y }, this.blackGroup, JSON.game.all_moves[iPiece])); break;
                    case 'n': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Springer.svg",   "black",    { x: i, y: y }, this.blackGroup, JSON.game.all_moves[iPiece])); break;
                    case 'b': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Läufer.svg",     "black",    { x: i, y: y }, this.blackGroup, JSON.game.all_moves[iPiece])); break;
                    case 'q': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Dame.svg",       "black",    { x: i, y: y }, this.blackGroup, JSON.game.all_moves[iPiece])); break;
                    case 'k': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/König.svg",      "black",    { x: i, y: y }, this.blackGroup, JSON.game.all_moves[iPiece])); break;
                    case 'p': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Bauer.svg",        "black",    { x: i, y: y }, this.blackGroup, JSON.game.all_moves[iPiece])); break;
                }

                y++;

            })

        })

        this.turn++;

        if((this.turn % 2) == 0){

            if(this.side = "black"){

                this.pieces.forEach((piece) => piece.startListen())
                this.interID = setInterval(() => { this.timer--; this.timerTxt.textContent = Math.floor(this.timer / 60) + " : " + (this.timer % 60) }, 1000);

            }else{
                this.interID = setInterval(() => {this.requestGameState();}, 1000);
            }

        }else{

            if(this.side == "black"){

                this.interID = setInterval(() => {this.requestGameState();}, 1000);

            }else{
                this.pieces.forEach((piece) => piece.startListen())
                this.interID = setInterval(() => { this.timer--; this.timerTxt.textContent = Math.floor(this.timer / 60) + " : " + (this.timer % 60) }, 1000);
            }

        }

    }

    setUpGame() {

        const cssVar = window.getComputedStyle(document.documentElement);

        var size = this.ref.clientHeight;

        setAttributes(this.ref, { "width": size, viewBox: "0 0 800 800" })

        this.gameInfo.style.width = (this.ref.parentElement.clientWidth - size) + "px";

        this.tileGroup = setUpSVG("g", {}, this.ref)
        this.blackGroup = setUpSVG("g", {}, this.ref)
        this.whiteGroup = setUpSVG("g", {}, this.ref)

        for (let i = 0; i < 8; i++) {

            for (let j = 0; j < 8; j++) {

                if (((i % 2) == 1 && (j % 2) == 1) || ((i % 2) == 0 && (j % 2) == 0)) {
                    this.gameTiles[j][i] = setUpSVG("rect", { height: 100, width: 100, x: i * 100, y: j * 100, fill: cssVar.getPropertyValue("--colorSignal"), stroke: "black" }, this.tileGroup);
                } else {
                    this.gameTiles[j][i] = setUpSVG("rect", { height: 100, width: 100, x: i * 100, y: j * 100, fill: cssVar.getPropertyValue("--colorBoardDark"), stroke: "black" }, this.tileGroup);
                }

            }
        }

        for(let i=0; i<8; i++){

            var svg = setUpSVG("text", {x: i * 100 + 85, y:15, height: 100, width: 100, class:"boardLettering"}, this.tileGroup)
            svg.textContent=encodeRow(i);

            svg= setUpSVG("text", {x: 5, y: i * 100 + 95, height: 100, width: 100, class:"boardLettering"}, this.tileGroup)
            svg.textContent= i+1;

        }

        this.pieces.push(new gamePiece(this, 0, "./static/Chesspieces/SVG/Turm_w.svg",      "white",    { x: 0, y: 0 }, this.whiteGroup, []));
        this.pieces.push(new gamePiece(this, 1, "./static/Chesspieces/SVG/Springer_w.svg",  "white",    { x: 0, y: 1 }, this.whiteGroup, [{ x: 2, y: 0 }, { x: 2, y: 2 }]));
        this.pieces.push(new gamePiece(this, 2, "./static/Chesspieces/SVG/Läufer_w.svg",    "white",    { x: 0, y: 2 }, this.whiteGroup, []));
        this.pieces.push(new gamePiece(this, 3, "./static/Chesspieces/SVG/Dame_w.svg",      "white",    { x: 0, y: 3 }, this.whiteGroup, []));
        this.pieces.push(new gamePiece(this, 4, "./static/Chesspieces/SVG/König_w.svg",     "white",    { x: 0, y: 4 }, this.whiteGroup, []));
        this.pieces.push(new gamePiece(this, 5, "./static/Chesspieces/SVG/Läufer_w.svg",    "white",    { x: 0, y: 5 }, this.whiteGroup, []));
        this.pieces.push(new gamePiece(this, 6, "./static/Chesspieces/SVG/Springer_w.svg",  "white",    { x: 0, y: 6 }, this.whiteGroup, [{ x: 2, y: 7 }, { x: 2, y: 5 }]));
        this.pieces.push(new gamePiece(this, 7, "./static/Chesspieces/SVG/Turm_w.svg",      "white",    { x: 0, y: 7 }, this.whiteGroup, []));

        this.pieces.push(new gamePiece(this, 0, "./static/Chesspieces/SVG/Turm.svg",        "black",    { x: 7, y: 0 }, this.blackGroup, []));
        this.pieces.push(new gamePiece(this, 1, "./static/Chesspieces/SVG/Springer.svg",    "black",    { x: 7, y: 1 }, this.blackGroup, []));
        this.pieces.push(new gamePiece(this, 2, "./static/Chesspieces/SVG/Läufer.svg",      "black",    { x: 7, y: 2 }, this.blackGroup, []));
        this.pieces.push(new gamePiece(this, 3, "./static/Chesspieces/SVG/Dame.svg",        "black",    { x: 7, y: 3 }, this.blackGroup, []));
        this.pieces.push(new gamePiece(this, 4, "./static/Chesspieces/SVG/König.svg",       "black",    { x: 7, y: 4 }, this.blackGroup, []));
        this.pieces.push(new gamePiece(this, 5, "./static/Chesspieces/SVG/Läufer.svg",      "black",    { x: 7, y: 5 }, this.blackGroup, []));
        this.pieces.push(new gamePiece(this, 6, "./static/Chesspieces/SVG/Springer.svg",    "black",    { x: 7, y: 6 }, this.blackGroup, []));
        this.pieces.push(new gamePiece(this, 7, "./static/Chesspieces/SVG/Turm.svg",        "black",    { x: 7, y: 7 }, this.blackGroup, []));

        for (let i = 0; i < 8; i++) {

            this.pieces.push(new gamePiece(this, 7 + i, "./static/Chesspieces/SVG/Bauer_w.svg", "white", { x: 1, y: i }, this.whiteGroup, [{ x: 2, y: i }, { x: 3, y: i }]))
            this.pieces.push(new gamePiece(this, 7 + i, "./static/Chesspieces/SVG/Bauer.svg", "black", { x: 6, y: i }, this.blackGroup, []))

        }
        
        console.log(this)

    }

    setUpInfo() {

        const txtBox = setUpHTML("div", { width: "100%", height: "300px", class: "textBox" }, this.gameInfo);

        txtBox.appendChild(document.createTextNode(this.user + " vs. " + this.oppo));

        this.timerTxt = setUpHTML("div", { width: "100%", height: "300px", class: "timer" }, this.gameInfo);

        this.timerTxt.textContent = "Waiting for player..."

        this.moveRef = setUpHTML("div", { width: "100%", class: "moveHistory" }, this.gameInfo);

        

    }

}
