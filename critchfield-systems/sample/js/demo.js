// Sample site: forms don't send anywhere, they explain that instead.
document.querySelectorAll('form').forEach((form) => {
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const note = form.querySelector('.cs-demo-note');
        if (!note) return;
        note.innerHTML = 'This is a sample site, so nothing was sent. On your real website this form goes straight to your inbox. <a href="tel:+18592707050">Call or text Critchfield Systems at (859) 270-7050</a>.';
        note.classList.add('cs-show');
    });
});
const year = document.getElementById('cs-year');
if (year) year.textContent = new Date().getFullYear();
