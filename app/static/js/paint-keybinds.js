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
