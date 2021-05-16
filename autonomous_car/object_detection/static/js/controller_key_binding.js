$(document).ready(function() {

    function forward() {
        console.log('forward');
        window.location.href = "/forward";
    }

    function backward() {
        console.log('backward');
        window.location.href = "/back";
    }

    function turnLeft() {
        console.log('turn left');
        window.location.href = "/left";
    }

    function turnRight() {
        console.log('turn right');
        window.location.href = "/right";
    }

    function stop() {
        console.log('stop');
        window.location.href = "/stop";
    }

    function clockwise() {
        console.log('clockwise');
        window.location.href = "/clockwise";
    }

    function anti_clockwise() {
        console.log('anti-clockwise');
        window.location.href = "/anti-clockwise";
    }

    Mousetrap.bind({
        'space': stop,
        'w': forward,
        's': backward,
        'a': turnLeft,
        'd': turnRight,
        'q': clockwise,
        'e': anti_clockwise,
    });
});