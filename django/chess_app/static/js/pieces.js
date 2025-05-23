import { setAttributes, setUpHTML, setUpSVG, getCookie, encodeRow } from "./helperScripts.js";



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

        this.cssVar = window.getComputedStyle(document.documentElement);

        this.listener = Array(3)

        this.svg = setUpSVG("image", { href: svg, height: 100, width: 100, x: pos.y * 100, y: pos.x * 100, "user-select": "none" }, this.parent);

    }



    remove() {
        this.svg.remove();
    }

    /*Makes game pieces interactable, when its your turn.*/

    startListen() {
        if (this.possibleMoves == undefined) { return }

        if (this.side == this.game.side) {

            this.listener[0] = this.startDrag.bind(this);

            this.svg.addEventListener("mousedown", this.listener[0])
        }

    }



    stopListen() {

        this.svg.removeEventListener("mousedown", this.listener[0])

    }

    /*Highlights the tiles, that the game piece can move to and attaches it to the cursor. */

    startDrag() {

        this.possibleMoves.forEach((tile) => {

            const svg = this.game.gameTiles[tile.x][tile.y];
            setAttributes(svg, { fill: this.cssVar.getPropertyValue("--colorHighlight") })

        })

        this.svg.removeEventListener("mousedown", this.listener[0]);

        this.listener[1] = this.dragPiece.bind(this);
        this.listener[2] = this.endDrag.bind(this);

        window.addEventListener("mousemove", this.listener[1]);
        window.addEventListener("mouseup", this.listener[2]);

    }

    /*Scalar is needed, because the SVG view window is always 800 x 800, while the tracked distance is dependingon your browser window. */

    dragPiece(event) {

        const x = this.svg.getAttribute("x");
        const y = this.svg.getAttribute("y");

        const scalar = 800 / this.game.ref.clientHeight;

        setAttributes(this.svg, { x: parseInt(x) + parseInt(event.movementX) * scalar, y: parseInt(y) + parseInt(event.movementY) * scalar });

    }

    /*Determines if the position of the piece at the end of drag is a valid move and sends that move to the backend and updates the game statewith the response*/

    endDrag() {

        const x = parseInt(this.svg.getAttribute("y")) + 50;
        const y = parseInt(this.svg.getAttribute("x")) + 50;

        this.possibleMoves.forEach(async (tile) => {

            const tileLowerX = tile.x * 100;
            const tileUpperX = (tile.x + 1) * 100;

            const tileLowerY = tile.y * 100;
            const tileUpperY = (tile.y + 1) * 100;

            if ((tileLowerX <= x) && (x <= tileUpperX) && (tileLowerY < y) && (y < tileUpperY)) {

                this.game.pieces.forEach((piece) => piece.stopListen())
                //send Move
                const queryparams = {

                    roomID: this.game.roomID,
                    userID: this.game.user,
                    side: this.side,
                    move: encodeRow(this.pos.y) + (this.pos.x + 1) + " to " + encodeRow(tile.y) + (tile.x + 1),

                };

                this.pos = tile;

                const csrftoken = getCookie('csrftoken');

                var response = await fetch("/send_move", {

                    method: "POST",
                    body: JSON.stringify(queryparams),
                    headers: {

                        "Content-Type": "application/json; charset=UTF-8",
                        "X-CSRFToken": csrftoken

                    },
                    credentials: "include"

                });

                response = await response.json();

                this.game.updateGameState(response)

                setAttributes(this.svg, { x: this.pos.y * 100, y: this.pos.x * 100 })

                return

            }

        })

        this.possibleMoves.forEach((tile) => {

            const svg = this.game.gameTiles[tile.x][tile.y];

            if (((tile.y % 2) == 1 && (tile.x % 2) == 1) || ((tile.y % 2) == 0 && (tile.x % 2) == 0)) {

                setAttributes(svg, { fill: this.cssVar.getPropertyValue("--colorSignal") })

            } else {

                setAttributes(svg, { fill: this.cssVar.getPropertyValue("--colorBoardDark") })

            }

        })

        window.removeEventListener("mousemove", this.listener[1])
        window.removeEventListener("mouseup", this.listener[2])

        this.listener[0] = this.startDrag.bind(this);

        this.svg.addEventListener("mousedown", this.listener[0])

        setAttributes(this.svg, { x: this.pos.y * 100, y: this.pos.x * 100 })

    }



}

