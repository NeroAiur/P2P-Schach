export function setAttributes(el, attrs) {

    Object.keys(attrs).forEach(key => el.setAttribute(key, attrs[key]));

}

export function setUpHTML(type, attributes, parent){

    let html = document.createElement(type);

    setAttributes(html, attributes);

    parent.appendChild(html);

    return(html)

}

export function setUpSVG(type, attributes, parent){

    let html = document.createElementNS("http://www.w3.org/2000/svg",type);

    setAttributes(html, attributes);

    parent.appendChild(html);

    return(html)

}

export function cleanInput(input){

    //do stuff

    return input

}

export function hash(input){

    hashedInput = digest("SHA-256", input)

    return hashedInput

}