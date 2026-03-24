// Костыль для localhost:8080 vs 8000, потом переделать
const API_BASE = window.location.origin;


const shortenForm = document.getElementById('shortenForm');
const statsForm = document.getElementById('statsForm');
const longUrlInput = document.getElementById('longUrl');
const shortIdInput = document.getElementById('shortId');
const resultDiv = document.getElementById('result');
const shortUrlInput = document.getElementById('shortUrl');
const copyBtn = document.getElementById('copyBtn');
const statsLink = document.getElementById('statsLink');
const statsResultDiv = document.getElementById('statsResult');
const statsIdSpan = document.getElementById('statsId');
const statsClicksSpan = document.getElementById('statsClicks');

// Состояние загрузки
let isLoading = false;

// Создание короткой ссылки
shortenForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const url = longUrlInput.value.trim();
    if (!url) {
        alert('Введите URL');
        return;
    }

    if (isLoading) return; 
   
    const submitBtn = shortenForm.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.textContent;
    submitBtn.textContent = '🔄 Создаём...';
    isLoading = true;

    try {
        const response = await fetch(`${API_BASE}/shorten`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Ошибка при создании ссылки');
        }

        const data = await response.json();

     
        shortUrlInput.value = data.short_url;
        statsLink.href = `${API_BASE}/stats/${data.short_id}`;
        resultDiv.classList.remove('hidden');

       
        longUrlInput.value = '';

       
        resultDiv.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        console.error('Shorten error:', error);
        alert('Ошибка: ' + error.message);
    } finally {
        submitBtn.textContent = originalBtnText;
        isLoading = false;
    }
});

// Копирование в буфер обмена - современный способ
copyBtn.addEventListener('click', async () => {
    try {
        await navigator.clipboard.writeText(shortUrlInput.value);

       
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✅ Скопировано!';
        setTimeout(() => {
            copyBtn.textContent = originalText;
        }, 2000);
    } catch (err) {
        // Fallback для старых браузеров
        shortUrlInput.select();
        document.execCommand('copy'); // Старый способ, но работает
        alert('Скопировано (старый браузер)');
    }
});

// Проверка статистики
statsForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const shortId = shortIdInput.value.trim();
    if (!shortId) {
        alert('Введите ID ссылки');
        return;
    }

    if (isLoading) return;

    const submitBtn = statsForm.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.textContent;
    submitBtn.textContent = '🔄 Ищем...';
    isLoading = true;

    try {
        const response = await fetch(`${API_BASE}/stats/${shortId}`);

        if (!response.ok) {
            if (response.status === 404) {
                throw new Error('Ссылка не найдена');
            }
            throw new Error('Ошибка при получении статистики');
        }

        const data = await response.json();

    
        statsIdSpan.textContent = data.short_id;
        statsClicksSpan.textContent = data.clicks;
        statsResultDiv.classList.remove('hidden');

        // Очищаем поле ввода
        shortIdInput.value = '';

        // Автоскролл
        statsResultDiv.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        console.error('Stats error:', error);
        alert('Ошибка: ' + error.message);
        statsResultDiv.classList.add('hidden');
    } finally {
        submitBtn.textContent = originalBtnText;
        isLoading = false;
    }
});


longUrlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        shortenForm.dispatchEvent(new Event('submit'));
    }
});

shortIdInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        statsForm.dispatchEvent(new Event('submit'));
    }
});

//  добавить валидацию URL на клиенте
// добавить кэширование последних ссылок в localStorage
//  сделать красивый тостер вместо alert