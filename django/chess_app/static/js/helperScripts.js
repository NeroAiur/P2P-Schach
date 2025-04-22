export function setAttributes(el, attrs) {

    Object.keys(attrs).forEach(key => el.setAttribute(key, attrs[key]));

}

export function setUpHTML(type, attributes, parent){

    let html = document.createElement(type);

    setAttributes(html, attributes);

    parent.appendChild(html);

    return(html)

}