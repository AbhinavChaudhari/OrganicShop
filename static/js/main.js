$(document).ready(function(){

    $("#qty").keyup(function(){
        total = parseInt($("#vandor_price").val()) + parseInt($("#qty").val());
        $("#total").val(total);
    });
     
 });