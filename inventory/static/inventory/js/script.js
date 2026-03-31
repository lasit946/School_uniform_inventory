const container = document.querySelector('.container');
const switchText = document.getElementById('switch-text');

switchText.addEventListener('click', (e) => {
    if (e.target.id === 'switch-btn') {
        container.classList.toggle('active');

        if (container.classList.contains('active')) {
            switchText.innerHTML = 'Already have an account? <span id="switch-btn">Login</span>';
        } else {
            switchText.innerHTML = 'Don\'t have an account? <span id="switch-btn">Register</span>';
        }
    }
});