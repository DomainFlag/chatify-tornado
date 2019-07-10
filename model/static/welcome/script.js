const timeout = 900;
const tokens = [
    "hurdle",
    "problem",
    "wait",
    "heavy"
];

let contentSwappable = document.querySelector(".content-swappable");
if(contentSwappable != null) {
    let identifier = setInterval((() => {
        let index = 0;

        return () => {
            if (index >= tokens.length - 1) {
                clearInterval(identifier);
            }

            contentSwappable.innerHTML = tokens[index];

            index++;
        }
    })(), timeout);
}