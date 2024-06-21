function sendText(e){
    e.preventDefault()
    // console.log(e)
    const formData = new FormData(e.target)
    let summary = formData.get("summary");
    // return false
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        
            document.getElementById("feedback").innerText = ""
            document.getElementById("prediction").innerHTML = `
                <h2 style="margin: 20px 0;">Our Prediction:</h2>
                <p id="rating">${this.responseText}</p>`;
            }
    };

    console.log(summary)
    if (summary.length > 0){
        xhttp.open("POST", "/sendSummary") 
        xhttp.send(formData);
    } else {
        document.getElementById("prediction").innerHTML = ""
        document.getElementById("feedback").innerText = "Finish filling out the summary before submitting!"
    }
    // summary?.length > 0 && 
//    alert("My First Test");
};