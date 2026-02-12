// ── Nav scroll effect ──
window.addEventListener('scroll', () => {
    document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50);
});

// ── Scroll animations ──
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) entry.target.classList.add('visible');
    });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.animate-in').forEach(el => observer.observe(el));

// ── Schema tabs ──
document.querySelectorAll('.schema-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.schema-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        document.querySelectorAll('.schema-code').forEach(c => c.style.display = 'none');
        document.getElementById('schema-' + tab.dataset.tab).style.display = 'block';
    });
});

// ── Toast ──
function showToast(message, isError = false) {
    const toast = document.getElementById('toast');
    const icon = document.getElementById('toastIcon');
    const msg = document.getElementById('toastMsg');
    msg.textContent = message;
    icon.textContent = isError ? '❌' : '✅';
    toast.className = isError ? 'toast error show' : 'toast show';
    setTimeout(() => toast.classList.remove('show'), 4000);
}

// ── Waitlist form ──
document.getElementById('waitlistForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('submitBtn');
    btn.disabled = true;
    btn.innerHTML = 'Submitting…';

    const formData = {
        name: document.getElementById('name').value.trim(),
        email: document.getElementById('email').value.trim(),
        firm: document.getElementById('firm').value.trim(),
        role: document.getElementById('role').value || 'Not specified'
    };

    try {
        const res = await fetch('/api/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const data = await res.json();
        if (res.ok && data.success) {
            showToast(data.message);
            e.target.reset();
        } else {
            showToast(data.error || 'Something went wrong.', true);
        }
    } catch (err) {
        showToast('Network error. Please try again.', true);
    } finally {
        btn.disabled = false;
        btn.innerHTML = 'Request Access <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>';
    }
});

// ── Smooth scroll for nav links ──
document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(link.getAttribute('href'));
        if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
});
