let currentData = [];
let availableTags = [];

// DOM Elements
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('excel-file');
const tableHead = document.getElementById('table-head');
const tableBody = document.getElementById('table-body');
const tagButtons = document.getElementById('tag-buttons');
const editor = document.getElementById('mail-editor');
const subjectInput = document.getElementById('mail-subject');

// Drag & Drop Handling
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
});

dropZone.addEventListener('drop', handleDrop, false);
fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

function handleDrop(e) {
    let dt = e.dataTransfer;
    let files = dt.files;
    handleFiles(files);
}

function handleFiles(files) {
    if (files.length > 0) {
        uploadExcel(files[0]);
    }
}

async function uploadExcel(file) {
    const formData = new FormData();
    formData.append('file', file);

    // UX Feedback
    dropZone.innerHTML = '<div class="spinner-border text-primary" role="status"></div>';

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();

        if (result.data && result.data.length > 0) {
            currentData = result.data;
            availableTags = Object.keys(currentData[0]);
            renderTable();
            renderTags();
        }

        // Reset Dropzone UI
        dropZone.innerHTML = `
            <input type="file" id="excel-file" class="d-none" accept=".xlsx, .xls">
            <label for="excel-file" class="btn btn-light btn-sm mb-2 shadow-sm text-primary fw-medium" style="cursor: pointer;">✔️ Dosya Yüklendi (${file.name})</label>
            <p class="text-muted small mb-0">Değiştirmek için tekrar sürükleyin</p>
        `;
        document.getElementById('excel-file').addEventListener('change', (e) => handleFiles(e.target.files));

    } catch (error) {
        alert('Dosya yüklenirken hata oluştu. Lütfen geçerli bir Excel yükleyin.');
        console.error(error);
        window.location.reload();
    }
}

function renderTable() {
    if (currentData.length === 0) return;

    // Head
    tableHead.innerHTML = availableTags.map(tag => `<th class="ps-3 py-2">${tag}</th>`).join('');

    // Body
    tableBody.innerHTML = currentData.map(row => {
        return `<tr>${availableTags.map((tag, i) => `<td class="${i === 0 ? 'ps-3 fw-medium' : ''}">${row[tag] || '-'}</td>`).join('')}</tr>`;
    }).join('');
}

function renderTags() {
    tagButtons.innerHTML = availableTags.map(tag => {
        return `<button class="btn btn-sm btn-outline-primary fw-medium" onclick="insertTag('${tag}')">[${tag}] Ekle</button>`;
    }).join('');
}

function insertTag(tag) {
    const tagString = `{{${tag}}}`;
    const startPos = editor.selectionStart;
    const endPos = editor.selectionEnd;

    editor.value = editor.value.substring(0, startPos) + tagString + editor.value.substring(endPos, editor.value.length);
    editor.focus();
    editor.selectionStart = startPos + tagString.length;
    editor.selectionEnd = startPos + tagString.length;
}

function downloadTemplate() {
    window.location.href = '/api/download-template';
}

