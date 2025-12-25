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
    
    // Braille Builder
    initBrailleBuilder();
}

// === BRAILLE BUILDER ===
let builderSequence = []; // Array de objetos {dots: [1,2,3], unicode: '⠇'}
let selectedCellIndex = -1; // Índice de la celda seleccionada (-1 = ninguna)
let insertMode = false; // Si estamos en modo insertar

function initBrailleBuilder() {
    const dotBuilders = document.querySelectorAll('.dot-builder');
    let currentDots = [];
    
    // Click en puntos para activar/desactivar
    dotBuilders.forEach(dot => {
        dot.addEventListener('click', () => {
            const dotNum = parseInt(dot.dataset.dot);
            
            if (currentDots.includes(dotNum)) {
                // Desactivar
                currentDots = currentDots.filter(d => d !== dotNum);
                dot.classList.remove('active');
            } else {
                // Activar
                currentDots.push(dotNum);
                dot.classList.add('active');
            }
        });
    });
    
    // Agregar carácter a la secuencia
    document.getElementById('btn-add-char').addEventListener('click', () => {
        // Convertir puntos actuales a Unicode Braille
        const unicode = dotsToUnicode(currentDots);
        
        const newCell = {
            dots: [...currentDots],
            unicode: unicode
        };
        
        // Si estamos en modo insertar, insertar antes de la celda seleccionada
        if (insertMode && selectedCellIndex >= 0) {
            builderSequence.splice(selectedCellIndex, 0, newCell);
            insertMode = false;
            selectedCellIndex = -1;
            showNotification('Carácter insertado', 'success');
        } else {
            builderSequence.push(newCell);
        }
        
        updateSequenceDisplay();
        
        // Limpiar constructor
        currentDots = [];
        dotBuilders.forEach(dot => dot.classList.remove('active'));
    });
    
    // Agregar espacio
    document.getElementById('btn-add-space').addEventListener('click', () => {
        const newCell = {
            dots: [],
            unicode: '⠀'
        };
        
        if (insertMode && selectedCellIndex >= 0) {
            builderSequence.splice(selectedCellIndex, 0, newCell);
            insertMode = false;
            selectedCellIndex = -1;
            showNotification('Espacio insertado', 'success');
        } else {
            builderSequence.push(newCell);
        }
        updateSequenceDisplay();
    });
    
    // Limpiar celda actual
    document.getElementById('btn-reset-builder').addEventListener('click', () => {
        currentDots = [];
        dotBuilders.forEach(dot => dot.classList.remove('active'));
    });
    
    // Limpiar toda la secuencia
    document.getElementById('btn-clear-sequence').addEventListener('click', () => {
        builderSequence = [];
        selectedCellIndex = -1;
        insertMode = false;
        updateSequenceDisplay();
    });
    
    // Eliminar celda seleccionada
    document.getElementById('btn-delete-selected').addEventListener('click', () => {
        if (selectedCellIndex >= 0 && selectedCellIndex < builderSequence.length) {
            builderSequence.splice(selectedCellIndex, 1);
            selectedCellIndex = -1;
            insertMode = false;
            updateSequenceDisplay();
            showNotification('Celda eliminada', 'success');
        }
    });
    
    // Insertar antes de la celda seleccionada
    document.getElementById('btn-insert-before').addEventListener('click', () => {
        if (selectedCellIndex >= 0) {
            insertMode = true;
            showNotification('Modo insertar activado - Construye el carácter y presiona "Agregar"', 'info');
            updateSequenceDisplay();
        }
    });
    
    // === BOTONES RÁPIDOS ===
    
    // Agregar indicador de mayúscula (puntos 4,6)
    document.getElementById('btn-add-capital').addEventListener('click', () => {
        const newCell = {
            dots: [4, 6],
            unicode: '⠨'
        };
        
        if (insertMode && selectedCellIndex >= 0) {
            builderSequence.splice(selectedCellIndex, 0, newCell);
            insertMode = false;
            selectedCellIndex = -1;
            showNotification('Indicador de mayúscula insertado', 'success');
        } else {
            builderSequence.push(newCell);
            showNotification('Indicador de mayúscula agregado', 'success');
        }
        updateSequenceDisplay();
    });
    
    // Agregar indicador de número (puntos 3,4,5,6)
    document.getElementById('btn-add-number').addEventListener('click', () => {
        const newCell = {
            dots: [3, 4, 5, 6],
            unicode: '⠼'
        };
        
        if (insertMode && selectedCellIndex >= 0) {
            builderSequence.splice(selectedCellIndex, 0, newCell);
            insertMode = false;
            selectedCellIndex = -1;
            showNotification('Indicador de número insertado', 'success');
        } else {
            builderSequence.push(newCell);
            showNotification('Indicador de número agregado', 'success');
        }
        updateSequenceDisplay();
    });
    
    // Mostrar modal de signos de puntuación
    document.getElementById('btn-show-punctuation').addEventListener('click', () => {
        showPunctuationModal();
    });
    
    // Cerrar modal
    document.getElementById('btn-close-modal').addEventListener('click', () => {
        closePunctuationModal();
    });
    
    // Cerrar modal al hacer clic fuera
    document.getElementById('punctuation-modal').addEventListener('click', (e) => {
        if (e.target.id === 'punctuation-modal') {
            closePunctuationModal();
        }
    });
}

