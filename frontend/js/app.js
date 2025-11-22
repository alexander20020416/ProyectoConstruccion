/**
 * SISTEMA DE TRANSCRIPCIÓN BRAILLE - JavaScript Principal
 * ========================================================
 * Maneja la interacción del usuario y las llamadas a la API
 * 
 * Autor: GR4
 * Fecha: Noviembre 2025
 */

// === CONFIGURACIÓN ===
const API_BASE_URL = window.location.origin + '/api';

// === ESTADO GLOBAL ===
let currentMode = 'text-to-braille';
let currentSignageType = 'elevator';

// === INICIALIZACIÓN ===
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Sistema Braille inicializado');
    initTabs();
    initConverter();
    initSignage();
    initReference();
    initHistory();
});

// === GESTIÓN DE TABS ===
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.dataset.tab;
            
            // Desactivar todos los tabs
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Activar tab seleccionado
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
            
            // Cargar historial si es necesario
            if (targetTab === 'history') {
                loadHistory();
            }
        });
    });
}

// === CONVERSOR ===
function initConverter() {
    // Mode toggle
    const btnTextToBraille = document.getElementById('mode-text-to-braille');
    const btnBrailleToText = document.getElementById('mode-braille-to-text');
    const textPanel = document.getElementById('text-to-braille-panel');
    const braillePanel = document.getElementById('braille-to-text-panel');
    
    btnTextToBraille.addEventListener('click', () => {
        currentMode = 'text-to-braille';
        btnTextToBraille.classList.add('active');
        btnBrailleToText.classList.remove('active');
        textPanel.style.display = 'block';
        braillePanel.style.display = 'none';
    });
    
    btnBrailleToText.addEventListener('click', () => {
        currentMode = 'braille-to-text';
        btnBrailleToText.classList.add('active');
        btnTextToBraille.classList.remove('active');
        braillePanel.style.display = 'block';
        textPanel.style.display = 'none';
    });
    
    // Contador de caracteres
    const inputText = document.getElementById('input-text');
    const charCount = document.getElementById('char-count');
    
    inputText.addEventListener('input', () => {
        charCount.textContent = inputText.value.length;
    });
    
    // Botones de conversión
    document.getElementById('btn-convert-to-braille').addEventListener('click', convertToBraille);
    document.getElementById('btn-convert-to-text').addEventListener('click', convertToText);
    document.getElementById('btn-clear-text').addEventListener('click', clearTextPanel);
    document.getElementById('btn-clear-braille').addEventListener('click', clearBraillePanel);
}

