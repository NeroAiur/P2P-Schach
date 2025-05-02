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

    }

    async awaitGame(){

        const queryparams = {
            userID: this.user,
            roomID:this.roomID,
        };

        var response = await (await fetch("./await_game", {

            method: "POST",
            body: JSON.stringify(queryparams),
            headers: {"Content-type": "application/json; charset=UTF-8"}

        }).json());

        if(response.black != "none"){

            this.gameBoard.map((row)=>{
                row.map((tile)=>{
                    
                    if(tile instanceof gamePiece){
                        tile.startListen();
                    }
    
                })
            })
    
            setInterval(() => { this.timer--; this.timerTxt.textContent = Math.floor(this.timer / 60) + " : " + (this.timer % 60) }, 1000);

            clearInterval(this.interID)

        }

    }

    async requestGameState(){

        const queryparams = {
            userID: this.user,
            roomID:this.roomID,
        };

        var response = await (await fetch("./await_game", {

            method: "POST",
            body: JSON.stringify(queryparams),
            headers: {"Content-type": "application/json; charset=UTF-8"}

        }).json());

    }

    updateGameState(board, possibleMoves){
        var rows = board.split('/');
        var tile = rows.split('');

        var iPiece= 0;

        this.pieces.forEach((piece)=>{
            piece.remove();
            piece = null
        })

        rows.forEach((row, i)=>{
            var y= 0;

            tile.forEach((tile, j)=>{
                if(!isNaN(tile)){
                    y = y + tile
                }

                switch(tile){
                    case 'R': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Turm_w.svg", "white", { x: i, y: y }, whiteGroup, possibleMoves[iPiece]));
                    case 'N': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Springer_w.svg", "white", { x: i, y: y }, whiteGroup, possibleMoves[iPiece]));
                    case 'B': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Läufer_w.svg", "white", { x: i, y: y }, whiteGroup, possibleMoves[iPiece]));
                    case 'Q': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Dame_w.svg", "white", { x: i, y: y }, whiteGroup, possibleMoves[iPiece]));
                    case 'K': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/König_w.svg", "white", { x: i, y: y }, whiteGroup, possibleMoves[iPiece]));
                    case 'P': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Bauer_w.svg", "white", { x: i, y: y }, whiteGroup, possibleMoves[iPiece]))

                    case 'r': this.pieces.push(new gamePiece(this,iPiece, "./static/Chesspieces/SVG/Turm_w.svg", "black", { x: i, y: y }, whiteGroup, possibleMoves[iPiece]));
                    case 'n': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Springer_w.svg", "black", { x: i, y: y }, whiteGroup, possibleMoves[iPiece]));
                    case 'b': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Läufer_w.svg", "black", { x: i, y: y }, whiteGroup, possibleMoves[iPiece]));
                    case 'q': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Dame_w.svg", "black", { x: i, y: y }, whiteGroup, possibleMoves[iPiece]));
                    case 'k': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/König_w.svg", "black", { x: i, y: y }, whiteGroup, possibleMoves[iPiece]));
                    case 'p': this.pieces.push(new gamePiece(this, iPiece, "./static/Chesspieces/SVG/Bauer.svg", "black", { x: i, y: i }, blackGroup, possibleMoves[iPiece]))
                }

            })

        })

    }

    setUpGame() {

        const cssVar = window.getComputedStyle(document.documentElement);

        var size = this.ref.clientHeight;

        setAttributes(this.ref, { "width": size, viewBox: "0 0 800 800" })

        this.gameInfo.style.width = (this.ref.parentElement.clientWidth - size) + "px";

        const tileGroup = setUpSVG("g", {}, this.ref)
        const blackGroup = setUpSVG("g", {}, this.ref)
        const whiteGroup = setUpSVG("g", {}, this.ref)

        for (let i = 0; i < 8; i++) {

            for (let j = 0; j < 8; j++) {

                if (((i % 2) == 1 && (j % 2) == 1) || ((i % 2) == 0 && (j % 2) == 0)) {
                    this.gameTiles[j][i] = setUpSVG("rect", { height: 100, width: 100, x: i * 100, y: j * 100, fill: cssVar.getPropertyValue("--colorSignal"), stroke: "black" }, tileGroup);
                } else {
                    this.gameTiles[j][i] = setUpSVG("rect", { height: 100, width: 100, x: i * 100, y: j * 100, fill: cssVar.getPropertyValue("--colorBoardDark"), stroke: "black" }, tileGroup);
                }

            }
        }

        for(let i=0; i<8; i++){

            var svg = setUpSVG("text", {x: i * 100 + 85, y:15, height: 100, width: 100, class:"boardLettering"}, tileGroup)
            svg.textContent=encodeRow(i);

            svg= setUpSVG("text", {x: 5, y: i * 100 + 95, height: 100, width: 100, class:"boardLettering"}, tileGroup)
            svg.textContent= i+1;

        }

        this.pieces.push(new gamePiece(this, 0, "./static/Chesspieces/SVG/Turm_w.svg", "white", { x: 0, y: 0 }, whiteGroup, []));
        this.pieces.push(new gamePiece(this, 1, "./static/Chesspieces/SVG/Springer_w.svg", "white", { x: 0, y: 1 }, whiteGroup, [{ x: 2, y: 0 }, { x: 2, y: 2 }]));
        this.pieces.push(new gamePiece(this, 2, "./static/Chesspieces/SVG/Läufer_w.svg", "white", { x: 0, y: 2 }, whiteGroup, []));
        this.pieces.push(new gamePiece(this, 3, "./static/Chesspieces/SVG/Dame_w.svg", "white", { x: 0, y: 3 }, whiteGroup, []));
        this.pieces.push(new gamePiece(this, 4, "./static/Chesspieces/SVG/König_w.svg", "white", { x: 0, y: 4 }, whiteGroup, []));
        this.pieces.push(new gamePiece(this, 5, "./static/Chesspieces/SVG/Läufer_w.svg", "white", { x: 0, y: 5 }, whiteGroup, []));
        this.pieces.push(new gamePiece(this, 6, "./static/Chesspieces/SVG/Springer_w.svg", "white", { x: 0, y: 6 }, whiteGroup, [{ x: 2, y: 7 }, { x: 2, y: 5 }]));
        this.pieces.push(new gamePiece(this, 7, "./static/Chesspieces/SVG/Turm_w.svg", "white", { x: 0, y: 7 }, whiteGroup, []));

        this.pieces.push(new gamePiece(this, 0, "./static/Chesspieces/SVG/Turm.svg", "black", { x: 7, y: 0 }, blackGroup, []));
        this.pieces.push(new gamePiece(this, 1, "./static/Chesspieces/SVG/Springer.svg", "black", { x: 7, y: 1 }, blackGroup, []));
        this.pieces.push(new gamePiece(this, 2, "./static/Chesspieces/SVG/Läufer.svg", "black", { x: 7, y: 2 }, blackGroup, []));
        this.pieces.push(new gamePiece(this, 3, "./static/Chesspieces/SVG/Dame.svg", "black", { x: 7, y: 3 }, blackGroup, []));
        this.pieces.push(new gamePiece(this, 4, "./static/Chesspieces/SVG/König.svg", "black", { x: 7, y: 4 }, blackGroup, []));
        this.pieces.push(new gamePiece(this, 5, "./static/Chesspieces/SVG/Läufer.svg", "black", { x: 7, y: 5 }, blackGroup, []));
        this.pieces.push(new gamePiece(this, 6, "./static/Chesspieces/SVG/Springer.svg", "black", { x: 7, y: 6 }, blackGroup, []));
        this.pieces.push(new gamePiece(this, 7, "./static/Chesspieces/SVG/Turm.svg", "black", { x: 7, y: 7 }, blackGroup, []));

        for (let i = 0; i < 8; i++) {

            this.pieces.push(new gamePiece(this, 7 + i, "./static/Chesspieces/SVG/Bauer_w.svg", "white", { x: 1, y: i }, whiteGroup, [{ x: 2, y: i }, { x: 3, y: i }]))
            this.pieces.push(new gamePiece(this, 7 + i, "./static/Chesspieces/SVG/Bauer.svg", "black", { x: 6, y: i }, blackGroup, []))

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
