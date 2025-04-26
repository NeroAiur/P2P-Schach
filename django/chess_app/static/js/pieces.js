import { setAttributes, setUpHTML, setUpSVG } from "./helperScripts.js";

export class gamePiece {

    id;
    svg;
    pos;

    constructor(game, id, svg, side, pos, parent, possibleMoves) {

        this.game = game;
        this.id = id;
        this.parent = parent;
        this.pos = pos;
        this.side = side;
        this.possibleMoves = possibleMoves;

        this.listener = Array(3)

        this.svg = setUpSVG("image", { href: svg, height: 100, width: 100, x: pos.y * 100, y: pos.x * 100, "user-select": "none" }, this.parent);

        if (this.side == this.game.side) {

            this.listener[0] = this.startDrag.bind(this);

            this.svg.addEventListener("mousedown", this.listener[0])
        }

    }

    startDrag() {

        this.possibleMoves.forEach((tile) => {

            const svg = this.game.gameTiles[tile.x][tile.y];
            setAttributes(svg, { fill: "#BF3B91" })

        })

        this.svg.removeEventListener("mousedown", this.listener[0]);

        this.listener[1] = this.dragPiece.bind(this);
        this.listener[2] = this.endDrag.bind(this);

        window.addEventListener("mousemove", this.listener[1]);
        window.addEventListener("mouseup", this.listener[2]);

        console.log("1");
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

        const x = parseInt(this.svg.getAttribute("y")) + 50;

        const y = parseInt(this.svg.getAttribute("x")) + 50;


        this.possibleMoves.forEach((tile) => {

            const tileLowerX = tile.x * 100;
            const tileUpperX = (tile.x + 1) * 100;

            const tileLowerY = tile.y * 100;
            const tileUpperY = (tile.y + 1) * 100;

            if ((tileLowerX <= x) && (x <= tileUpperX) && (tileLowerY < y) && (y < tileUpperY)) {

                console.log({ x: x, y: y, LX: tileLowerX, UX: tileUpperX, LY: tileLowerY, UY: tileUpperY })

                //send Move
                this.pos = tile;

                setAttributes(this.svg, { x: this.pos.y * 100, y: this.pos.x * 100 })

                this.possibleMoves.forEach((tile) => {

                    const svg = this.game.gameTiles[tile.x][tile.y];

                    if (((tile.y % 2) == 1 && (tile.x % 2) == 1) || ((tile.y % 2) == 0 && (tile.x % 2) == 0)) {
                        setAttributes(svg, { fill: "#FFFFFF" })
                    } else { setAttributes(svg, { fill: "#DDDDDD" }) }
                })

                return

            }

        })

        window.removeEventListener("mousemove", this.listener[1])
        window.removeEventListener("mouseup", this.listener[2])

        this.listener[0] = this.startDrag.bind(this);

        this.svg.addEventListener("mousedown", this.listener[0])

        setAttributes(this.svg, { x: this.pos.y * 100, y: this.pos.x * 100 })

        console.log("3")
    }

}

