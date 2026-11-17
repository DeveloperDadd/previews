// components/sections/faq/*/script.js, plus aria-expanded for screen readers
const faqItems = Array.from(document.querySelectorAll('.cs-faq-item'));
for (const item of faqItems) {
    const button = item.querySelector('.cs-button');
    item.addEventListener('click', () => {
        item.classList.toggle('active');
        if (button) button.setAttribute('aria-expanded', item.classList.contains('active') ? 'true' : 'false');
    });
}
