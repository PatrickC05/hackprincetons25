// document.addEventListener('DOMContentLoaded', function () {
//     if (window.location.pathname === '/') { // Only apply on home page
//         const container = document.getElementById('floating-money');
        
//         // Ensure the container has the correct dimensions before calculation
//         const containerWidth = container.offsetWidth;
//         const containerHeight = container.offsetHeight;
//         const moneySize = 30; // Size of the money signs (adjust as needed)

//         // Function to create a single money sign
//         function createMoneySign() {
//             const moneySign = document.createElement('span');
//             moneySign.classList.add('money');
//             moneySign.textContent = '$'; // Dollar sign
//             container.appendChild(moneySign);

//             // Random initial position, ensuring the sign doesn't start off-screen
//             let x = Math.random() * (containerWidth - moneySize); // Random X within container bounds
//             let y = Math.random() * (containerHeight - moneySize); // Random Y within container bounds
//             let xSpeed = Math.random() * 2 + 1; // Random speed in X direction
//             let ySpeed = Math.random() * 2 + 1; // Random speed in Y direction
//             let isSwimming = false; // Flag to control swimming away behavior
//             let swimAngle = 0;
//             let swimSpeed = 0;

//             // Set the initial position of the money sign
//             moneySign.style.position = 'absolute';
//             moneySign.style.transform = `translate(${x}px, ${y}px)`;

//             // Function to animate the money sign
//             function move() {
//                 // If the sign is "swimming," adjust its movement
//                 if (isSwimming) {
//                     x += Math.cos(swimAngle) * swimSpeed;
//                     y += Math.sin(swimAngle) * swimSpeed;
//                 } else {
//                     // Otherwise, perform the regular bouncing logic
//                     x += xSpeed;
//                     y += ySpeed;

//                     // If the money sign hits the boundaries, reverse its direction
//                     if (x >= containerWidth - moneySize || x <= 0) {
//                         xSpeed = -xSpeed;
//                     }
//                     if (y >= containerHeight - moneySize || y <= 0) {
//                         ySpeed = -ySpeed;
//                     }
//                 }

//                 // Apply the new position
//                 moneySign.style.transform = `translate(${x}px, ${y}px)`;

//                 requestAnimationFrame(move);  // Continue the animation
//             }

//             move();

//             // Return an object to access and manipulate the swimming behavior
//             return {
//                 moneySign: moneySign,
//                 startSwimming: function (clickX, clickY) {
//                     // Calculate the angle from the money sign to the click position
//                     const angle = Math.atan2(y - clickY, x - clickX);
//                     swimSpeed = 3 + Math.random() * 3;  // Random swimming speed
//                     swimAngle = angle;  // Set swimming direction
//                     isSwimming = true;  // Enable swimming behavior
//                 }
//             };
//         }

//         // Create multiple money signs
//         const moneySigns = [];
//         for (let i = 0; i < 100; i++) {  // You can increase the number to add more dollar signs
//             const money = createMoneySign();
//             moneySigns.push(money);
//         }

//         // Make the money swim away when the user clicks anywhere on the screen
//         container.addEventListener('click', function (event) {
//             const clickX = event.clientX - container.offsetLeft;  // Adjust for container position
//             const clickY = event.clientY - container.offsetTop;  // Adjust for container position

//             console.log(`Click at: ${clickX}, ${clickY}`); // Debugging log to check click position

//             // Loop through all the money signs and move them away from the click position
//             moneySigns.forEach(money => {
//                 money.startSwimming(clickX, clickY);
//             });
//         });
//     }
// });
document.addEventListener('DOMContentLoaded', function () {
    if (window.location.pathname === '/') { // Only apply on home page
        const container = document.getElementById('floating-money');
        const containerWidth = container.offsetWidth;
        const containerHeight = container.offsetHeight;
        const moneySize = 30; // Size of the money signs (adjust as needed)

        function createMoneySign() {
            const moneySign = document.createElement('span');
            moneySign.classList.add('money');
            moneySign.textContent = '$'; // Dollar sign

            container.appendChild(moneySign);

            // Random initial position, ensuring the sign doesn't start off-screen
            let x = Math.random() * (containerWidth - moneySize);
            let y = Math.random() * (containerHeight - moneySize);
            let xSpeed = Math.random() * 2 + 1; // Random speed in X direction
            let ySpeed = Math.random() * 2 + 1; // Random speed in Y direction

            // Function to animate the money sign
            function move() {
                x += xSpeed;
                y += ySpeed;

                // If the money sign hits the boundaries, reverse its direction
                if (x >= containerWidth - moneySize || x <= 0) {
                    xSpeed = -xSpeed;
                }
                if (y >= containerHeight - moneySize || y <= 0) {
                    ySpeed = -ySpeed;
                }

                // Apply the new position
                moneySign.style.transform = `translate(${x}px, ${y}px)`;

                requestAnimationFrame(move);  // Continue the animation
            }

            move();
        }

        // Create multiple money signs
        for (let i = 0; i < 100; i++) {  // You can increase the number to add more dollar signs
            createMoneySign();
        }
    }
});
