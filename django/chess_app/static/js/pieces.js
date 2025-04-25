import { setAttributes, setUpHTML, setUpSVG } from "./helperScripts.js";


export class gamePiece {

    id;
    svg;
    pos;

    constructor(game, id, svg, side, pos, parent) {

        this.game = game;
        this.id = id;
        this.parent = parent;
        this.pos = pos;
        this.side = side;

        this.svg = setUpSVG("image", { href: svg, height: 100, width: 100, x: pos.y * 100, y: pos.x * 100 }, this.parent);

        if (this.side == this.game.side) {
            this.svg.addEventListener("mousedown", this.startDrag.bind(this))
        }

    }

    startDrag() {
        this.svg.removeEventListener("mousedown", this.startDrag)

        this.game.ref.addEventListener("mousemove", this.dragPiece.bind(this))
        this.svg.addEventListener("mouseup", this.endDrag.bind(this))

        console.log("1")
    }

    dragPiece(event) {
        const x = this.svg.getAttribute("x");

        const y = this.svg.getAttribute("y");

        const scalar = 800 / this.game.ref.clientHeight;

        console.log(scalar)

        setAttributes(this.svg, { x: parseInt(x) + parseInt(event.movementX) * scalar, y: parseInt(y) + parseInt(event.movementY) * scalar });

        console.log("2")

    }

    endDrag() {
        this.game.ref.removeEventListener("mousemove", this.dragPiece)
        this.svg.removeEventListener("mouseup", this.endDrag)

        console.log("3")
    }


}