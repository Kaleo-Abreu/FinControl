document.addEventListener("DOMContentLoaded", function () {
    const tipo = document.getElementById("tipo");
    const campoId = document.getElementById("campo-id");
    const campoAtivo = document.getElementById("campo-ativo");
    const campoData = document.getElementById("campo-data");
    const campoDataFim = document.getElementById("campo-data-fim");

    function atualizarCampos() {
        campoId.classList.toggle("d-none", tipo.value !== "id");
        campoAtivo.classList.toggle("d-none", tipo.value !== "ativo");
        campoData.classList.toggle("d-none", tipo.value !== "data");
        campoDataFim.classList.toggle("d-none", tipo.value !== "data");
    }

    tipo.addEventListener("change", atualizarCampos);

    atualizarCampos();
});
