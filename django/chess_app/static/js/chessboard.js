import { setAttributes, setUpHTML, setUpSVG, encodeRow, decodeRow, getCookie } from "./helperScripts.js";
import { gamePiece } from "./pieces.js"

window.onload = () => {

    var parent = document.getElementById("gameBoard")

    const side = getCookie('side')

    const roomID = getCookie('room_id')

    console.log(side)

    const userID = localStorage.getItem('userID')

    const gameboard = new chessboard(roomID, userID, "???", side, "fast", parent)

    console.log(gameboard)
    
}

class chessboard {

    constructor(roomID, user, oppo, side, type, ref) {

        this.roomID = roomID;
        this.turn = 0;
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

        this.requestGameState();

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

        const decodedMoves = this.decodeMoves(JSON.game.all_moves);

        this.pieces.forEach((piece)=>{
            piece.remove();
        })

        this.pieces.splice(0, this.pieces.length);

        rows.forEach((row, i)=> {
            var y= 0;
            var tile = rows[i].split('');

            console.log(tile)

            tile.forEach((tile, j) => {

                if(!isNaN(tile)){
                    console.log('number')

                    y = y + parseInt(tile)

                }

                if(decodedMoves[i][y] == undefined){
                    decodedMoves[i][y] == []
                }

                switch(tile){
                    case 'R': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Turm_w.svg",       "white",    { x: i, y: y }, this.whiteGroup, decodedMoves[i][y])); y++; break;
                    case 'N': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Springer_w.svg",   "white",    { x: i, y: y }, this.whiteGroup, decodedMoves[i][y])); y++; break;
                    case 'B': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Läufer_w.svg",     "white",    { x: i, y: y }, this.whiteGroup, decodedMoves[i][y])); y++; break;
                    case 'Q': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Dame_w.svg",       "white",    { x: i, y: y }, this.whiteGroup, decodedMoves[i][y])); y++; break;
                    case 'K': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/König_w.svg",      "white",    { x: i, y: y }, this.whiteGroup, decodedMoves[i][y])); y++; break;
                    case 'P': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Bauer_w.svg",      "white",    { x: i, y: y }, this.whiteGroup, decodedMoves[i][y])); y++; break;

                    case 'r': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Turm.svg",        "black",    { x: i, y: y }, this.blackGroup, decodedMoves[i][y])); y++; break;
                    case 'n': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Springer.svg",   "black",    { x: i, y: y }, this.blackGroup, decodedMoves[i][y])); y++; break;
                    case 'b': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Läufer.svg",     "black",    { x: i, y: y }, this.blackGroup, decodedMoves[i][y])); y++; break;
                    case 'q': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Dame.svg",       "black",    { x: i, y: y }, this.blackGroup, decodedMoves[i][y])); y++; break;
                    case 'k': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/König.svg",      "black",    { x: i, y: y }, this.blackGroup, decodedMoves[i][y])); y++; break;
                    case 'p': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Bauer.svg",        "black",    { x: i, y: y }, this.blackGroup, decodedMoves[i][y])); y++; break;

                    default: break;
                }

            })

        })

        this.turn++;

        const evenOdd= this.turn % 2; 

        console.log(this)

        if(evenOdd == 0){
            console.log("1")
            if(this.side == "black"){
                console.log("2")
                this.pieces.forEach((piece) => piece.startListen())
                this.interID = setInterval(() => { this.timer--; this.timerTxt.textContent = Math.floor(this.timer / 60) + " : " + (this.timer % 60) }, 1000);

            }else if(this.side == "white"){
                console.log("3")
                this.interID = setInterval(() => {this.requestGameState();}, 1000);
            }

        }else{

            if(this.side == "black"){
                console.log("4")
                this.interID = setInterval(() => {this.requestGameState();}, 1000);

            }else if(this.side =="white"){
                console.log("5")
                this.pieces.forEach((piece) => piece.startListen())
                this.interID = setInterval(() => { this.timer--; this.timerTxt.textContent = Math.floor(this.timer / 60) + " : " + (this.timer % 60) }, 1000);
            }

        }

    }

    decodeMoves(allMoves){

        var mappedMoves = [...Array(8)].map(e => Array(8));

        allMoves.forEach((move) => {

            var letters = move.split('');

            const moveCoords = {
                yo: decodeRow(letters[0]),
                xo: parseInt(letters[1]) - 1,
                yp: decodeRow(letters[2]),
                xp: parseInt(letters[3]) - 1,
            }

            if(mappedMoves[moveCoords.xo][moveCoords.yo] == undefined){
                mappedMoves[moveCoords.xo][moveCoords.yo]= [{x: moveCoords.xp, y: moveCoords.yp}];
            }else{
                mappedMoves[moveCoords.xo][moveCoords.yo].push({x: moveCoords.xp, y: moveCoords.yp})
            }

        })

        return mappedMoves
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
