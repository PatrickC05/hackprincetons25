document.addEventListener('DOMContentLoaded', function () {
    // Only trigger the animation on the home page
    if (window.location.pathname === '/') {
        const moneySigns = document.querySelectorAll('.money');
        const container = document.getElementById('floating-money');
        const containerWidth = container.offsetWidth;
        const containerHeight = container.offsetHeight;

        function animateMoneySign(moneySign) {
            let x = Math.random() * containerWidth;  
            let y = Math.random() * containerHeight; 
            let xSpeed = Math.random() * 2 + 1; 
            let ySpeed = Math.random() * 2 + 1; 

            function move() {
                x += xSpeed;
                y += ySpeed;

                // If the money sign hits the boundaries, reverse its direction
                if (x >= containerWidth - 50 || x <= 0) {
                    xSpeed = -xSpeed;
                }
                if (y >= containerHeight - 50 || y <= 0) {
                    ySpeed = -ySpeed;
                }

                moneySign.style.transform = `translate(${x}px, ${y}px)`;
                requestAnimationFrame(move); 
            }
            move();
        }

        // Start the animation for each money sign
        moneySigns.forEach(sign => animateMoneySign(sign));
    }
});