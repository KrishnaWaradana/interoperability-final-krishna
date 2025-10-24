// Definisikan alamat API kita
const API_URL = 'http://127.0.0.1:8000';

// Event listener ini akan berjalan saat halaman HTML selesai dimuat
document.addEventListener('DOMContentLoaded', () => {
    loadEvents();
    
    const registerForm = document.getElementById('register-form');
    registerForm.addEventListener('submit', handleRegistration);
});

// Fungsi untuk mengambil dan menampilkan data event
async function loadEvents() {
    const eventListDiv = document.getElementById('event-list');
    const eventSelect = document.getElementById('event-select');
    
    eventListDiv.innerHTML = '<p>Memuat data event...</p>';
    eventSelect.innerHTML = '<option value="">-- Memuat event... --</option>';

    try {
        const response = await fetch(`${API_URL}/events/`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const events = await response.json();

        eventListDiv.innerHTML = ''; // Kosongkan div
        eventSelect.innerHTML = '<option value="">-- Pilih Event --</option>'; // Reset dropdown

        if (events.length === 0) {
            eventListDiv.innerHTML = '<p>Belum ada event yang tersedia.</p>';
            return;
        }

        events.forEach(event => {
            // 1. Tampilkan di daftar event
            const eventItem = document.createElement('div');
            eventItem.className = 'event-item';
            
            // Hitung sisa kuota
            const remainingQuota = event.quota - event.participants.length;
            
            eventItem.innerHTML = `
                <h3>${event.title}</h3>
                <p><strong>Tanggal:</strong> ${event.date}</p>
                <p><strong>Lokasi:</strong> ${event.location}</p>
                <p><strong>Sisa Kuota:</strong> ${remainingQuota} / ${event.quota}</p>
            `;
            eventListDiv.appendChild(eventItem);

            // 2. Tambahkan ke dropdown pendaftaran (jika kuota masih ada)
            if (remainingQuota > 0) {
                const option = document.createElement('option');
                option.value = event.id;
                option.textContent = `${event.title} (Sisa kuota: ${remainingQuota})`;
                eventSelect.appendChild(option);
            }
        });

    } catch (error) {
        console.error('Error fetching events:', error);
        eventListDiv.innerHTML = '<p>Gagal memuat data event. Cek koneksi API.</p>';
    }
}

// Fungsi untuk menangani submit form pendaftaran
async function handleRegistration(event) {
    event.preventDefault(); // Mencegah form reload halaman

    const form = event.target;
    const name = form.name.value;
    const email = form.email.value;
    const event_id = parseInt(form.event_id.value, 10);
    
    const messageEl = document.getElementById('register-message');
    messageEl.textContent = 'Sedang mendaftar...';
    messageEl.style.color = 'blue';

    if (!event_id) {
        messageEl.textContent = 'Silakan pilih event terlebih dahulu.';
        messageEl.style.color = 'red';
        return;
    }

    const registrationData = {
        name: name,
        email: email,
        event_id: event_id
    };

    try {
        const response = await fetch(`${API_URL}/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(registrationData),
        });

        if (response.ok) {
            // Berhasil
            const result = await response.json();
            messageEl.textContent = `Pendaftaran berhasil! (ID Peserta: ${result.id})`;
            messageEl.style.color = 'green';
            form.reset(); // Kosongkan form
            loadEvents(); // Muat ulang data event (untuk update kuota)
        } else {
            // Gagal (misal kuota penuh atau event not found)
            const errorData = await response.json();
            messageEl.textContent = `Pendaftaran gagal: ${errorData.detail}`;
            messageEl.style.color = 'red';
        }

    } catch (error) {
        console.error('Error registering:', error);
        messageEl.textContent = 'Terjadi kesalahan. Tidak dapat terhubung ke server.';
        messageEl.style.color = 'red';
    }
}