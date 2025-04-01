// static/js/script.js

/**
 * Función de inicialización que se ejecuta cuando el DOM está listo
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Documento cargado - JS funcionando correctamente');
    
    // 1. Manejo de alertas de Django (messages)
    initDjangoAlerts();
    
    // 2. Eventos globales
    setupGlobalEvents();
    
    // 3. Inicializar componentes comunes
    initComponents();
});

/**
 * Maneja las alertas/mensajes de Django
 */
function initDjangoAlerts() {
    const alerts = document.querySelectorAll('.alert-dismissible');
    
    alerts.forEach(alert => {
        // Cierra automáticamente las alertas después de 5 segundos
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
        
        // También se puede cerrar manualmente (ya implementado en tu HTML)
    });
}

/**
 * Configura eventos globales
 */
function setupGlobalEvents() {
    // Ejemplo: Confirmación antes de acciones importantes
    document.querySelectorAll('[data-confirm]').forEach(element => {
        element.addEventListener('click', (e) => {
            if (!confirm(element.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });
}

/**
 * Inicializa componentes comunes
 */
function initComponents() {
    // Ejemplo: Tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Ejemplo: Validación de formularios
    document.querySelectorAll('.needs-validation').forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Función para hacer peticiones AJAX genéricas
 */
function makeAjaxRequest(url, method = 'GET', data = null) {
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: data ? JSON.stringify(data) : null
    })
    .then(response => response.json())
    .catch(error => console.error('Error:', error));
}

// Exporta funciones para usarlas en otros archivos (si usas módulos)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initDjangoAlerts,
        setupGlobalEvents,
        initComponents,
        makeAjaxRequest
    };
}