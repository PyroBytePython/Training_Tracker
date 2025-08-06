// Анимация волн при загрузке
document.addEventListener('DOMContentLoaded', function() {
    const waves = document.querySelectorAll('.wave-divider path');
    waves.forEach((wave, index) => {
        wave.style.animation = `wave-animation ${10 - index * 2}s ease-in-out infinite alternate`;
    });
});

// Добавляем стили для анимации
const style = document.createElement('style');
style.textContent = `
    @keyframes wave-animation {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50px); }
    }
`;
document.head.appendChild(style);
