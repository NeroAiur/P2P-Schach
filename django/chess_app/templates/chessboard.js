import { setAttributes, setUpHTML, setUpSVG } from "./helperScripts.js";

window.onload = () => {

    var parent = document.getElementById("gameBoard")
    const gameboard = new chessboard(null, null, "fast", parent)
}

class chessboard{


    constructor(user, oppo, type, ref){
        this.user = user;
        this.oppo = oppo;
        this.type = type;
        this.ref = ref;

        this.setUpGame();
    }

    setUpGame(){

        var size = this.ref.clientHeight;

        console.log(size)

        setAttributes(this.ref, {"width": size, viewBox:"0 0 800 800"})

        for(let i =0; i<8; i++){
            for(let j=0; j<8; j++){
                setUpSVG("rect",{height: 100, width: 100, x: i*100, y: j*100, color: "#FFFFFF", border:"1px black"},this.ref)
            }
        }
    }

}