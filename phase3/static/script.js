let mensagens = document.getElementById('mensagens');
let input = document.getElementById('input-palpite');
let btn = document.getElementById('btn-enviar');

// Estabelecer conexão WebSocket com o servidor
// Note que o servidor está rodando em ws://localhost:8001
let socket = new WebSocket("ws://localhost:8001");

socket.onmessage = (event) => {
  // Recebe mensagens do servidor e as exibe
  mensagens.textContent += event.data + "\n";
};

btn.addEventListener('click', () => {
  let palpite = input.value;
  if (palpite.trim() !== "") {
    socket.send(palpite);
    input.value = "";
  }
});
