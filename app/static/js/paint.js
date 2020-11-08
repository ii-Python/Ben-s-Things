const canvas = document.getElementById("paint");
const context = canvas.getContext("2d");

console.log("iiPython's Paint.js v1.04");

// Check if we got an image url
const search = window.location.href.split("?")[1];

if (search !== null) {

    const params = new URLSearchParams(search);
    const parameters = {};

    for (let value of params.keys()) {
        parameters[value] = params.get(value);
    }

    if ("image" in parameters) {

        var imageURL = parameters["image"];

        var image = new Image();
        image.src = imageURL;

        image.onload = function() {
            context.drawImage(image, 0, 0);
        }

    }

}

// Mouse positioning
function getMousePos(canvas, evt) {
    var rect = canvas.getBoundingClientRect ();
    return {
      x: evt.clientX - rect.left,
      y: evt.clientY - rect.top
    };
}

// Mouse wheel logic
function wheelDirection(e) {
    var delta = null, direction = false;
    if (e.wheelDelta) {
        delta = e.wheelDelta / 60;
    } else if (e.detail) {
        delta = -e.detail / 2;
    }
    if (delta !== null) {
        direction = delta> 0? 1: 0;
    } else {
        direction = 1
    }

    return direction;
}

// Logic
let MOUSE_X = 0;
let MOUSE_Y = 0
let STROKESIZE = 5;
let MOUSEDOWN = false;
let CURRENTCOLOR = "black";

let TOOL = "brush";

canvas.onmousemove = function(event) {
    if (MOUSEDOWN) {
        drawLine (context, MOUSE_X, MOUSE_Y, event.offsetX, event.offsetY);
        MOUSE_X = event.offsetX;
        MOUSE_Y = event.offsetY;
    }
}

function drawLine(context, x1, y1, x2, y2) {
    
    // Begin drawing
    context.beginPath ();

    // Customization
    if (TOOL == "brush") {
        context.strokeStyle = CURRENTCOLOR;
        context.lineWidth = STROKESIZE;
    } else if (TOOL == "eraser") {
        context.strokeStyle = "white";
        context.lineWidth = 35;
    }

    // Make the line
    context.moveTo (x1, y1);
    context.lineTo (x2, y2);

    // Draw and clean up
    context.stroke ();
    context.closePath ();
}

canvas.onmousedown = function(event) {
    MOUSE_X = event.offsetX;
    MOUSE_Y = event.offsetY;
    MOUSEDOWN = true;
}
canvas.onmouseup = function(event) {
    if (MOUSEDOWN) {
        drawLine (context, MOUSE_X, MOUSE_Y, event.offsetX, event.offsetY);
        MOUSE_X = 0;
        MOUSE_Y = 0;
        MOUSEDOWN = false;
    }
}

// Stroke increase
canvas.onwheel = function(event) {
    if (wheelDirection (event) == 1) {
        if (STROKESIZE <100) {
            STROKESIZE ++;
        }
    } else {
        if (STROKESIZE) {
            STROKESIZE--;
        }
    }
}
