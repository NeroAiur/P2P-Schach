import { setAttributes, setUpHTML, setUpSVG } from "./helperScripts.js";
import {gamePiece} from "./pieces.js"

window.onload = () => {

    var parent = document.getElementById("gameBoard")
    const gameboard = new chessboard(null, null, "white", "fast", parent)
}

class chessboard{

    constructor(user, oppo, side, type, ref){
        this.user = user;
        this.side = side;
        this.oppo = oppo;
        this.type = type;
        this.ref = ref;

        this.gameInfo = document.getElementById("gameInfo");

        this.gameBoard= [...Array(8)].map(e => Array(8));


        this.setUpGame();
    }

    setUpGame(){

        var size = this.ref.clientHeight;

        setAttributes(this.ref, {"width": size, viewBox:"0 0 800 800"})

        setAttributes(this.gameInfo, {width: this.ref.parentElement.clientWidth-size, height: size})

        const tileGroup = setUpSVG("g",{},this.ref)
        const blackGroup = setUpSVG("g",{},this.ref)
        const whiteGroup = setUpSVG("g",{},this.ref)

        for(let i =0; i<8; i++){

            for(let j=0; j<8; j++){

                setUpSVG("rect",{height: 100, width: 100, x: i*100, y: j*100, fill: "#FFFFFF", stroke:"black"},tileGroup);

            }
        }

        this.gameBoard [0][0] = new gamePiece(this, 0,"./Chesspieces/SVG/Turm.svg", "white",{x:0,y:0},whiteGroup);
        this.gameBoard[0][1] = new gamePiece(this, 1,"./Chesspieces/SVG/Springer.svg", "white",{x:0,y:1},whiteGroup);
        this.gameBoard[0][2] = new gamePiece(this, 2,"./Chesspieces/SVG/Läufer.svg", "white",{x:0,y:2},whiteGroup);
        this.gameBoard[0][3] = new gamePiece(this, 3,"./Chesspieces/SVG/Dame.svg", "white",{x:0,y:3},whiteGroup);
        this.gameBoard[0][3] = new gamePiece(this, 4,"./Chesspieces/SVG/König.svg", "white",{x:0,y:4},whiteGroup);
        this.gameBoard[0][2] = new gamePiece(this, 5,"./Chesspieces/SVG/Läufer.svg", "white",{x:0,y:5},whiteGroup);
        this.gameBoard[0][1] = new gamePiece(this, 6,"./Chesspieces/SVG/Springer.svg", "white",{x:0,y:6},whiteGroup);
        this.gameBoard [0][0] = new gamePiece(this, 7,"./Chesspieces/SVG/Turm.svg", "white",{x:0,y:7},whiteGroup);

        this.gameBoard [7][0] = new gamePiece(this, 0,"./Chesspieces/SVG/Turm.svg", "black", {x:7,y:0}, blackGroup);
        this.gameBoard[7][1] = new gamePiece(this, 1,"./Chesspieces/SVG/Springer.svg", "black", {x:7,y:1}, blackGroup);
        this.gameBoard[7][2] = new gamePiece(this, 2,"./Chesspieces/SVG/Läufer.svg", "black", {x:7,y:2}, blackGroup);
        this.gameBoard[7][3] = new gamePiece(this, 3,"./Chesspieces/SVG/Dame.svg", "black", {x:7,y:3}, blackGroup);
        this.gameBoard[7][3] = new gamePiece(this, 4,"./Chesspieces/SVG/König.svg", "black", {x:7,y:4}, blackGroup);
        this.gameBoard[7][2] = new gamePiece(this, 5,"./Chesspieces/SVG/Läufer.svg", "black", {x:7,y:5}, blackGroup);
        this.gameBoard[7][1] = new gamePiece(this, 6,"./Chesspieces/SVG/Springer.svg", "black", {x:7,y:6}, blackGroup);
        this.gameBoard [7][0] = new gamePiece(this, 7,"./Chesspieces/SVG/Turm.svg", "black", {x:7,y:7}, blackGroup);

        for(let i=0; i<8; i++){

            this.gameBoard[1][i] = new gamePiece(this, 7+i,"./Chesspieces/SVG/Bauer.svg", "white", {x:1,y:i}, whiteGroup)
            this.gameBoard[6][i] = new gamePiece(this, 7+i,"./Chesspieces/SVG/Bauer.svg", "black", {x:6,y:i}, blackGroup)

        }

        console.log(this)

    }

}