function dotsToUnicode(dots) {
    const BRAILLE_BASE = 0x2800;
    const dotOffsets = {
        1: 0x01, 2: 0x02, 3: 0x04, 4: 0x08,
        5: 0x10, 6: 0x20
    };
    
    let offset = 0;
    dots.forEach(dot => {
        offset |= dotOffsets[dot];
    });
    
    return String.fromCharCode(BRAILLE_BASE + offset);
}

function updateSequenceDisplay() {
    const display = document.getElementById('braille-sequence-display');
    const sequenceInfo = document.getElementById('sequence-info');
    const btnDelete = document.getElementById('btn-delete-selected');
    const btnInsert = document.getElementById('btn-insert-before');
    
    if (builderSequence.length === 0) {
        display.innerHTML = '<p style="color: var(--text-secondary);">(vacío - construye caracteres arriba)</p>';
        sequenceInfo.textContent = '';
        btnDelete.disabled = true;
        btnInsert.disabled = true;
        selectedCellIndex = -1;
        insertMode = false;
        return;
    }
    
    // Actualizar info de secuencia
    let infoText = `(${builderSequence.length} celdas)`;
    if (insertMode) {
        infoText += ' - MODO INSERTAR';
    }
    sequenceInfo.textContent = infoText;
    
    // Renderizar como celdas visuales seleccionables
    let html = '';
    builderSequence.forEach((item, index) => {
        const isSelected = index === selectedCellIndex;
        html += `<div class="braille-cell selectable ${isSelected ? 'selected' : ''}" data-index="${index}">`;
        html += `<span class="cell-index">${index + 1}</span>`;
        html += '<div class="braille-dots">';
        
        const brailleOrder = [1, 4, 2, 5, 3, 6];
        brailleOrder.forEach(dotNumber => {
            const isActive = item.dots.includes(dotNumber);
            html += `<div class="braille-dot ${isActive ? 'active' : ''}"></div>`;
        });
        
        html += '</div>';
        html += '</div>';
    });
    
    display.innerHTML = html;
    
    // Actualizar estado de botones
    btnDelete.disabled = selectedCellIndex < 0;
    btnInsert.disabled = selectedCellIndex < 0;
    
    // Agregar eventos de clic a las celdas
    display.querySelectorAll('.braille-cell.selectable').forEach(cell => {
        cell.addEventListener('click', () => {
            const index = parseInt(cell.dataset.index);
            
            // Toggle selección
            if (selectedCellIndex === index) {
                selectedCellIndex = -1;
                insertMode = false;
            } else {
                selectedCellIndex = index;
            }
            
            updateSequenceDisplay();
        });
    });
}

// === MODAL DE SIGNOS DE PUNTUACIÓN ===
const PUNCTUATION_SIGNS = [
    { char: '.', name: 'Punto', dots: [3] },
    { char: ',', name: 'Coma', dots: [2] },
    { char: ';', name: 'Punto y coma', dots: [2, 3] },
    { char: ':', name: 'Dos puntos', dots: [2, 5] },
    { char: '?', name: 'Interrogación (cierre)', dots: [2, 6] },
    { char: '¿', name: 'Interrogación (apertura)', dots: [2, 6] },
    { char: '!', name: 'Exclamación (cierre)', dots: [2, 3, 5] },
    { char: '¡', name: 'Exclamación (apertura)', dots: [2, 3, 5] },
    { char: '-', name: 'Guión', dots: [3, 6] },
    { char: '(', name: 'Paréntesis (abre)', dots: [1, 2, 6] },
    { char: ')', name: 'Paréntesis (cierra)', dots: [3, 4, 5] },
    { char: '"', name: 'Comillas', dots: [2, 3, 6] },
    { char: "'", name: 'Apóstrofo', dots: [3] },
    { char: '*', name: 'Asterisco', dots: [3, 5] },
    { char: '@', name: 'Arroba', dots: [4, 7] }
];

