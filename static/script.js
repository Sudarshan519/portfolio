
// now = Math.floor(Date.now() / 1000)
// var ws = new WebSocket("ws://127.0.0.1:8000/ws/" + "${now}");
// //const ws = new WebSocket("ws://" + window.location.host + "/ws/1");

// ws.onmessage = function (event) {
//     console.log(event.data)
//     const data = JSON.parse(event.data);
//     const message = data.server;
//     const notificationContainer = document.getElementById("notification-container");
//     const notificationItem = document.createElement("div");
//     notificationItem.innerText = message;
//     notificationContainer.appendChild(notificationItem);
// };


now = Math.floor(Date.now() / 1000)
// console.log(window.location.host)
var url = "jobsserach.vercel.app";
//${window.location.host}
// var ws = new WebSocket(`ws://${url}/ws/` + 1);
// ws.onmessage = function (event) {
//     console.log(event)
//     //     ///     var messages = document.getElementById('messages')
//     //     ///     var message = document.createElement('li')
//     //     ///    var content = document.createTextNode(event.data)
//     //     ///     message.appendChild(content)
//     //     ///    messages.appendChild(message)
// };

//const ws = new WebSocket("ws://" + window.location.host + "/ws/notifications/");
//       ws.onmessage = function (event) {
//         console.log(event.data)
//   }
// Get the button that opens the modal
var btn = document.getElementById("myBtn");
var loader = document.getElementById("loaderlast")
// Get the <span> element that closes the modal
//        <!-- var span = document.getElementsByClassName("close")[0]; -->
span = document.getElementById("closeId")
// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none"; loader.style.display = "none"
}
let slideIndex = 1;
let running = false;
showSlides(slideIndex);
document.getElementById("myAnchor").addEventListener("click", function (event) {

    //   console.log('clicked');

    submitContact();//
    event.preventDefault()
});


// Next/previous controls
function plusSlides(n) {
    running = true
    //  console.log(n)
    showSlides(slideIndex += n);
    //  running = false
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides() {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    if (slideIndex > slides.length || slideIndex <= 1) { slideIndex = 1 }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
    if (running == false)
        setTimeout(() => {
            // console.log(slideIndex)
            showSlides(), slideIndex++
        }, 10000); // Change image every 2 seconds
}

// Get the modal
var modal = document.getElementById("myModal");
async function submitContact() {
    var emailInput = document.getElementById("emailId")
    var nameInput = document.getElementById("nameId")
    var messageInput = document.getElementById("messageId")
    var posturl = window.location.host;

    console.log(nameInput.value)
    console.log(messageInput.value)
    fetch("/contactsubmit",
        {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify({ "name": nameInput.value, "email": emailInput.value, "message": messageInput.value })
        })
        .then(function (res) {
            console.log(res)
            emailInput.value = ''
            nameInput.value = ''
            messageInput.value = ''
            //   ptage = document.getElementById("messageTag")
            // ptage.text = "Sucessfully uploaded.We will get back to you soon."
            modal.style.display = "block";


            // modal = "Sucessfully uploaded.We will get back to you soon."
        })
        .catch(function (res) {
            console.log(res)

        })
}

// When the user clicks on the button, open the modal
btn.onclick = function () {

    modal.style.display = "block";
}



// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";

    }
}

// Handle page refresh or tab close
// window.addEventListener('beforeunload', function () {
//     // Close the WebSocket connection before the page is unloaded
//     if (socket) {
//         socket.close();
//     }
// })