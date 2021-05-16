$(document).ready(function () {

    $("#d-up").click(function(){
        $.get("/forward", function () {
            console.log("Car Forward.");
        });
    });

    $("#d-left").click(function(){
        $.get("/left", function () {
            console.log("Car Turned Left.");
        });
    });

    $("#d-right").click(function(){
        $.get("/right", function () {
            console.log("Car Turned Right.");
        });
    });

    $("#d-stop").click(function(){
        $.get("/stop", function () {
            console.log("Car Stopped.");
        });
    });

    $("#d-back").click(function(){
        $.get("/back", function () {
            console.log("Car Backwards.");
        });
    });

    $("#d-clockwise").click(function(){
        $.get("/clockwise", function () {
            console.log("Car Clockwise.");
        });
    });

    $("#d-anti-clockwise").click(function(){
        $.get("/anti-clockwise", function () {
            console.log("Car Anti-Clockwise.");
        });
    });
});