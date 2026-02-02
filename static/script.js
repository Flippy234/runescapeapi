document.querySelectorAll('.skill-card').forEach(card => {
    card.addEventListener('mouseenter', function () {
        const sparkle = document.createElement('div');
        sparkle.className = 'sparkle';
        sparkle.style.top = Math.random() * 80 + 10 + '%';
        sparkle.style.left = Math.random() * 80 + 10 + '%';
        sparkle.style.animationDelay = '0s';
        sparkle.style.animationDuration = '1s';
        this.appendChild(sparkle);
        setTimeout(() => { sparkle.remove(); }, 1000);
    });
});

setTimeout(() => {
    document.querySelectorAll('.progress-bar').forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => { bar.style.width = width; }, 100);
    });
}, 500);

document.querySelectorAll('.skill-card').forEach(card => {
    const levelElement = card.querySelector('.skill-level');
    const level = parseInt(levelElement.textContent);
    if (level >= 90) {
        card.classList.add('high-level');
    }
});