async function convertToBraille() {
    const inputText = document.getElementById('input-text').value.trim();
    const outputBraille = document.getElementById('output-braille');
    
    if (!inputText) {
        showNotification('Por favor ingresa un texto', 'warning');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/convert/to-braille`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: inputText,
                format: 'unicode'
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            outputBraille.textContent = data.braille;
            outputBraille.style.color = 'var(--braille-color)';
            showNotification('✓ Conversión exitosa', 'success');
        } else {
            throw new Error(data.error || 'Error en la conversión');
        }
    } catch (error) {
        console.error('Error:', error);
        outputBraille.textContent = 'Error: ' + error.message;
        outputBraille.style.color = 'var(--error-color)';
        showNotification('Error en la conversión', 'error');
    } finally {
        showLoading(false);
    }
}

async function convertToText() {
    const inputBraille = document.getElementById('input-braille').value.trim();
    const outputText = document.getElementById('output-text');
    
    if (!inputBraille) {
        showNotification('Por favor ingresa texto en Braille', 'warning');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/convert/to-text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                braille: inputBraille
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            outputText.textContent = data.text;
            outputText.style.color = 'var(--text-primary)';
            showNotification('✓ Conversión exitosa', 'success');
        } else {
            throw new Error(data.error || 'Error en la conversión');
        }
    } catch (error) {
        console.error('Error:', error);
        outputText.textContent = 'Error: ' + error.message;
        outputText.style.color = 'var(--error-color)';
        showNotification('Error en la conversión', 'error');
    } finally {
        showLoading(false);
    }
}

function clearTextPanel() {
    document.getElementById('input-text').value = '';
    document.getElementById('output-braille').textContent = 'El resultado aparecerá aquí...';
    document.getElementById('char-count').textContent = '0';
}

function clearBraillePanel() {
    document.getElementById('input-braille').value = '';
    document.getElementById('output-text').textContent = 'El resultado aparecerá aquí...';
}

// === SEÑALÉTICA ===
function initSignage() {
    const signageType = document.getElementById('signage-type');
    const elevatorForm = document.getElementById('elevator-form');
    const doorForm = document.getElementById('door-form');
    const labelForm = document.getElementById('label-form');
    
    signageType.addEventListener('change', (e) => {
        currentSignageType = e.target.value;
        
        // Ocultar todos los formularios
        elevatorForm.style.display = 'none';
        doorForm.style.display = 'none';
        labelForm.style.display = 'none';
        
        // Mostrar formulario seleccionado
        if (currentSignageType === 'elevator') {
            elevatorForm.style.display = 'block';
        } else if (currentSignageType === 'door') {
            doorForm.style.display = 'block';
        } else if (currentSignageType === 'label') {
            labelForm.style.display = 'block';
        }
    });
    
    // Botón agregar piso
    document.getElementById('btn-add-floor').addEventListener('click', addFloor);
    
    // Listener para eliminar pisos (delegación de eventos)
    document.getElementById('floor-list').addEventListener('click', (e) => {
        if (e.target.classList.contains('btn-remove')) {
            e.target.closest('.floor-item').remove();
        }
    });
    
    // Botón generar PDF
    document.getElementById('btn-generate-pdf').addEventListener('click', generatePDF);
}

function addFloor() {
    const floorList = document.getElementById('floor-list');
    const floorItem = document.createElement('div');
    floorItem.className = 'floor-item';
    floorItem.innerHTML = `
        <input type="text" placeholder="Nombre del piso" class="input floor-text">
        <input type="text" placeholder="Número" class="input floor-number">
        <button class="btn btn-small btn-remove">✕</button>
    `;
    floorList.appendChild(floorItem);
}

async function generatePDF() {
    const pdfStatus = document.getElementById('pdf-status');
    pdfStatus.textContent = '';
    pdfStatus.classList.remove('show');
    
    let items = [];
    let title = '';
    
    try {
        if (currentSignageType === 'elevator') {
            title = document.getElementById('elevator-title').value || 'ASCENSOR';
            const floorItems = document.querySelectorAll('.floor-item');
            
            if (floorItems.length === 0) {
                throw new Error('Agrega al menos un piso');
            }
            
            floorItems.forEach(item => {
                const text = item.querySelector('.floor-text').value;
                const number = item.querySelector('.floor-number').value;
                if (text && number) {
                    items.push({ text, number });
                }
            });
            
        } else if (currentSignageType === 'door') {
            const doorName = document.getElementById('door-name').value;
            const doorNumber = document.getElementById('door-number').value;
            
            if (!doorName) {
                throw new Error('Ingresa el nombre de la puerta');
            }
            
            title = doorName;
            items = [{ text: doorName, number: doorNumber }];
            
        } else if (currentSignageType === 'label') {
            const labelText = document.getElementById('label-text').value;
            const labelSubtitle = document.getElementById('label-subtitle').value;
            
            if (!labelText) {
                throw new Error('Ingresa el texto de la etiqueta');
            }
            
            title = labelText;
            items = [{ text: labelText, subtitle: labelSubtitle }];
        }
        
        if (items.length === 0) {
            throw new Error('No hay elementos para generar el PDF');
        }
        
        showLoading(true);
        
        const response = await fetch(`${API_BASE_URL}/generate-signage`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: title,
                items: items,
                format: currentSignageType
            })
        });
        
        if (response.ok) {
            // Descargar PDF
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `senaletica_braille_${Date.now()}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showNotification('✓ PDF generado exitosamente', 'success');
            pdfStatus.textContent = '✓ PDF descargado correctamente';
            pdfStatus.className = 'status-message success show';
        } else {
            const error = await response.json();
            throw new Error(error.error || 'Error al generar PDF');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showNotification(error.message, 'error');
        pdfStatus.textContent = '✕ Error: ' + error.message;
        pdfStatus.className = 'status-message error show';
    } finally {
        showLoading(false);
    }
}

// === REFERENCIA ===
function initReference() {
    generateAlphabetTable();
    generateNumbersTable();
    generateAccentedTable();
}

async function generateAlphabetTable() {
    const table = document.getElementById('alphabet-table');
    const alphabet = 'abcdefghijklmnopqrstuvwxyz';
    
    for (let char of alphabet) {
        try {
            const response = await fetch(`${API_BASE_URL}/braille/info/${char}`);
            const data = await response.json();
            
            if (data.success) {
                const item = document.createElement('div');
                item.className = 'braille-item';
                item.innerHTML = `
                    <span class="braille-char">${data.unicode}</span>
                    <span class="char-label">${char}</span>
                `;
                table.appendChild(item);
            }
        } catch (error) {
            console.error(`Error al obtener info de ${char}:`, error);
        }
    }
}

