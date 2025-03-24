// mostra sintomas da parte do corpo selecionada
function mostrarSintomas(parteCorpo) {
    // removendo sintomas abertos antes de exibir outros sintomas
    const sintomas = document.querySelectorAll('.sintomas')
    sintomas.forEach(s => s.classList.remove('show'))

    // obter a div .parteCorpo que foi clicada
    const divParteCorpo = document.querySelector(`.parteCorpo[onclick*="${parteCorpo}"]`)
    const divSintomas = document.getElementById(parteCorpo)

    // pegar a posição da div .parteCorpo
    const rect = divParteCorpo.getBoundingClientRect()

    // definir a posição da div .sintomas no lugar da div .parteCorpo
    divSintomas.style.top = `${rect.top + window.scrollY}px`
    divSintomas.style.left = `${rect.left + window.scrollX}px`
    divSintomas.style.width = `${rect.width}px`
    divSintomas.style.height = `${rect.height}px`

    // mostrar sintomas
    divSintomas.classList.add('show')

    // travar rolagem do eixo Y
    const grid = document.querySelector('.grid')
    grid.style.overflow = 'hidden'
}

// fecha sintomas com botão "voltar"
function fecharSintomas() {
    let sintomas = document.querySelectorAll('.sintomas')
    sintomas.forEach(s => s.classList.remove('show'))

    // libera a rolagem do eixo Y
    const grid = document.querySelector('.grid')
    grid.style.overflow = 'auto' // Restaura o scroll padrão
}