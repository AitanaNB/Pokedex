//Función para recoger el nickname que se le quiere dar a un Pokémon al capturarlo
document.querySelectorAll('.btn-capture-small').forEach(btn => {
    btn.addEventListener('click', () => {
        const slot = btn.dataset.slot;
        const equipoId = btn.dataset.equipo;
        const url = btn.dataset.url;
        const nickname = prompt("Escribe el nombre del Pokémon:");
        if (!nickname) return;

        const form = document.createElement("form");
        form.method = "POST";
        form.action = url;  // URL ya correcta con Flask

        const inputEquipo = document.createElement("input");
        inputEquipo.type = "hidden";
        inputEquipo.name = "idEquipo";
        inputEquipo.value = equipoId;
        form.appendChild(inputEquipo);

        const inputSlot = document.createElement("input");
        inputSlot.type = "hidden";
        inputSlot.name = "slot";
        inputSlot.value = slot;
        form.appendChild(inputSlot);

        const inputNickname = document.createElement("input");
        inputNickname.type = "hidden";
        inputNickname.name = "nickname";
        inputNickname.value = nickname;
        form.appendChild(inputNickname);

        document.body.appendChild(form);
        form.submit();
    });
});

