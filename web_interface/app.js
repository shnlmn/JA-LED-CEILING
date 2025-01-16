const ws = new WebSocket("ws://" + window.location.hostname + ":5555");

ws.onopen = () => {
  console.log("WebSocket connected");
};

document.getElementById("animationSelect")
  .addEventListener("change", (e) => {
    ws.send(`animation:${e.target.value}`);
  });

document.getElementById("magInput")
  .addEventListener("input", (e) => {
    ws.send(`mag:${e.target.value}`);
  });

