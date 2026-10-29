
const menuToggle = document.getElementById('menuToggle');
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('sidebarOverlay');

function fecharMenu() {
    if (!sidebar || !overlay || !menuToggle) {
        return;
    }

    sidebar.classList.remove('sidebar-open');
    overlay.classList.remove('overlay-visible');
    menuToggle.setAttribute('aria-expanded', 'false');
}

if (menuToggle && sidebar && overlay) {
    menuToggle.addEventListener('click', function () {
        const aberto = sidebar.classList.toggle('sidebar-open');

        overlay.classList.toggle('overlay-visible', aberto);
        menuToggle.setAttribute('aria-expanded', String(aberto));
    });

    overlay.addEventListener('click', fecharMenu);

    document.querySelectorAll('.sidebar-nav .nav-link').forEach(link => {
        link.addEventListener('click', fecharMenu);
    });
}

const currentDate = document.getElementById('currentDate');

if (currentDate) {
    currentDate.textContent = new Intl.DateTimeFormat('pt-BR', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    }).format(new Date());
}
