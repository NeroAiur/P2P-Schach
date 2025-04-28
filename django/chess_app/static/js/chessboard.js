{ }

import { setAttributes, setUpHTML, setUpSVG, encodeRow } from "./helperScripts.js";
import { gamePiece } from "./pieces.js"

window.onload = () => {

    var parent = document.getElementById("gameBoard")
    const gameboard = new chessboard("0000", null, "white", "fast", parent)
    
}

class chessboard {

    constructor(user, oppo, side, type, ref) {

        this.user = user;
        this.side = side;
        this.oppo = oppo;
        this.type = type;
        this.ref = ref;

        this.moveHistory = [];

        this.gameInfo = document.getElementById("gameInfo");

        this.gameBoard = [...Array(8)].map(e => Array(8));
        this.gameTiles = [...Array(8)].map(e => Array(8));

        this.timer = 900;

        this.setUpGame()
        this.setUpInfo();

        this.interID = setInterval(() => this.awaitGame(), 2500);

    }

    async awaitGame(){

        const queryparams = {
            user: this.user,
        };

        var response = await (await fetch("./lobby", {

            method: "POST",
            body: JSON.stringify(queryparams),
            headers: {"Content-type": "application/json; charset=UTF-8"}

        }));

        if(true){

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

        this.gameBoard[0][0] = new gamePiece(this, 0, "./static/Chesspieces/SVG/Turm_w.svg", "white", { x: 0, y: 0 }, whiteGroup, []);
        this.gameBoard[0][1] = new gamePiece(this, 1, "./static/Chesspieces/SVG/Springer_w.svg", "white", { x: 0, y: 1 }, whiteGroup, [{ x: 2, y: 0 }, { x: 2, y: 2 }]);
        this.gameBoard[0][2] = new gamePiece(this, 2, "./static/Chesspieces/SVG/Läufer_w.svg", "white", { x: 0, y: 2 }, whiteGroup, []);
        this.gameBoard[0][3] = new gamePiece(this, 3, "./static/Chesspieces/SVG/Dame_w.svg", "white", { x: 0, y: 3 }, whiteGroup, []);
        this.gameBoard[0][4] = new gamePiece(this, 4, "./static/Chesspieces/SVG/König_w.svg", "white", { x: 0, y: 4 }, whiteGroup, []);
        this.gameBoard[0][5] = new gamePiece(this, 5, "./static/Chesspieces/SVG/Läufer_w.svg", "white", { x: 0, y: 5 }, whiteGroup, []);
        this.gameBoard[0][6] = new gamePiece(this, 6, "./static/Chesspieces/SVG/Springer_w.svg", "white", { x: 0, y: 6 }, whiteGroup, [{ x: 2, y: 7 }, { x: 2, y: 5 }]);
        this.gameBoard[0][7] = new gamePiece(this, 7, "./static/Chesspieces/SVG/Turm_w.svg", "white", { x: 0, y: 7 }, whiteGroup, []);

        this.gameBoard[7][0] = new gamePiece(this, 0, "./static/Chesspieces/SVG/Turm.svg", "black", { x: 7, y: 0 }, blackGroup, []);
        this.gameBoard[7][1] = new gamePiece(this, 1, "./static/Chesspieces/SVG/Springer.svg", "black", { x: 7, y: 1 }, blackGroup, []);
        this.gameBoard[7][2] = new gamePiece(this, 2, "./static/Chesspieces/SVG/Läufer.svg", "black", { x: 7, y: 2 }, blackGroup, []);
        this.gameBoard[7][3] = new gamePiece(this, 3, "./static/Chesspieces/SVG/Dame.svg", "black", { x: 7, y: 3 }, blackGroup, []);
        this.gameBoard[7][4] = new gamePiece(this, 4, "./static/Chesspieces/SVG/König.svg", "black", { x: 7, y: 4 }, blackGroup, []);
        this.gameBoard[7][5] = new gamePiece(this, 5, "./static/Chesspieces/SVG/Läufer.svg", "black", { x: 7, y: 5 }, blackGroup, []);
        this.gameBoard[7][6] = new gamePiece(this, 6, "./static/Chesspieces/SVG/Springer.svg", "black", { x: 7, y: 6 }, blackGroup, []);
        this.gameBoard[7][7] = new gamePiece(this, 7, "./static/Chesspieces/SVG/Turm.svg", "black", { x: 7, y: 7 }, blackGroup, []);

        for (let i = 0; i < 8; i++) {

            this.gameBoard[1][i] = new gamePiece(this, 7 + i, "./static/Chesspieces/SVG/Bauer_w.svg", "white", { x: 1, y: i }, whiteGroup, [{ x: 2, y: i }, { x: 3, y: i }])
            this.gameBoard[6][i] = new gamePiece(this, 7 + i, "./static/Chesspieces/SVG/Bauer.svg", "black", { x: 6, y: i }, blackGroup, [])

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
