function submit() 
{
    var otp = document.getElementById("otp").value;
    var apigClient = apigClientFactory.newClient();
    var msg = "OTP not found, Access Denied";
	let params = {};
	var body = {
        "otp" : otp
    };
    console.log(body);
    apigClient.rootPost(params,body)
	.then(function(result){
        msg = result['data']['body'];
        console.log(msg);
        document.getElementById("response").innerHTML = '<h4 style="color:green">' + msg + '</h4>';
	}).catch(function(result) {
        console.log("ERROR: " + result);
        document.getElementById("response").innerHTML = msg;
    });
}