function showPunctuationModal() {
    const modal = document.getElementById('punctuation-modal');
    const grid = document.getElementById('punctuation-grid');
    
    // Generar contenido del grid
    let html = '';
    PUNCTUATION_SIGNS.forEach(sign => {
        html += `<div class="punctuation-item" data-dots="${sign.dots.join(',')}" data-char="${sign.char}">`;
        html += createBrailleCellRef(sign.dots);
        html += `<span class="sign-label">${sign.char}</span>`;
        html += `<span class="sign-name">${sign.name}</span>`;
        html += '</div>';
    });
    
    grid.innerHTML = html;
    
    // Agregar eventos de clic a cada signo
    grid.querySelectorAll('.punctuation-item').forEach(item => {
        item.addEventListener('click', () => {
            const dots = item.dataset.dots.split(',').map(d => parseInt(d));
            const char = item.dataset.char;
            
            const newCell = {
                dots: dots,
                unicode: dotsToUnicode(dots)
            };
            
            // Si estamos en modo insertar, insertar antes
            if (insertMode && selectedCellIndex >= 0) {
                builderSequence.splice(selectedCellIndex, 0, newCell);
                insertMode = false;
                selectedCellIndex = -1;
                showNotification(`Signo "${char}" insertado`, 'success');
            } else {
                builderSequence.push(newCell);
                showNotification(`Signo "${char}" agregado`, 'success');
            }
            
            updateSequenceDisplay();
            closePunctuationModal();
        });
    });
    
    modal.classList.add('active');
}

function closePunctuationModal() {
    document.getElementById('punctuation-modal').classList.remove('active');
}

