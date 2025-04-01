// Exibe os sintomas da parte do corpo com base no botão clicaco
function mostrarSintomas(parteCorpoId) {
    // Fecha qualquer modal que já esteja aberto
    const modals = document.querySelectorAll('.sintomas')
    modals.forEach(modal => modal.classList.remove('show'))

    // Localiza o modal e o botão correspondente à parte do corpo
    const modal = document.getElementById(parteCorpoId)
    const buttonElement = document.querySelector(`.parteCorpo[onclick*="${parteCorpoId}"]`)

    if (!modal || !buttonElement) {
        console.error("Elemento não encontrado para: ", parteCorpoId)
        return
    }

    // Obtém a posição e o tamanho do botão clicado
    const rect = buttonElement.getBoundingClientRect()
    modal.style.top = `${rect.top + window.scrollY}px`
    modal.style.left = `${rect.left + window.scrollX}px`;
    modal.style.width = `${rect.width}px`;
    modal.style.height = `${rect.height}px`;

    //Exibe o modal com a transição do CSS
    modal.classList.add('show')

    // Trava rolagem da grid
    const grid = document.querySelector('.grid')
    if (grid) {
        grid.style.overflow = 'hidden'
    }
}

// Fecha os modais de sintomas
function fecharSintomas() {
    const modals = document.querySelectorAll('.sintomas')
    modals.forEach(modal => modal.classList.remove('show'))

    // Libera a rolagem da grid
    const grid = document.querySelector('.grid')
    if (grid) {
        grid.style.overflow = 'auto'
    }
}