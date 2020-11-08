// Keybinds
let CTRLDOWN = false;
let STATUSELEM = document.getElementById("status");

document.onkeydown = function(event) {

    event = event || window.event;

    // Check for control key
    if (event.keyCode == 17 || event.keyCode == 91) CTRLDOWN = true;

    // Check for eraser
    if (event.keyCode == 69) {

        if (TOOL == "brush") {
            TOOL = "eraser"
            STATUSELEM.innerText = "Eraser enabled";
        } else if (TOOL == "eraser") {
            TOOL = "brush"
            STATUSELEM.innerText = null;
        }
    }

    // Color changing
    if (event.keyCode == 49) CURRENTCOLOR = "black";
    if (event.keyCode == 50) CURRENTCOLOR = "#00008B";
    if (event.keyCode == 51) CURRENTCOLOR = "#0091EA";
    if (event.keyCode == 52) CURRENTCOLOR = "#FF0081";
    if (event.keyCode == 53) CURRENTCOLOR = "#329932";
    if (event.keyCode == 54) CURRENTCOLOR = "#FFFF00";
    if (event.keyCode == 55) CURRENTCOLOR = "#FF0000";
    if (event.keyCode == 56) CURRENTCOLOR = "#4C0000";    

    // Keybinds
    if (!CTRLDOWN) return;

    if (event.keyCode == 67) {

        // Clear the canvas
        context.clearRect(0, 0, canvas.width, canvas.height);
    } else if (event.keyCode == 83) {

        // Save the canvas as an image
        event.preventDefault();

    }

};
document.onkeyup = function(event) {

    event = event || window.event;

    // Check if control key was let go
    if (event.keyCode == 17 || event.keyCode == 91) CTRLDOWN = false;

}