// Crear celda Braille visual para el modal (usa clases -ref)
function createBrailleCellRef(activeDots) {
    const brailleOrder = [1, 4, 2, 5, 3, 6];
    let html = '<div class="braille-cell-ref"><div class="braille-dots-grid">';
    
    brailleOrder.forEach(dotNumber => {
        const isActive = activeDots.includes(dotNumber);
        html += `<div class="braille-dot-ref ${isActive ? 'active' : ''}"></div>`;
    });
    
    html += '</div></div>';
    return html;
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
            // Renderizar con cajas Braille
            outputBraille.innerHTML = renderBrailleCells(data.dots_info);
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

function renderBrailleCells(dotsInfo) {
    if (!dotsInfo || dotsInfo.length === 0) {
        return 'El resultado aparecerá aquí...';
    }
    
    let html = '<div class="braille-cells-container">';
    
    dotsInfo.forEach(item => {
        if (item.type === 'space') {
            html += '<div class="braille-space"></div>';
        } else {
            html += '<div class="braille-cell">';
            html += '<div class="braille-dots">';
            
            // Crear la cuadrícula de 6 puntos en el orden correcto del sistema Braille
            // Orden Braille:  1 4    Orden Grid: pos1 pos2
            //                 2 5                pos3 pos4
            //                 3 6                pos5 pos6
            const brailleOrder = [1, 4, 2, 5, 3, 6];
            
            brailleOrder.forEach(dotNumber => {
                const isActive = item.dots.includes(dotNumber);
                html += `<div class="braille-dot ${isActive ? 'active' : ''}"></div>`;
            });
            
            html += '</div>';
            html += `<div class="braille-label">${escapeHtml(item.char)}</div>`;
            html += '</div>';
        }
    });
    
    html += '</div>';
    return html;
}

async function convertToText() {
    const outputText = document.getElementById('output-text');
    
    // Construir string Unicode desde la secuencia
    if (builderSequence.length === 0) {
        showNotification('Por favor construye una secuencia Braille', 'warning');
        return;
    }
    
    const brailleString = builderSequence.map(item => item.unicode).join('');
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/convert/to-text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                braille: brailleString
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Verificar si la traducción es válida
            if (data.valid === false) {
                // Traducción inválida - mostrar mensaje de error
                let errorHtml = '<div class="translation-error">';
                errorHtml += '<strong>⚠️ Traducción inválida</strong><br>';
                
                if (data.errors && data.errors.length > 0) {
                    errorHtml += '<ul class="error-list">';
                    data.errors.forEach(err => {
                        errorHtml += `<li>${err}</li>`;
                    });
                    errorHtml += '</ul>';
                }
                
                if (data.text) {
                    errorHtml += `<p class="partial-result">Resultado parcial: "${data.text}"</p>`;
                }
                
                errorHtml += '</div>';
                
                outputText.innerHTML = errorHtml;
                outputText.style.color = 'var(--warning-color)';
                showNotification('La secuencia Braille contiene errores', 'warning');
            } else {
                // Traducción válida
                outputText.textContent = data.text;
                outputText.style.color = 'var(--text-primary)';
                showNotification('✓ Conversión exitosa', 'success');
            }
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

// === SEÑALÉTICA / PDF ===
function initSignage() {
    // Botón vista previa
    document.getElementById('btn-preview-pdf').addEventListener('click', previewBraille);
    
    // Botón generar PDF
    document.getElementById('btn-generate-pdf').addEventListener('click', generatePDF);
    
    // Botón limpiar
    document.getElementById('btn-clear-signage').addEventListener('click', () => {
        document.getElementById('signage-text').value = '';
        document.getElementById('pdf-preview').style.display = 'none';
        document.getElementById('pdf-preview-content').innerHTML = '';
    });
}

async function previewBraille() {
    const text = document.getElementById('signage-text').value.trim();
    const previewSection = document.getElementById('pdf-preview');
    const previewContent = document.getElementById('pdf-preview-content');
    
    if (!text) {
        showNotification('Por favor ingresa un texto', 'warning');
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch(`${API_BASE_URL}/convert/to-braille`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text, format: 'unicode' })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Mostrar vista previa con celdas visuales
            previewContent.innerHTML = renderBrailleCells(data.dots_info);
            previewSection.style.display = 'block';
            showNotification('Vista previa generada', 'success');
        } else {
            throw new Error(data.error || 'Error en la conversión');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

async function generatePDF() {
    const pdfStatus = document.getElementById('pdf-status');
    const text = document.getElementById('signage-text').value.trim();
    
    pdfStatus.textContent = '';
    pdfStatus.classList.remove('show');
    
    if (!text) {
        showNotification('Por favor ingresa un texto', 'warning');
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch(`${API_BASE_URL}/generate-pdf`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });
        
        if (response.ok) {
            // Descargar PDF
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `braille_${Date.now()}.pdf`;
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
    generatePunctuationTable();
}

// Función auxiliar para crear celda Braille visual con 6 puntos
function createBrailleCell(dots, label) {
    // dots es un array de números [1,2,3,4,5,6] indicando qué puntos están activos
    const activeDots = new Set(dots);
    
    // Orden de los puntos en la cuadrícula: 1,4,2,5,3,6 (columna izq, columna der)
    const dotOrder = [1, 4, 2, 5, 3, 6];
    
    let dotsHTML = '';
    for (let dot of dotOrder) {
        const isActive = activeDots.has(dot);
        dotsHTML += `<div class="braille-dot-ref ${isActive ? 'active' : ''}"></div>`;
    }
    
    const item = document.createElement('div');
    item.className = 'braille-item-visual';
    item.innerHTML = `
        <div class="braille-cell-ref">
            ${dotsHTML}
        </div>
        <span class="char-label">${label}</span>
    `;
    return item;
}

async function generateAlphabetTable() {
    const table = document.getElementById('alphabet-table');
    const alphabet = 'abcdefghijklmnopqrstuvwxyz';
    
    for (let char of alphabet) {
        try {
            const response = await fetch(`${API_BASE_URL}/braille/info/${char}`);
            const data = await response.json();
            
            if (data.success) {
                const item = createBrailleCell(data.dots, char);
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
    
    // Generar números usando braille/info para obtener solo el símbolo del número (sin indicador)
    for (let num of numbers) {
        try {
            const response = await fetch(`${API_BASE_URL}/braille/info/${num}`);
            const data = await response.json();
            
            if (data.success) {
                const item = createBrailleCell(data.dots, num);
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
                const item = createBrailleCell(data.dots, char);
                table.appendChild(item);
            }
        } catch (error) {
            console.error(`Error al obtener ${char}:`, error);
        }
    }
}

async function generatePunctuationTable() {
    const table = document.getElementById('punctuation-table');
    
    // Agregar el punto manualmente primero (tiene problemas con la URL)
    // Punto = puntos [3]
    const dotItem = createBrailleCell([3], '.');
    table.appendChild(dotItem);
    
    // Resto de signos de puntuación
    const punctuation = [',', ';', ':', '?', '¿', '!', '¡', '-', '(', ')', '"', '=', '+', '/', '*'];
    
    for (let char of punctuation) {
        try {
            const response = await fetch(`${API_BASE_URL}/braille/info/${encodeURIComponent(char)}`);
            const data = await response.json();
            
            if (data.success) {
                const item = createBrailleCell(data.dots, char);
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
