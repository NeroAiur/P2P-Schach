

//Applies css styles "attrs" in form JSON to element "el".

export function setAttributes(el, attrs) {

    Object.keys(attrs).forEach(key => el.setAttribute(key, attrs[key]));

}

//Creates and appends HTML element

export function setUpHTML(type, attributes, parent) {

    let html = document.createElement(type);

    setAttributes(html, attributes);

    parent.appendChild(html);

    return (html)

}



export function setUpSVG(type, attributes, parent) {

    let html = document.createElementNS("http://www.w3.org/2000/svg", type);

    setAttributes(html, attributes);

    parent.appendChild(html);

    return (html)

}



export function cleanInput(input) {

    //do stuff

    return input

}



export async function hash(input) {

    const encoder = new TextEncoder();
    const data = encoder.encode(input); 

    const byteArray = await window.crypto.subtle.digest("SHA-256", data)

    const hashedInput = new Int32Array(byteArray);

    return hashedInput

}



export function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let i = 0; i < cookies.length; i++) {

            const cookie = cookies[i].trim();

            // Prüfe, ob dieses Cookie mit dem gewünschten Namen beginnt
            if (cookie.startsWith(name + "=")) {

                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

                break;

            }

        }

    }

    return cookieValue;

}



export function encodeRow(row){

    return String.fromCharCode(65 + row);

}



export function decodeRow(row){

    return (parseInt(row.charCodeAt(0)) - 65)
    
}