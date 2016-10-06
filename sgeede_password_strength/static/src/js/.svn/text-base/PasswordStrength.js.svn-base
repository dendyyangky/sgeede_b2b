
function CheckPasswordStrength(new_password,varpassword_strength) { 
    $(".button.oe_button.oe_form_button").remove();
    var password_strength = document.getElementById("password_strength");
    if (new_password.length == 0) {
        new_password = "";
        return;
    }
    var regex = new Array();
    regex.push("[A-Z]"); 
    regex.push("[a-z]");
    regex.push("[0-9]");
    regex.push("[$@$!%*#?& `]"); 
    var passed = 0;

    for (var i = 0; i < regex.length; i++) {
        if (new RegExp(regex[i]).test(new_password)) {
            passed++;
        }
    }
    if (passed > 2 && new_password.length > 8) {
        passed++;
    }
     var color = "";
     var strength = "";
    switch (passed) {
        case 0:
        case 1:
            strength = "<div id=weak>Weak</div>";
            password_strength_meter =  1; 
            break;
        case 2:
            strength = "<div id=good>Good</div>";
            password_strength_meter=  2; 
            break;
        case 3:
            strength = "<div id=very-good>Very Good</div>";
            password_strength_meter=  3; 
            break;
        case 4:
            strength = "<div id=strong>Strong</div>";
            password_strength_meter=  4; 
            break;
        case 5:
            strength = "<div id=very-strong>Very Strong</div>";
            password_strength_meter=  5; 
            break;
    }
    password_strength = strength;
    $("input[name='varpassword_strength']").attr("value", password_strength_meter);
    $(".password_strength").html(password_strength);
   
}

     
           
       

