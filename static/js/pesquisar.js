const seletor = document.getElementById("tipo");
const campoId = document.getElementById("campo-id");
const campoAtivo = document.getElementById("campo-ativo");
const campoData = document.getElementById("campo-data");

function atualizarCampos() {
    campoId.classList.toggle("d-none", seletor.value !== "id");
    campoAtivo.classList.toggle("d-none", seletor.value !== "ativo");
    campoData.classList.toggle("d-none", seletor.value !== "data");
}

seletor.addEventListener("change", atualizarCampos);

atualizarCampos();
