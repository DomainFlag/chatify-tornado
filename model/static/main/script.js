let form = document.querySelector("#form-input");
let content = document.querySelector(".form-input-content");

document.addEventListener("keypress", (event) => {
    let key = event.which || event.keyCode;

    if(key === 13) {
        if(content.value.length > 0) {
            form.submit();
        }
    }
});

class Application {

    constructor() {
        // create WebSocket connection.
        this.socket = new WebSocket('ws://localhost:8000/socket');

        this.open();
        this.listen();
    }

    open() {
        console.log("Trying to connect");

        this.socket.addEventListener("open", event => {
            this.socket.send("Hello Server!");

            setTimeout(() => {
                this.socket.send("Once again it's me");
            }, 10000);
        });
    }

    listen() {
        this.socket.addEventListener('message', function (event) {
            console.log('Message from server ', event.data);
        });
    }
}

let application = new Application();