async function startSending() {
    if (currentData.length === 0) {
        alert('Lütfen önce bir Excel dosyası yükleyin.');
        return;
    }

    if (!subjectInput.value || !editor.value) {
        alert('Lütfen konu ve mail içeriğini doldurun.');
        return;
    }

    const savedSmtp = localStorage.getItem('smtpSettings');
    let smtpSettings = null;
    if (savedSmtp) {
        smtpSettings = JSON.parse(savedSmtp);
        if (!smtpSettings.server || !smtpSettings.user || !smtpSettings.password) {
            alert('SMTP Ayarlarınız eksik. Lütfen sağ üstten ⚙️ Ayarlar menüsüne girip eksikleri tamamlayın.');
            openSmtpModal();
            return;
        }
    } else {
        alert('İlk gönderimden önce sağ üstten ⚙️ Ayarlar menüsüne girip SMTP mail bilgilerinizi kaydetmelisiniz.');
        openSmtpModal();
        return;
    }

    const payload = {
        subject: subjectInput.value,
        body_template: editor.value,
        recipients: currentData,
        smtp_settings: smtpSettings
    };

    try {
        const bgBtn = document.querySelector('button.btn-primary');
        const origText = bgBtn.innerHTML;
        bgBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Başlatılıyor...';
        bgBtn.disabled = true;

        const response = await fetch('/api/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await response.json();

        if (response.ok) {
            alert("✔️ " + result.message);
        } else {
            alert("❌ Hata: " + (result.detail || result.message));
        }

        bgBtn.innerHTML = origText;
        bgBtn.disabled = false;
    } catch (error) {
        alert('Gönderim başlatılamadı. Backend bağlantısını kontrol edin.');
    }
}

async function saveCurrentTemplate() {
    if (!subjectInput.value || !editor.value) {
        alert('Lütfen konu ve mail içeriğini doldurun.');
        return;
    }

    const name = prompt("Şablon için bir isim girin:");
    if (!name) return;

    const payload = {
        name: name,
        subject: subjectInput.value,
        body: editor.value
    };

    try {
        const response = await fetch('/api/templates', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await response.json();
        alert("✔️ " + result.message);
    } catch (error) {
        alert('Şablon kaydedilemedi.');
    }
}

// Modal handling
let templatesModal;
let smtpModal;

document.addEventListener("DOMContentLoaded", () => {
    templatesModal = new bootstrap.Modal(document.getElementById('templatesModal'));
    smtpModal = new bootstrap.Modal(document.getElementById('smtpModal'));

    // Load saved SMTP settings
    const savedSmtp = localStorage.getItem('smtpSettings');
    if (savedSmtp) {
        const smtp = JSON.parse(savedSmtp);
        document.getElementById('smtp-server').value = smtp.server || '';
        document.getElementById('smtp-port').value = smtp.port || '465';
        document.getElementById('smtp-user').value = smtp.user || '';
        document.getElementById('smtp-password').value = smtp.password || '';
    }

    // Check Authentication
    fetch('/api/me')
        .then(res => res.json())
        .then(data => {
            if (data.logged_in) {
                document.getElementById('user-info').classList.remove('d-none');
                document.getElementById('user-info').classList.add('d-flex');
                document.getElementById('user-name').innerText = data.user.name;
                document.getElementById('user-avatar').src = data.user.picture;

                document.getElementById('btn-login').classList.add('d-none');
                document.getElementById('btn-logout').classList.remove('d-none');
            }
        }).catch(err => console.error(err));
});

function openSmtpModal() {
    smtpModal.show();
}

function saveSmtpSettings() {
    const smtp = {
        server: document.getElementById('smtp-server').value,
        port: document.getElementById('smtp-port').value,
        user: document.getElementById('smtp-user').value,
        password: document.getElementById('smtp-password').value
    };
    localStorage.setItem('smtpSettings', JSON.stringify(smtp));
    alert('SMTP Ayarları başarıyla tarayıcıya kaydedildi.');
    smtpModal.hide();
}

async function openTemplatesModal() {
    try {
        const response = await fetch('/api/templates');
        const result = await response.json();

        const list = document.getElementById('templates-list');
        if (result.templates.length === 0) {
            list.innerHTML = '<li class="list-group-item text-center text-muted py-4">Kayıtlı şablon bulunamadı.</li>';
        } else {
            list.innerHTML = result.templates.map(t => {
                const encodedData = encodeURIComponent(JSON.stringify(t));
                return `
                    <li class="list-group-item d-flex justify-content-between align-items-center list-group-item-action py-3" style="cursor:pointer;" onclick="loadTemplate('${encodedData}')">
                        <span class="fw-medium">${t.name}</span>
                        <small class="text-muted opacity-75">${t.subject}</small>
                    </li>
                `;
            }).join('');
        }

        templatesModal.show();
    } catch (error) {
        alert('Şablonlar yüklenemedi.');
    }
}

function loadTemplate(encodedData) {
    const template = JSON.parse(decodeURIComponent(encodedData));
    subjectInput.value = template.subject;
    editor.value = template.body;
    templatesModal.hide();
}