async function generateNumbersTable() {
    const table = document.getElementById('numbers-table');
    const numbers = '0123456789';
    
    // Generar números mediante conversión
    for (let num of numbers) {
        try {
            const response = await fetch(`${API_BASE_URL}/convert/to-braille`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: num, format: 'unicode' })
            });
            const data = await response.json();
            
            if (data.success) {
                const item = document.createElement('div');
                item.className = 'braille-item';
                item.innerHTML = `
                    <span class="braille-char">${data.braille}</span>
                    <span class="char-label">${num}</span>
                `;
                table.appendChild(item);
            }
        } catch (error) {
            console.error(`Error al obtener ${num}:`, error);
        }
    }
}

async function generateAccentedTable() {
    const table = document.getElementById('accented-table');
    const accented = ['á', 'é', 'í', 'ó', 'ú', 'ñ', 'ü'];
    
    for (let char of accented) {
        try {
            const response = await fetch(`${API_BASE_URL}/braille/info/${char}`);
            const data = await response.json();
            
            if (data.success) {
                const item = document.createElement('div');
                item.className = 'braille-item';
                item.innerHTML = `
                    <span class="braille-char">${data.unicode}</span>
                    <span class="char-label">${char}</span>
                `;
                table.appendChild(item);
            }
        } catch (error) {
            console.error(`Error al obtener ${char}:`, error);
        }
    }
}

// === HISTORIAL ===
function initHistory() {
    document.getElementById('btn-refresh-history').addEventListener('click', loadHistory);
    document.getElementById('history-filter').addEventListener('change', loadHistory);
}

async function loadHistory() {
    const historyList = document.getElementById('history-list');
    const filter = document.getElementById('history-filter').value;
    
    historyList.innerHTML = '<p class="loading">Cargando historial...</p>';
    
    try {
        let url = `${API_BASE_URL}/history?limit=50`;
        if (filter) {
            url += `&type=${filter}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success && data.history.length > 0) {
            historyList.innerHTML = '';
            
            data.history.forEach(item => {
                const historyItem = document.createElement('div');
                historyItem.className = 'history-item';
                
                const typeClass = item.conversion_type === 'text_to_braille' 
                    ? 'type-to-braille' 
                    : 'type-to-text';
                
                const typeLabel = item.conversion_type === 'text_to_braille'
                    ? 'Español → Braille'
                    : 'Braille → Español';
                
                const date = new Date(item.timestamp).toLocaleString('es-ES');
                
                historyItem.innerHTML = `
                    <div class="history-header">
                        <span class="history-type ${typeClass}">${typeLabel}</span>
                        <span class="history-timestamp">${date}</span>
                    </div>
                    <div class="history-content">
                        <div class="history-original">${escapeHtml(item.original_text)}</div>
                        <div class="history-braille">${item.braille_text}</div>
                    </div>
                `;
                
                historyList.appendChild(historyItem);
            });
        } else {
            historyList.innerHTML = '<p class="loading">No hay conversiones en el historial</p>';
        }
    } catch (error) {
        console.error('Error al cargar historial:', error);
        historyList.innerHTML = '<p class="loading">Error al cargar el historial</p>';
    }
}

// === UTILIDADES ===
function showLoading(show) {
    const overlay = document.getElementById('loading-overlay');
    if (show) {
        overlay.classList.add('active');
    } else {
        overlay.classList.remove('active');
    }
}

function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    const messageEl = document.getElementById('notification-message');
    
    messageEl.textContent = message;
    notification.className = `notification ${type} show`;
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 4000);
}

document.getElementById('notification-close').addEventListener('click', () => {
    document.getElementById('notification').classList.remove('show');
});

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// === LOG DE ESTADO ===
console.log(`
╔════════════════════════════════════════╗
║   SISTEMA DE TRANSCRIPCIÓN BRAILLE    ║
║           Versión 1.0.0                ║
╚════════════════════════════════════════╝

✓ API Base URL: ${API_BASE_URL}
✓ Tabs inicializados
✓ Conversor listo
✓ Generador de señalética listo
✓ Tablas de referencia cargando...
✓ Sistema completamente funcional
`);
