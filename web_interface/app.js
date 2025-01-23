console.log(window.location.hostname)
const ws = new WebSocket("ws://" + window.location.hostname + ":5555");

ws.onopen = () => {
  console.log("WebSocket connected");
  ws.send("request_ui_schema:1")
};

document.getElementById("animationSelect")
.addEventListener("change", (e) => {
    ws.send(`animation:${e.target.value}`);
    console.log("Sent animation ", e.target.value);
  });

ws.onmessage = (event) => {
  console.log("Raw event data: ", event.data);
  let data;
  try{
    data = JSON.parse(event.data);
    console.log("Received Data: ", data)
    if (data.ui_schema && data.current_values) {
      buildDynamicControls(data.ui_schema, data.current_values);
    }
  } catch (e) {
    console.log("Received non-JSON or other message:", event.data, e);
  }
};

function buildDynamicControls(schema, currentValues){
  const container = document.getElementById("controls");
  container.innerHTML = "";

  Object.entries(schema).forEach(([key, config]) => {
    const value = currentValues[key] ?? 0;
    const label = document.createElement("label");

    let input;
    input = document.createElement("input");
    input.type = config.type || "text";
    if (config.min !== undefined) input.min = config.min;
    if (config.max !== undefined) input.max = config.max;
    if (config.step !== undefined) input.step = config.step;

    input.value = value;

    label.textContent = `${config.label || key}: ${input.value}`;

    input.addEventListener("input", () => {
      label.textContent = `${config.label || key}: ${input.value}`;
      ws.send(`${key}:${input.value}`);
    });

    container.appendChild(label);
    container.appendChild(input);
    container.appendChild(document.createElement("br"));
  })
}
